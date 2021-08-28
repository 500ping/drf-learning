from django.db import models
from rest_framework import serializers

from .models import Category, Currency, Transaction
from users.serializers import ReadUserSerializer
from .reports import ReportParams


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'code', 'name')


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ('id', 'name', 'user',)


# class TransactionSerializer(serializers.ModelSerializer):
#     # Show code of the currency instead of id
#     currency = serializers.SlugRelatedField(slug_field="code", queryset=Currency.objects.all())

#     class Meta:
#         model = Transaction
#         fields = '__all__'


class WriteTransactionSerializer(serializers.ModelSerializer):
    # Show code of the currency instead of id
    currency = serializers.SlugRelatedField(slug_field="code", queryset=Currency.objects.all())
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Transaction
        fields = (
            "amount",
            "currency",
            "date",
            "description",
            "category",
            "user",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only accept categories which is created by current user
        user = self.context['request'].user
        self.fields['category'].queryset = user.categories.all()


class ReadTransactionSerializer(serializers.ModelSerializer):
    # Show the currenct object instead of id
    currency = CurrencySerializer()
    category = CategorySerializer()
    user = ReadUserSerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "currency",
            "date",
            "description",
            "category",
            "user",
        )
        read_only_fields = fields # Speed up the code, Django just care about retrive the data


class ReportEntrySerializer(serializers.Serializer):
    category = CategorySerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class ReportParamsSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return ReportParams(**validated_data)