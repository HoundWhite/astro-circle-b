from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
from .models import *
from django.contrib.auth import authenticate
import uuid

# КЛАСС СЕРИАЛИЗАЦИИ ДАННЫХ ПОЛЬЗОВАТЕЛЯ
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'telephon', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'telephon': {'required': True},
            'username': {'required': False}  # Делаем необязательным
        }

    def create(self, validated_data):
        # Хеширование пароля
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

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