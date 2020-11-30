from datetime import datetime

import dateutil.parser
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .common import importerStoreCrawler
from .models import Product, Store, User, TypePrice, ProductPrice
from .serializer import ProductsSerializer, StoreSerializer, UserSerializer, TypePriceSerializer, ProductPriceSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

    @action(detail=False, methods=['get'], url_path='by_user/(?P<user_pk>[^/.]+)')
    def get_by_user(self, request, user_pk=None):
        ps = Product.objects.filter(user=user_pk, status=True).order_by("creation_date")
        serializer = ProductsSerializer(ps, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search/(?P<filter_pk>[^/.]+)')
    def search_products(self, request, filter_pk=None):
        stores = Store.objects.filter(status=True)
        store_serializer = StoreSerializer(stores, many=True)
        post_list = []
        for store in store_serializer.data:
            crawler_class = importerStoreCrawler.get_product_list_class(store['name'])
            data = crawler_class().search_products(search=filter_pk)
            post_list.append({'store': store['name'], 'data': ProductsSerializer(data, many=True).data})
        return JsonResponse(post_list, safe=False)

    @action(detail=False, methods=['get'], url_path='(?P<pk>[^/.]+)/find_related')
    def find_related(self, request, pk=None):
        main_product: Product = Product.objects.filter(id=pk).first()
        main_product.save(update_fields=['updated_date'])
        products_serializer = ProductsSerializer(Product.objects.filter(related_to=pk), many=True, context={'request': request}).data
        list_products = []
        if products_serializer:
            for product in products_serializer:
                if dateutil.parser.isoparse(product['updated_date']).day < datetime.today().day:
                    product['store'] = Store(**product['store'])
                    product['related_to'] = main_product
                    child = Product(**product)
                    crawler_class = importerStoreCrawler.get_product_page_class(child.store.name)
                    crawler_class().extract_product(child)
                    child.refresh_from_db()
                    if child.normal_price:
                        ProductPrice(producto=child, price=child.normal_price, type=TypePrice(id=1)).save()
                    if child.offer_price:
                        ProductPrice(producto=child, price=child.offer_price, type=TypePrice(id=2)).save()
                    dict_obj = model_to_dict(child)
                    dict_obj['store'] = child.store.name
                    list_products.append(dict_obj)
                else:
                    product['store'] = product['store']['name']
                    list_products.append(product)
        else:
            stores = Store.objects.filter(status=True)
            store_serializer = StoreSerializer(stores, many=True).data
            for store in store_serializer:
                crawler_class = importerStoreCrawler.get_product_list_class(store['name'])
                data = crawler_class().search_products(search=main_product.sku)
                products = ProductsSerializer(data, many=True).data
                if not products:
                    data = crawler_class().search_products(search=main_product.name)
                    products = ProductsSerializer(data, many=True).data

                store_instance = Store(**store)

                for item in products:
                    item['store'] = store_instance
                    item['related_to'] = main_product
                    product_instance = Product(**item)
                    product_instance.save()
                    product_instance.refresh_from_db()
                    if product_instance.normal_price:
                        ProductPrice(producto=product_instance, price=product_instance.normal_price,
                                     type=TypePrice(id=1)).save()
                    if product_instance.offer_price:
                        ProductPrice(producto=product_instance, price=product_instance.offer_price,
                                     type=TypePrice(id=2)).save()
                    dict_obj = model_to_dict(product_instance)
                    dict_obj['store'] = product_instance.store.name
                    list_products.append(dict_obj)

        list_products.sort(key=lambda x: x.get('price'))
        return JsonResponse(list_products, safe=False)


class StoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Stores to be viewed or edited.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], url_path='by_uid/(?P<uid_pk>[^/.]+)')
    def by_uid(self, request, uid_pk):
        client = User.objects.filter(uid=uid_pk).first()
        if client:
            serializer = UserSerializer(client, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'message': 'Client with UID {} not found'.format(uid_pk)},
                            status=status.HTTP_404_NOT_FOUND)


class TypePriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TypePrices to be viewed or edited.
    """
    queryset = TypePrice.objects.all()
    serializer_class = TypePriceSerializer


class ProductPriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TypePrices to be viewed or edited.
    """
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer

    @action(detail=False, methods=['get'], url_path='by_parent/(?P<id_pk>[^/.]+)')
    def by_parent(self, request, id_pk):
        types = TypePriceSerializer(TypePrice.objects.all(), many=True, context={'request': request}).data
        result = []

        for item_type in types:
            prices: [] = ProductPriceSerializer(ProductPrice.objects.filter(producto=id_pk, type=item_type['id']), many=True, context={'request': request}).data
            if prices:
                result.append({
                    'serie': item_type['descripcion'],
                    'datos': list(map(lambda x: x['price'], prices)),
                    'label': list(map(lambda x: x['created'], prices))
                })
        return JsonResponse(result, safe=False)
