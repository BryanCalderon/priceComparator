from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('search/<str:filter>/', views.search_products),
    path('hola/page/<int:num>/', views.page),
]
