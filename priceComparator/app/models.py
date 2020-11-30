from django.db import models
from django.utils import timezone
from rest_framework import serializers


class Store(models.Model):
    name = models.CharField(max_length=50)
    crawler = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    created = serializers.HiddenField(default=timezone.now())


class User(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    identification = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100)
    created = serializers.HiddenField(default=timezone.now())
    is_active = models.BooleanField(default=True)
    uid = models.CharField(max_length=100)

    def __str__(self):
        return "{} {}".format(self.name, self.last_name)


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
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='products', on_delete=models.DO_NOTHING, null=True)
    store = models.ForeignKey(Store, related_name='products', on_delete=models.DO_NOTHING, null=True)
    related_to = models.ForeignKey('self', related_name='childs', on_delete=models.DO_NOTHING, null=True)


class TypePrice(models.Model):
    descripcion = models.CharField(max_length=50)


class ProductPrice(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    price = models.FloatField(max_length=30)
    type = models.ForeignKey(TypePrice, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
