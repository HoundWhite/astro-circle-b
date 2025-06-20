# импорты необходимых бибилиотек 
# импорт класса абстракт юзера
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
import uuid
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Создание класса юзер(наследуется от абстрактного юзера)
class User(AbstractUser):
    # поля челика Charfield тупо вид поля(текстовое)
    name = models.CharField(max_length=255)
    telephon = models.CharField(max_length=20)
    # ВНИМАНИЕЕЕ У ЕМЕЙЛА ЕМЕЙЛФИЛД, Unique- разрешение на спецсимволы в поле типа @
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True, default=None)
    
    # Указываем, что поле для входа - email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'telephon']  # Добавляем обязательные поля для createsuperuser
    
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        if not self.username:
            # Генерируем уникальный username на основе email
            self.username = f"user_{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)
    
    # возвращаем емейл как индетификационные поле
    def __str__(self):
        return self.email

# КЛАСС МОДЕЛИ ДЛЯ ТОВАРОВ
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='products/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

# КЛАСС МОДЕЛИ ДЛЯ УСЛУГ
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name