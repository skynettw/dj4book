from django.contrib import admin
from mysite import models

class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'sku', 'name', 'stock', 'price')
    ordering = ('category',)

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
