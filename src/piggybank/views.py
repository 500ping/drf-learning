from django.db.models import query
from django.db.models.query import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, ReadTransactionSerializer, WriteTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None # No Pagination


class CategoryModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated,]
    # queryset =  Transaction.objects.all()
    # Because query with foreign key, we should use select_related() to prefetch info from db
    # Django now just use 1 query
    # queryset =  Transaction.objects.select_related("currency", 'category', 'user')
    # serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['description']
    ordering_fields = ['amount', "date"]
    filterset_fields = ['currency__code']

    def get_queryset(self):
        return Transaction.objects.select_related("currency", 'category', 'user').filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer

    # User the shortcut in serializer class
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #     return super().perform_create(serializer)