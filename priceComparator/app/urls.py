from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('hola/<str:nombre>/', views.hola),
]
