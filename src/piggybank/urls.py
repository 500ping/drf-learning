from django.urls import path
from rest_framework import routers

from .views import CurrencyModelViewSet, CategoryModelViewSet, TransactionModelViewSet, TransactionReportAPIView

router = routers.SimpleRouter()
router.register(r'categories', CategoryModelViewSet, basename='category')
router.register(r'transactions', TransactionModelViewSet, basename='transaction')
router.register(r'currencies', CurrencyModelViewSet, basename='currency')

urlpatterns = [
    # path("currencies/", CurrencyListAPIView.as_view(), name='currencies'),
    path("report/", TransactionReportAPIView.as_view(), name='report'),
] + router.urls
