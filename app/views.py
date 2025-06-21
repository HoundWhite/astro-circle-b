from django.shortcuts import render
import json
# ИМПОРТЫ БЕСКОНЕЧНЫЕ НА ПРЕДСТАВЛЕНИЯ(((((((((((((
from rest_framework import generics, status, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import IsAdminUser
import logging

logger = logging.getLogger(__name__)

# генерик это модуль который содержит штуки для создания представлений
# API endpoint для просмотра списка всех пользователей.
# Доступ только для администраторов.
class AdminUserListView(generics.ListAPIView):
    # работа с БД где мы берем все записи в таблицу юзера
    queryset = User.objects.all()
    # вызываем предыдущий сериализатор данных
    serializer_class = UserSerializer
    # права доступа юзер является админом или нет
    permission_classes = [IsAdminUser]

    

    # представление на создание списка пользователей
class UserListView(generics.ListCreateAPIView):
    # работа с БД где мы берем все записи в таблицу юзера
    queryset = User.objects.all()
    # вызываем предыдущий сериализатор данных
    serializer_class = UserSerializer


# РЕГА РЕГА
class RegApiView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        try:
            logger.info(f"Registration attempt with data: {request.data}")
            
            # Принудительно парсим JSON, если DRF не сделал это автоматически
            if not isinstance(request.data, dict):
                try:
                    data = json.loads(request.body.decode('utf-8'))
                    request._full_data = data  # Переопределяем данные
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                    raise exceptions.ParseError("Invalid JSON")

            logger.info(f"Raw data: {request.body.decode('utf-8')}")
            logger.info(f"Parsed data: {request.data}")
            
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error(f"Serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()
            token = Token.objects.create(user=user)
            
            logger.info(f"User {user.email} registered successfully")
            
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'name': user.name,
                'telephon': user.telephon  # Убедитесь, что поле в модели названо так же
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(f"Registration failed: {str(e)}")  # Запишет полный traceback
            return Response(
                {"error": "Internal Server Error", "details": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



# АУФ АУНТЕФИКАЦИЯ
# Создаётся сериализатор (self.serializer_class), в который передаются:
# data=request.data (логин и пароль из запроса)
# context={'request': request} (контекст запроса для дополнительной проверки)
class AuthApiView(APIView):
    authentication_classes = []  # Отключаем аутентификацию для входа
    permission_classes = []     # Разрешаем доступ без проверки прав
    
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email,
                'name': user.name,
                'telephon': user.telephon
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

# представление на личный кабинет
# выдается только челу у которого есть токен, ну и проверка зареган или залогинен
class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            logger.info(f"Fetching profile for user: {request.user.email}")
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching user profile: {str(e)}")
            return Response({
                'error': 'Ошибка при получении данных профиля'
            }, status=status.HTTP_400_BAD_REQUEST)

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []  # Отключаем аутентификацию
    permission_classes = []     # Разрешаем доступ без проверки прав

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []  # Отключаем аутентификацию
    permission_classes = []     # Разрешаем доступ без проверки прав

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context