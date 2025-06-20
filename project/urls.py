"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import UserListView, RegApiView, AuthApiView, UserProfileView, AdminUserListView

urlpatterns = [
    path('admin-api/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/', admin.site.urls),
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', RegApiView.as_view(), name='register'),
    path('login/', AuthApiView.as_view(), name='login'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include('app.urls')),  # Включаем все URL-маршруты из приложения app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
