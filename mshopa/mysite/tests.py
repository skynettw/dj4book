from django.test import TestCase

from decimal import Decimal

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.core import mail
from django.test import Client, override_settings
from filer.models import Image
from paypal.standard.forms import PayPalPaymentsForm

from .models import Category, Order, OrderItem, Product


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ShopUpgradeTests(TestCase):
    """Local SQLite tests; no payment, mail or social-login network requests."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='example-user', email='example@test.invalid', password='test-only-password')
        EmailAddress.objects.create(user=cls.user, email=cls.user.email, verified=True, primary=True)
        cls.category = Category.objects.create(name='Example category')
        image = Image.objects.create(name='Example image', original_filename='example.png')
        # Catalog rendering needs a URL, not an actual file or storage write.
        Image.objects.filter(pk=image.pk).update(file='test-only/example.png')
        cls.product = Product.objects.create(
            category=cls.category, sku='TEST-1', name='Example product',
            description='Teaching example', image=image, stock=10, price=Decimal('12.50'))

    def login(self):
        self.client.force_login(self.user, backend='django.contrib.auth.backends.ModelBackend')

    def test_catalog_category_and_product_pages(self):
        for url in ['/', '/%d/' % self.category.pk, '/product/%d/' % self.product.pk]:
            with self.subTest(url=url):
                self.assertContains(self.client.get(url), self.product.name)

    def test_anonymous_cart_change_requires_login(self):
        response = self.client.get('/cart/additem/%d/2/' % self.product.pk)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_cart_add_render_and_remove(self):
        self.login()
        for _ in range(2):
            self.assertEqual(self.client.get('/cart/additem/%d/1/' % self.product.pk).status_code, 302)
        self.assertEqual(self.client.session['cart'][str(self.product.pk)]['quantity'], 2)
        self.assertContains(self.client.get('/cart/'), self.product.name)
        self.assertEqual(self.client.get('/cart/removeitem/%d/' % self.product.pk).status_code, 302)
        self.assertNotIn(str(self.product.pk), self.client.session['cart'])

    def test_verified_user_can_create_order_without_external_email(self):
        self.login()
        for _ in range(2):
            self.client.get('/cart/additem/%d/1/' % self.product.pk)
        response = self.client.post('/order/', {
            'full_name': 'Example', 'address': 'Test address', 'phone': '0000000000'})
        self.assertRedirects(response, '/myorders/')
        order = Order.objects.get(user=self.user)
        item = OrderItem.objects.get(order=order)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, Decimal('12.50'))
        self.assertEqual(self.client.session['cart'], {})
        self.assertEqual(len(mail.outbox), 2)

    def test_allauth_login_and_signup_pages(self):
        for url in ['/accounts/login/', '/accounts/signup/']:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_login_post_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/accounts/login/', {}).status_code, 403)

    def test_paypal_form_still_renders_locally(self):
        form = PayPalPaymentsForm(initial={
            'business': 'example@test.invalid', 'amount': '25.00',
            'item_name': 'Teaching example', 'invoice': 'test-only', 'currency_code': 'TWD'})
        self.assertIn('Teaching example', form.render())
