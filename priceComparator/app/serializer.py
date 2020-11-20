from rest_framework import serializers

from .models import Product, Store, User


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'image', 'url', 'price', 'model', 'brand', 'normal_price', 'offer_price',
                  'updated_date', 'user']


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'url', 'name', 'crawler']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'last_name', 'identification', 'email', 'uid', 'is_active']
