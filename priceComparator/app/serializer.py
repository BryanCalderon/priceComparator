from rest_framework import serializers

from .models import Product, Store, User, TypePrice, ProductPrice


class StoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'url', 'name', 'crawler']


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    store = StoreSerializer(read_only=True)
    related_to = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), allow_null=True)
    updated_date = serializers.DateTimeField(allow_null=True)
    creation_date = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'image', 'url', 'price', 'model', 'brand', 'normal_price', 'offer_price',
                  'updated_date', 'user', 'store', 'related_to', 'creation_date']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    last_name = serializers.CharField(allow_null=True, required=False)
    identification = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'last_name', 'identification', 'email', 'uid', 'is_active']


class TypePriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypePrice
        fields = ['id', 'descripcion']


class ProductPriceSerializer(serializers.HyperlinkedModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=ProductPrice.objects.all())
    type = TypePriceSerializer(read_only=True)
    created = serializers.DateTimeField()

    class Meta:
        model = ProductPrice
        fields = ['id', 'price', 'producto', 'type', 'created']
