from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import ProductSerializer, ProductStatSerializer
from core.models import Product


class ProductViewSet(ReadOnlyModelViewSet):
    """Класс представление Продуктов,
    В сет запросов попадают только уроки продуктов к которым у пользователя
    есть доступ."""

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        user = self.request.user
        return user.products.all()


class ProductStatViewSet(ReadOnlyModelViewSet):
    """Представление статистики продуктов."""

    serializer_class = ProductStatSerializer
    queryset = Product.objects.all()
