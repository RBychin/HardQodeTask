from django.contrib.auth.models import AbstractUser
from django.db import models

from project.settings import MAX_LENGTH


class CustomUser(AbstractUser):
    """Абстрактная модель пользователя, которая добавляет
    поле Продукта со связью М2М."""
    products = models.ManyToManyField(
        'Product', related_name='users',
        blank=True
    )


class Product(models.Model):
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    name = models.CharField(
        max_length=MAX_LENGTH
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Модель Урока."""
    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    name = models.CharField(
        max_length=MAX_LENGTH
    )
    link = models.CharField(
        max_length=MAX_LENGTH
    )
    duration = models.PositiveIntegerField()
    product = models.ManyToManyField(
        Product, related_name='lessons'
    )

    def __str__(self):
        return self.name


class UserLesson(models.Model):
    """Промежуточная таблица
    для хранения информации Пользователь - Урок."""
    class Meta:
        verbose_name = 'информация'
        verbose_name_plural = 'информации'
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='lessons'
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        related_name='statistic'
    )
    viewed_duration = models.PositiveIntegerField(default=0, null=False)
    last_view_date = models.DateField(null=True, blank=True)
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.lesson}'
