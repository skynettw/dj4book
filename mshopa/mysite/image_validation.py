"""Validate raster upload contents before filer writes them to storage."""
import warnings

from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


def validate_raster_upload(file_name, file, owner, mime_type):
    formats = {'image/jpeg': 'JPEG', 'image/png': 'PNG',
               'image/gif': 'GIF', 'image/webp': 'WEBP'}
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            file.seek(0)
            with Image.open(file, formats=[formats[mime_type]]) as image:
                if image.format != formats[mime_type]:
                    raise ValidationError('Image contents do not match the file extension.')
                image.verify()
            # verify() alone does not decode JPEG pixels. Decode every frame too.
            file.seek(0)
            with Image.open(file, formats=[formats[mime_type]]) as image:
                for frame in range(getattr(image, 'n_frames', 1)):
                    image.seek(frame)
                    image.load()
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError,
            Image.DecompressionBombError, Image.DecompressionBombWarning) as error:
        raise ValidationError('Invalid, incomplete or oversized image.') from error
    finally:
        file.seek(0)
