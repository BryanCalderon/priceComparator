from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .common import storeCrawler
from .models import Product, Store, User
from .serializer import ProductsSerializer, StoreSerializer, UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

    @action(detail=False, methods=['get'], url_path='by_user/(?P<user_pk>[^/.]+)')
    def get_by_user(self, request, user_pk=None):
        ps = Product.objects.filter(user=user_pk, status=True)
        serializer = ProductsSerializer(ps, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='search/(?P<filter_pk>[^/.]+)')
    def search_products(self, request, filter_pk=None):
        stores = Store.objects.filter(status=True)
        store_serializer = StoreSerializer(stores, many=True)
        post_list = []
        for store in store_serializer.data:
            crawler_class = storeCrawler.get_product_page_store(store['crawler'])
            data = crawler_class().search_products(search=filter_pk)
            post_list.append({'store': store['name'], 'data': ProductsSerializer(data, many=True).data})
        return JsonResponse(post_list, content_type="application/json", safe=False)

    @action(detail=False, methods=['get'], url_path='(?P<pk>[^/.]+)/search_and_save/(?P<filter_pk>[^/.]+)')
    def search_and_save(self, request, pk=None, filter_pk=None):
        stores = Store.objects.filter(status=True)
        store_serializer = StoreSerializer(stores, many=True)
        product_parent = Product.objects.filter(id=pk).first()
        post_list = []
        for store in store_serializer.data:
            crawler_class = storeCrawler.get_product_page_store(store['crawler'])
            data = crawler_class().search_products(search=filter_pk)
            products = ProductsSerializer(data, many=True).data
            for prod in products:
                product_existente: Product = Product.objects.filter(store=store['id'], sku=prod['sku']).first()
                if product_existente:
                    product_existente.price = prod['price']
                    product_existente.normal_price = prod['normal_price']
                    product_existente.offer_price = prod['offer_price']
                    product_existente.url = prod['url']
                    product_existente.model = prod['model']
                    if product_existente.related_to is None:
                        product_existente.related_to = product_parent
                    if product_existente.store is None:
                        product_existente.store = Store(**store)
                    product_existente.save()
                else:
                    child = Product(**prod)
                    child.related_to = product_parent
                    child.store = Store(**store)
                    child.save()

            post_list.append({'store': store['name'], 'data': products})
        return JsonResponse(post_list, content_type="application/json", safe=False)


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
