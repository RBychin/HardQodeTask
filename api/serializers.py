from django.db.models import Sum
from rest_framework import serializers

from core.models import Product, Lesson, UserLesson, CustomUser


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели Уроков, с репрезентацией и
    добавлением полей последней даты просмотра и временем просмотра Урока"""
    is_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ['name', 'link', 'duration', 'is_viewed']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context.get('request').user
        data = instance.statistic.all()
        for obj in data:
            lesson = UserLesson.objects.filter(user=user, lesson=obj.lesson).last()
            if lesson:
                rep['viewed_duration'] = lesson.viewed_duration
                rep['last_view_date'] = lesson.last_view_date
        return rep

    def get_is_viewed(self, obj):
        lesson = UserLesson.objects.filter(
            user=self.context.get('request').user,
            lesson=obj).last()
        percent = 0
        if lesson:
            view_duration = lesson.viewed_duration
            lesson_duration = obj.duration
            percent = int((view_duration / lesson_duration) * 100)
            lesson.is_viewed = True
            lesson.save()
        return percent >= 80


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор Продуктов со списком Уроков."""
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'lessons']


class ProductStatSerializer(serializers.ModelSerializer):
    """Сериализатор статистических данных о каждом продукте."""
    views_count = serializers.SerializerMethodField()
    views_spend_time = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    conversion = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'views_count',
                  'views_spend_time', 'students_count',
                  'conversion']

    def get_views_count(self, obj):
        return obj.lessons.filter(statistic__is_viewed=True).count()

    def get_views_spend_time(self, obj):
        data = obj.lessons.all().aggregate(
            views_spend_time=Sum('statistic__viewed_duration')
        )
        return data['views_spend_time'] if data['views_spend_time'] else 0

    def get_students_count(self, obj):
        return CustomUser.objects.filter(products=obj).count()

    def get_conversion(self, obj):
        resource_student_count = UserLesson.objects.filter(
            lesson__product=obj
        ).values('user').distinct().count()
        platform_users_count = CustomUser.objects.all().count()
        return round(resource_student_count / platform_users_count, 2)
