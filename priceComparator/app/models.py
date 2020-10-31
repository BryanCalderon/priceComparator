from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=30)
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=455)
    status = models.BooleanField(default=True)
    url = models.CharField(max_length=455)
    brand = models.CharField(max_length=50, null=True)
    model = models.CharField(max_length=50, null=True)
    price = models.FloatField(max_length=30)
    normal_price = models.FloatField(max_length=30, null=True)
    offer_price = models.FloatField(max_length=30, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)
