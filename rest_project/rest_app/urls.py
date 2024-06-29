from rest_framework import routers
from . import views
from django.urls import path


app_name = 'rest_app'

urlpatterns = [
    path('products/', views.product_list),
    path('product/<int:pk>/', views.product),
]