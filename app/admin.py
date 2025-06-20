from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product
from django.utils.html import format_html

# регаем пользователя админ панели
@admin.register(User)
class CustUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'password', 'telephon')
    search_fields = ('email', 'password', 'telephon')

# регистрируем модель товаров
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'display_image', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Нет изображения"
    display_image.short_description = 'Изображение'