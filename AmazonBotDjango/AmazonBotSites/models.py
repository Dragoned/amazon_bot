from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    link = models.TextField()
    descrizione = models.TextField(null=True, blank=True)

class Price(models.Model):
    price = models.FloatField()
    datetime = models.DateTimeField()
    ID_Product = models.ForeignKey(Product, on_delete=models.CASCADE)