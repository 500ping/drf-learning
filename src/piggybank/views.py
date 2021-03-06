from django.db.models import query
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, DjangoModelPermissions, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, ReadTransactionSerializer, WriteTransactionSerializer, ReportEntrySerializer, ReportParamsSerializer
from .reports import transaction_report
from .permissions import IsAdminOrReadOnly


# class CurrencyListAPIView(ListAPIView):
#     permission_classes = [AllowAny,]
#     queryset = Currency.objects.all()
#     serializer_class = CurrencySerializer
#     pagination_class = None # No Pagination
    # renderer_classes = [XMLRenderer]

class CurrencyModelViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly,]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None # No Pagination


class CategoryModelViewSet(ModelViewSet):
    # Need to regis permission to the user
    permission_classes = [DjangoModelPermissions,]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated,]
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


class TransactionReportAPIView(APIView):
    # permission_classes = [IsAuthenticated,]

    def get(self, request):
        print(request.GET)
        params_serializer = ReportParamsSerializer(data=request.GET, context={"request": request})
        params_serializer.is_valid(raise_exception=True)
        params = params_serializer.save()
        data = transaction_report(params)
        serializer = ReportEntrySerializer(instance=data, many=True)
        return Response(data=serializer.data)