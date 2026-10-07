"""Exercise real filer uploads and thumbnail bytes, with isolated storage."""
from io import BytesIO
from pathlib import Path
import tempfile
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from filer.fields import multistorage_file
from filer.models import File, Image
from PIL import Image as PILImage

from .models import Category, Product


class ImageUploadTests(TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.temp = tempfile.TemporaryDirectory(prefix='image-tests-', dir=root)
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(root))
        self.addCleanup(self.temp.cleanup)
        for attribute, folder in [('STORAGES', 'originals'), ('THUMBNAIL_STORAGES', 'thumbs')]:
            storage = FileSystemStorage(location=self.root / folder, base_url='/test-media/')
            replacement = patch.dict(getattr(multistorage_file, attribute),
                                     {'public': storage, 'private': storage})
            replacement.start()
            self.addCleanup(replacement.stop)
        self.user = User.objects.create_superuser('image-admin', 'image@test.invalid', 'test-only')
        self.client.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        self.url = reverse('admin:filer-ajax_upload')

    def image_bytes(self, format, **kwargs):
        output = BytesIO()
        mode = 'RGBA' if format == 'PNG' else 'RGB'
        with PILImage.new(mode, (80, 40), (10, 100, 200, 80) if mode == 'RGBA' else (10, 100, 200)) as image:
            image.save(output, format=format, **kwargs)
        return output.getvalue()

    def upload(self, name, data, client=None):
        return (client or self.client).post(self.url, {'file': SimpleUploadedFile(name, data)})

    def test_real_upload_decode_and_thumbnail_formats(self):
        for format, extension in [('JPEG', 'jpg'), ('PNG', 'png'), ('GIF', 'gif'), ('WEBP', 'webp')]:
            with self.subTest(format=format):
                response = self.upload('sample.' + extension, self.image_bytes(format))
                self.assertEqual(response.status_code, 200, response.content)
                image = Image.objects.get(pk=response.json()['file_id'])
                with image.file.storage.open(image.file.name) as source, PILImage.open(source) as decoded:
                    decoded.load()
                    self.assertEqual(decoded.size, (80, 40))
                    self.assertEqual(decoded.format, format)
                    if format == 'PNG':
                        self.assertEqual(decoded.getpixel((0, 0))[3], 80)
                thumbnail = image.file.get_thumbnail({'size': (32, 32), 'crop': True})
                with thumbnail.storage.open(thumbnail.name) as source, PILImage.open(source) as decoded:
                    decoded.load()
                    self.assertEqual(decoded.size, (32, 32))
                    if format == 'PNG':
                        self.assertEqual(decoded.convert('RGBA').getpixel((0, 0))[3], 80)
                product = Product.objects.create(
                    category=Category.objects.create(name=format), sku=format,
                    name='Real ' + format, description='Image integration',
                    image=image, stock=1, price='1.00')
                self.assertContains(self.client.get('/product/%d/' % product.pk), image.file.url)
                image.file.close()

    def test_animated_gif_frames_preserved(self):
        output = BytesIO()
        with PILImage.new('RGB', (80, 40), 'red') as first, PILImage.new('RGB', (80, 40), 'blue') as second:
            first.save(output, format='GIF', save_all=True, append_images=[second], duration=50, loop=0)
        response = self.upload('animated.gif', output.getvalue())
        self.assertEqual(response.status_code, 200, response.content)
        image = Image.objects.get(pk=response.json()['file_id'])
        with image.file.storage.open(image.file.name) as source, PILImage.open(source) as decoded:
            self.assertEqual(decoded.n_frames, 2)
            decoded.seek(1)
            decoded.load()
            self.assertEqual(decoded.convert('RGB').getpixel((0, 0)), (0, 0, 255))
        image.file.close()

    def test_exif_orientation_thumbnail(self):
        exif = PILImage.Exif()
        exif[274] = 6
        response = self.upload('rotated.jpg', self.image_bytes('JPEG', exif=exif))
        self.assertEqual(response.status_code, 200, response.content)
        image = Image.objects.get(pk=response.json()['file_id'])
        thumbnail = image.file.get_thumbnail({'size': (32, 32), 'crop': False})
        with thumbnail.storage.open(thumbnail.name) as source, PILImage.open(source) as decoded:
            decoded.load()
            self.assertEqual(decoded.size, (16, 32))
        image.file.close()

    def assert_rejected_without_storage(self, name, data):
        response = self.upload(name, data)
        self.assertEqual(response.status_code, 400, response.content)
        self.assertEqual(File.objects.count(), 0)
        self.assertFalse(any(path.is_file() for path in self.root.rglob('*')))

    def test_fake_image_rejected(self):
        self.assert_rejected_without_storage('fake.png', b'not an image')

    def test_truncated_jpeg_rejected(self):
        self.assert_rejected_without_storage('broken.jpg', self.image_bytes('JPEG')[:-30])

    def test_mismatched_image_extension_rejected(self):
        self.assert_rejected_without_storage('disguised.png', self.image_bytes('JPEG'))

    def test_truncated_png_rejected(self):
        self.assert_rejected_without_storage('broken.png', self.image_bytes('PNG')[:-20])

    def test_pixel_limit_rejected(self):
        with patch('PIL.Image.MAX_IMAGE_PIXELS', 100):
            self.assert_rejected_without_storage('large.png', self.image_bytes('PNG'))

    def test_upload_requires_permission_and_csrf(self):
        anonymous = self.upload('sample.png', self.image_bytes('PNG'), Client())
        self.assertEqual(anonymous.status_code, 302)
        staff = User.objects.create_user('staff-only', password='test-only', is_staff=True)
        client = Client()
        client.force_login(staff, backend='django.contrib.auth.backends.ModelBackend')
        self.assertEqual(self.upload('sample.png', self.image_bytes('PNG'), client).status_code, 403)
        csrf = Client(enforce_csrf_checks=True)
        csrf.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')
        self.assertEqual(self.upload('sample.png', self.image_bytes('PNG'), csrf).status_code, 403)
        self.assertEqual(File.objects.count(), 0)
