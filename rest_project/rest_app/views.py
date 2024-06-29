'''
    Есть три способа использования представлений:
    1) Представление на основе декоратора api_view
    2) Представление на основе класса APIView
    3) Представление на основе класса с использованием миксинов;
    4) Использование уже готовых представлений, реализующих общие паттерны (вернуть список, обновить объект и т.п.)
    
    - Декоратор api_view и класс APIView предоставляют возможность использования
    объектов Request и Response, являющиеся расширением объектов HttpRequest/HttpResponse. 
    Они позволяют определить тип входящих данных по заголовку Content-Type, тип исходящих данных
    по заголовку Accept и сериализовать их в требуемый формат.


'''


from django.shortcuts import get_object_or_404
from rest_framework import decorators
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_app.models import Product
from rest_app.serializers import ProductSerializer

# Функциональные представления с использованием декоратора 
# api_view
# Для указания используемых парсеров и рендереров используются
# соответствующие декораторы
@decorators.api_view(['GET', 'POST'])
@decorators.parser_classes([JSONParser,])
@decorators.renderer_classes([JSONRenderer,])
def product_list(request, format=None):
    if request.method == 'GET':
        products_db = Product.objects.all()
        serializer = ProductSerializer(products_db, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@decorators.api_view(['GET', 'PUT', 'DELETE'])
@decorators.parser_classes([JSONParser,])
@decorators.renderer_classes([JSONRenderer,])
def product(request, pk, format=None):
    product = get_object_or_404(Product, id=pk)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)