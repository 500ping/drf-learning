from django.urls import path
from rest_framework import routers

from .views import CurrencyListAPIView, CategoryModelViewSet

router = routers.SimpleRouter()
router.register(r'categories', CategoryModelViewSet, basename='categories')

urlpatterns = [
    path("currencies/", CurrencyListAPIView.as_view(), name='currencies'),
] + router.urls
