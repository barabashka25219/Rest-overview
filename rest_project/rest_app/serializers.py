'''
    С помощью сериализаторов можно трансформировать любой 
    python-объект в требуемый формат.

    Сериализаторы поддерживают следующие функции:
    - валидация переданных данных (валидация поля/всех полей);
    - создание и обновление записей в БД;

    После сериализации входные данные нужно проверить методом is_valid():
    он проверяет корректность данных и нормализует их.
    При возникновении ошибок метод is_valid() возвращает False, а свойство
    .errors содержит список ошибок.

    Для сохранения или обновления данных БД сериализатору требуются реализация
    методов: 
        - create(self, data);
        - update(self, instance, data)

    При обновлении данных требуется передавать словарь из всех полей, иначе возникает исключение
    ErrorDetail из-за отсутствия поля. 
    Для частичного обновления данных существует флаг partial, из-за чего исключение не возникает:
        serializer = ProductSerializer(product, data=data, partial=True)
'''

from rest_framework import serializers
from .models import Product, Basket, Feedback
from django.contrib.auth.models import User

# Сериализаторы на основе класса Serializer
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)                            
    description = serializers.CharField(max_length=2048, allow_blank=True)
    price = serializers.IntegerField(default=0)

    # Объвление пользовательской валидации по всем полям:
    # закоментировано, поскольку мешает работе метода is_valid();
    # использовалось для демонастрации
    # can_be_selled = serializers.BooleanField(required=False)

    # def validate(self, data):
    #     if data['can_be_selled'] is not True:
    #         raise serializers.ValidationError("Iphones must be selled!")
    #     return data

    # Объявление пользовательской валидации по одному полю
    # имя метода обязательно начинается с validate_{имя поля}
    def validate_price(self, value):
        if value < 100:
            raise serializers.ValidationError("Price can't be less than $100")

    # Метод create() используется неявно при вызове метода save()
    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    # Метод update() используется неявно при инициализации сериализатора
    # с экземпляром модели и данными
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.desciprion = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data.pop('username'))
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
    serializers.IntegerField(read_only=True)
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Feedback
        fields = ['user', 'product', 'grade', 'text']
        read_only_fields = ['id',]
        

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        product_data = validated_data.pop('product')
        user = User.objects.get(username=user_data['username'])
        product = Product.objects.get(name=product_data['name'])
        feedback = Feedback.objects.create(user=user, product=product, **validated_data)
        return feedback