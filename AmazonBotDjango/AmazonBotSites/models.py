from django.db import models
from Account.models import Account

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    link = models.TextField()
    descrizione = models.TextField(null=True, blank=True)
    User = models.ManyToManyField(Account, through='Traking')

class Price(models.Model):
    price = models.FloatField()
    datetime = models.DateTimeField()
    ID_Product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=255)
    product = models.ManyToManyField(Product)

class Traking(models.Model):
    ID_Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ID_User = models.ForeignKey(Account, on_delete=models.CASCADE)
    target_price = models.FloatField()

class ProductList(models.Model):
    name = models.CharField(max_length=255)
    target_price = models.FloatField()
    ID_User = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='ProdContent')

class ProdContent(models.Model):
    ID_Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ID_ProductList = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    quantity = models.IntegerField()