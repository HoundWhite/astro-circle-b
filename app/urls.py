from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegApiView.as_view()),
    path('login/', AuthApiView.as_view()),
    path('user-profile/', UserProfileView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
] 