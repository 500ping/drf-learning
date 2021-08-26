from django.urls import path
from rest_framework import routers

from .views import CurrencyListAPIView, CategoryModelViewSet, TransactionModelViewSet

router = routers.SimpleRouter()
router.register(r'categories', CategoryModelViewSet, basename='category')
router.register(r'transactions', TransactionModelViewSet, basename='transaction')

urlpatterns = [
    path("currencies/", CurrencyListAPIView.as_view(), name='currencies'),
] + router.urls
