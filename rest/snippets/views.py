from rest_framework import status
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics

# Generic mixed views based on classes
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

# Views based on classes with mixins
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
    
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin):
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.put(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# Views based on classes
# class SnippetList(APIView):
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=HTTP_201_CREATED)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

# class SnippetDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer= SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=HTTP_204_NO_CONTENT)

# Functional views
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=HTTP_201_CREATED)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     try:
#         snippet = Snippet.objects.get(id=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=HTTP_204_NO_CONTENT)
    
# Decorator api_view and objects "Request", "Response" may handle more 
# than one data format automatically.
# Requests already are not bound to specified data format.
#
# Examples:
# 
# http http://127.0.0.1:8000/snippets/
#
# http http://127.0.0.1:8000/snippets/ Accept:application/json - get data in JSON format
#
# http http://127.0.0.1:8000/snippets/ Accept:text/html - get data in html format
#
# http http://127.0.0.1:8000/snippets.json  # JSON suffix
#
# http http://127.0.0.1:8000/snippets.api   # Browsable API suffix
#
# http --json POST http://127.0.0.1:8000/snippets/ code="print(456)" # send POST request with JSON payload