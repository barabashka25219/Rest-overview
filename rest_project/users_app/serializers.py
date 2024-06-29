
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_app.serializers import ProductSerializer
from .models import Basket, Feedback
from rest_app.models import Product


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


# Пример вложенных сериализаторов
class BasketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer()
    product = ProductSerializer()

    def create(self, validated_data):
        user_data    = validated_data['user']
        product_data = validated_data['product']
        user = User.objects.get(username=user_data['username'])
        product = Product.objects.get(name=product_data['name'])
        basket = Basket.objects.create(user=user, product=product)
        return basket
    
    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.product = validated_data.get('product', instance.product)
        instance.save()
        return instance
    

# Пример сериализатора на основе классов с вложенным представлениями:
# здесь происходит переопределение полей user и product;
# переопределить можно любое поле
class FeedbackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'product', 'grade', 'text']
        read_only_fields = ['id',]
        
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        product_data = validated_data.pop('product')
        user = User.objects.get(username=user_data['username'])
        product = Product.objects.get(name=product_data['name'])
        feedback = Feedback.objects.create(user=user, product=product, **validated_data)
        return feedback
    
    def update(self, instance, validated_data):
        '''
            instance - текущий объект модели ORM.
            validated_data - очищенные и нормализованные данные.
        '''
        instance.grade = validated_data.get('grade', instance.grade)
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        return instance
