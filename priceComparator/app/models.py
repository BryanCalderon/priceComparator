from django.db import models


# Create your models here.

class Product(models.Model):
    sku = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    status = models.IntegerField()
    url = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.FloatField(max_length=30)
    normal_price = models.FloatField(max_length=30)
    offer_price = models.FloatField(max_length=30)
    creation_date = models.DateField()
    update_date = models.DateField()
