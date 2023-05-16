from django.db import models

class NewTable(models.Model):
    bigint_f = models.BigIntegerField()
    bool_f   = models.BooleanField()
    date_f   = models.DateField(auto_now=True)
    char_f   = models.CharField(max_length=20, unique=True)
    datetime_f=models.DateTimeField(auto_now_add=True)
    decimal_f= models.DecimalField(max_digits=10, decimal_places=2)
    float_f  = models.FloatField(null=True)
    int_f    = models.IntegerField(default=2010)
    text_f   = models.TextField()
    
class Product(models.Model):
    SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    sku = models.CharField(max_length=5)
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    size = models.CharField(max_length=1, choices=SIZES)
    qty = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

