'''
    Представления на основе класса APIView обеспечивают ту же фунцикональность,
    что и декоратор api_view для функциональный представлений HttpResponse/HttpRequest 
    до объектов Response/Request.

    В Django существуют представления на основе классов, реализующие наиболее часто
    используемые паттерны запросов (GET, POST, PUT, DELETE).
    Базовый класс - APIView. На его основе реализован класс GenericAPIView, использующий
    миксины для наследования методов create, retrive, update, ..., использующихся в 
    методах запросов. В общих чертах:

    1) APIView - базовый класс, реализующий обработку запросов в стиле Rest.
    2) GenericAPIView - базовый класс для общих классов.
    3) CreateModelMixin, ListModelMixin, RetriveModelMixin, UpdateModelMixin, DestroyModelMixin
       - миксины, реализующие методы для манипуляции  объектами модели, такие как:
        create(), list(), update(), partial_update(), retrive(), destroy()
    4) CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, 
       UpdateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetriveDestroyAPIView, 
       RetriveDestroyUpdateAPIView
       - классы-представления, наследующие вышеупомянутые миксины и реализовывающие методы
         запросов (get, post, put, delete, ...)

    Представления, основанные на использовании миксинов, позволяют реализовать
    часть функционала общих представлений, добавляя методы list, update, retrive, create, ...
'''
from django.shortcuts import render
from rest_framework import mixins
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from .serializers import BasketSerializer, FeedbackSerializer
from .models import Basket, Feedback
from rest_framework import generics


# Представление на основе класса APIView
class BasketViewList(views.APIView):
    parser_classes = [parsers.JSONParser,]
    renderer_classes = [renderers.JSONRenderer,]
    
    def get(self, request, format=None):
        baskets = Basket.objects.all()
        serializer = BasketSerializer(baskets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = BasketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Generic-представление RetrieveUpdateView
class BasketDetail(generics.RetrieveUpdateAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer


# Представления с использованием миксинов
# и класса GenericAPIView
class FeedBackViewList(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    parser_classes = [parsers.JSONParser,]          # мы можем не указывать парсеры и рендереры,
    renderer_classes = [renderers.JSONRenderer,]    # если они определены в settings.py->DEFAULT_{NAME}_CLASSES

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Представление на основе generic-класса, реализовывающего обработку
# запросов GET, PUT, DELETE и манипуляции с объектами БД (retrive, update, destroy)
# По умолчанию поиск объекта БД ведется по полю pk. Но мы можем определить иное
# поле, переопределив значение lookup_field. В примере оно будет для наглядности
# показано с тем же самым значением, что и в generic классе 
class FeedbackViewRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    lookup_field = 'pk' # для примера

    
# http POST http://127.0.0.1:8000/users/basket/ \
# product[id]=1 \
# product[name]="Iphone SE 2020" \
# product[price]:=null \
# product[description]="This is already olding device..." \
# user[id]=2 \
# user[username]="root" \
# Content-Type:application/json