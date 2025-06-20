from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
from .models import *
from django.contrib.auth import authenticate
import uuid

# КЛАСС СЕРИАЛИЗАЦИИ ДАННЫХ ПОЛЬЗОВАТЕЛЯ
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    # определяем метаданные(как будет вести себя модель в программе)
    class Meta:
        # указываем модель, поля
        model = User
        fields = ['id', 'name', 'email', 'telephon', 'password']
        # ЭКСТРАКВАРГИ ШКВАРКИ
        # Это  key-word-argument сюда мы задаем шо пароль только для чтения + емейл как обязательное поле
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
            'name': {'required': True},
            'telephon': {'required': True}
        }

    def validate_telephon(self, value):
        # Проверяем формат телефона
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError('Неверный формат телефона')
        return value

    def validate_password(self, value):
        # Проверяем длину пароля
        if len(value) < 8:
            raise serializers.ValidationError('Пароль должен содержать минимум 8 символов')
        return value

# СОЗДАЕМ ЮЗЕРА С ВАЛИДАЦИЕЙ ПОЛЕЙ
    def create(self, validated_data):
        # Проверяем, существует ли пользователь с таким email
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'Пользователь с таким email уже существует'})
            
        # Generate a unique username based on email
        username = f"user_{uuid.uuid4().hex[:8]}"
        
        user = User.objects.create_user(
            username=username,  # Add username parameter
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            telephon=validated_data['telephon']
        )
        return user

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                              email=email,
                              password=password)
            if not user:
                raise serializers.ValidationError('Неверный email или пароль')
        else:
            raise serializers.ValidationError('Необходимо указать email и пароль')

        attrs['user'] = user
        return attrs

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'image_url', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None