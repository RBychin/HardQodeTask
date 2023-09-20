from django.urls import path, include
from rest_framework import routers

from api.views import ProductViewSet, ProductStatViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('stats', ProductStatViewSet, basename='stats')

urlpatterns = [path('', include(router.urls))]
