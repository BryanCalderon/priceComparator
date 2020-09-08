from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponse
# Create your views here.
from rest_framework import viewsets, permissions

from .serializer import UserSerializer, GroupSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the APP index.")


def hola(request, nombre):
    print(request.method)
    return HttpResponse(str.format("HOLA {}!!!!!", nombre))


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
