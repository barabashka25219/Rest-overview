'''
    Есть три способа использования представлений:
    1) Представление на основе декоратора api_view
    2) Представление на основе класса APIView
    3) Представление на основе класса с использованием миксинов;
    
    Декоратор api_view и класс APIView предоставляют возможность использования
    объектов Request и Response, являющиеся расширением объектов HttpRequest/HttpResponse. 
    Они позволяют определить тип входящих данных по заголовку Content-Type, тип исходящих данных
    по заголовку Accept и сериализовать их в требуемый формат.
'''


from django.shortcuts import (
    render, get_object_or_404,
    get_list_or_404,
)
from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
)
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin,
    CreateModelMixin, UpdateModelMixin
)
from rest_framework.views import APIView
from rest_app.models import Product
from rest_app.serializers import ProductSerializer

# Функциональные представления с использованием декоратора 
# api_view
@api_view(['GET', 'POST'])
@parser_classes([JSONParser,])
@renderer_classes([JSONRenderer,])
def product_list(request, format=None):
    if request.method == 'GET':
        products_db = Product.objects.all()
        serializer = ProductSerializer(products_db, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser,])
@renderer_classes([JSONRenderer,])
def product(request, pk, format=None):
    product = get_object_or_404(Product, id=pk)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    

# Представления на основе класса APIView
class BasketViewList(APIView):
    parser_classes = [JSONParser,]
    renderer_classes = [JSONRenderer,]
    
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = ProductSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=HTTP_201_CREATED)
    
