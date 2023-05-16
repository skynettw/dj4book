from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from allauth.account.decorators import verified_email_required
from mysite import models
from cart.cart import Cart
from mysite import forms
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage

def index(request, id=0):
    try:
        all_products = None
        all_categories = models.Category.objects.all()

        if id > 0:
            category = models.Category.objects.get(id=id)
            if category is not None:
                all_products = models.Product.objects.filter(category=category)

        if all_products is None:
            all_products = models.Product.objects.all()

        paginator = Paginator(all_products, 5)

        p = request.GET.get('p')

        products = paginator.page(p)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    except Exception:
        products = []
    all_categories = models.Category.objects.all()    
    return render(request, 'index.html', locals())

def product(request, id):
    try:
        product = models.Product.objects.get(id=id)
    except:
        product = None

    return render(request, 'product.html', locals())

@login_required
def add_to_cart(request, id, quantity):
    cart = Cart(request)
    product = models.Product.objects.get(id=id)
    cart.add(product=product, quantity=quantity)
    return redirect('/')

@login_required
def remove_from_cart(request, id):
    product = models.Product.objects.get(id=id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('/cart/')

@login_required
def cart_detail(request):
    all_categories = models.Category.objects.all()
    cart = Cart(request).cart

    total_price = 0
    for _, item in cart.items():
        current_price = float(item['price']) * int(item['quantity'])
        total_price += current_price
    
    return render(request, 'cart.html', locals())

@verified_email_required
def order(request):
    all_categories = models.Category.objects.all()
    cartInstance = Cart(request)
    cart = cartInstance.cart
    total_price = 0
    for _, item in cart.items():
        current_price = float(item['price']) * int(item['quantity'])
        total_price += current_price

    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        new_order = models.Order(user=user)

        form = forms.OrderForm(request.POST, instance=new_order)
        if form.is_valid():
            order = form.save()
            email_messages = "您的購物內容如下：\n"
            for _, item in cart.items():
                product = models.Product.objects.get(id=item['product_id'])
                models.OrderItem.objects.create(
                    order=order, 
                    product=product,
                    price = item['price'],
                    quantity=item['quantity']
                )
                email_messages = email_messages + "\n" + \
                                "{}, {}, {}".format(item['name'], \
                                item['price'], item['quantity'])
            email_messages = email_messages + \
                    "\n以上共計{}元\nhttp://mshop.min-haung.com感謝您的訂購！".\
                    format(total_price)

            cartInstance.clear()

            messages.add_message(request, messages.INFO, "訂單已儲存，我們會儘快處理。")
            email = EmailMessage("感謝您的訂購", 
                email_messages, 
                '迷你小電商<ho@min-huang.com>',
                [request.user.email])
            email.send()
            email = EmailMessage("有人訂購產品囉", 
                email_messages, 
                '迷你小電商<ho@min-huang.com>',
                ['skynet.tw@gmail.com'])
            email.send()
            return redirect('/myorders/')
    else:
        form = forms.OrderForm()

    return render(request, 'order.html', locals())

@login_required
def my_orders(request):
    all_categories = models.Category.objects.all()
    orders = models.Order.objects.filter(user=request.user)
    return render(request, 'myorders.html', locals())

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html', locals())

@login_required
def payment(request, id):
    try:
        all_categories = models.Category.objects.all()
        order = models.Order.objects.get(id=id)
        all_order_items = models.OrderItem.objects.filter(order=order)

        items = list()
        total = 0
        for order_item in all_order_items:
            t = dict()
            t['name'] = order_item.product.name
            t['price'] = order_item.product.price
            t['quantity'] = order_item.quantity
            t['subtotal'] = order_item.product.price * order_item.quantity
            total = total + order_item.product.price
            items.append(t)

        host = request.get_host()
        paypal_dict = {
            "business": settings.PAYPAL_REVEIVER_EMAIL,
            "amount": total,
            "item_name": "迷你小電商貨品編號:{}".format(id),
            "invoice": "invoice-{}".format(id),
            "currency_code": 'TWD',
            "notify_url": "http://{}{}".format(host, reverse('paypal-ipn')),
            "return_url": "http://{}/done/".format(host),
            "cancel_return": "http://{}/canceled/".format(host),
            }
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)

        return render(request, 'payment.html', locals())
    except:
        messages.add_message(request, messages.WARNING, "訂單編號錯誤，無法處理付款。")
        return redirect('/myorders/')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_canceled.html', locals())
