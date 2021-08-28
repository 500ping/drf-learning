from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime

from .models import Category, Transaction


@dataclass
class ReportEntry:
    category: Category
    total: Decimal
    count: int
    avg: Decimal
    

@dataclass
class ReportParams:
    start_date: datetime
    end_date: datetime
    user: User


def transaction_report(params: ReportParams):
    data = []
    queryset = Transaction.objects.filter(
        user=params.user,
        date__gte=params.start_date,
        date__lte=params.end_date,
    ).values('category').annotate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount'),
    )

    # Get all categories and save into a dict --> better performance
    categories_index = {}
    for category in Category.objects.filter(user=params.user):
        categories_index[category.pk] = category

    for entry in queryset:
        # category = Category.objects.get(pk=entry['category']) # this way, each entry will excute one query --> low performance 
        category = categories_index.get(entry['category'])
        report_entry = ReportEntry(
            category,
            entry['total'],
            entry['count'],
            entry['avg'],
        )
        data.append(report_entry)
    return data