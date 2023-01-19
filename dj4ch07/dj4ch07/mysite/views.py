from django.shortcuts import render
from mysite import models

def index(request):
    products = models.Product.objects.all()
    return render(request, 'index.html', locals())

def detail(request, id):
    try:
        product = models.Product.objects.get(id=id)
        images = models.PPhoto.objects.filter(product=product)
    except:
        pass
    return render(request, 'detail.html', locals())
