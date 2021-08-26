from django.db.models import query
from django.db.models.query import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, ReadTransactionSerializer, WriteTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None # No Pagination


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionModelViewSet(ModelViewSet):
    # queryset =  Transaction.objects.all()
    # Because query with foreign key, we should use select_related() to prefetch info from db
    # Django now just use 1 query
    queryset =  Transaction.objects.select_related("currency", 'category')
    # serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['description']
    ordering_fields = ['amount', "date"]
    filterset_fields = ['currency__code']

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer