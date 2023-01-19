from django.db import models

class Maker(models.Model):
    name = models.CharField(max_length=10)
    country = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class PModel(models.Model):
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    url = models.URLField(default='http://i.imgur.com/Ous4iGB.png')

    def __str__(self):
        return self.name

class Product(models.Model):
    pmodel = models.ForeignKey(PModel, on_delete=models.CASCADE, verbose_name='型號')
    nickname = models.CharField(max_length=15, default='超值二手機', verbose_name='摘要')
    description = models.TextField(default='暫無說明')
    year = models.PositiveIntegerField(default=2016, verbose_name='出廠年份')
    price = models.PositiveIntegerField(default=0, verbose_name='價格')


    def __str__(self):
        return self.nickname

class PPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.CharField(max_length=20, default='產品照片')
    url = models.URLField(default='http://i.imgur.com/Z230eeq.png')
    media = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.description

