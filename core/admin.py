from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from core.models import Product, Lesson, UserLesson

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = (
        ('Main Information', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Products Access', {
            'fields': ('products',)
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'is_active')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson']