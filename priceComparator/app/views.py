from django.contrib.auth.models import User, Group
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, permissions

from .common import storeCrawler
from .models import Product
from .serializer import UserSerializer, GroupSerializer, ProductsSerializer

crawlers = ['product_page_alkosto', 'product_page_exito']


def index(request):
    return HttpResponse("Hello, world. You're at the APP index.")


def search_products(request, filter):
    post_list = []
    for crawler in crawlers:
        crawler_class = storeCrawler.get_product_page_store(crawler)
        data = crawler_class().search_products(search=filter)
        post_list.append(serializers.serialize('json', data))
    return HttpResponse(post_list, content_type="application/json")


def page(request, num):
    print(request.method)
    return JsonResponse({"page": num})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
