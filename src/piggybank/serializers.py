from django.db import models
from django.db.models.query import QuerySet
from rest_framework import serializers

from .models import Category, Currency, Transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'code', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


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

    class Meta:
        model = Transaction
        fields = (
            "amount",
            "currency",
            "date",
            "description",
            "category",
        )


class ReadTransactionSerializer(serializers.ModelSerializer):
    # Show the currenct object instead of id
    currency = CurrencySerializer()
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "currency",
            "date",
            "description",
            "category",
        )
        read_only_fields = fields # Speed up the code, Django just care about retrive the data