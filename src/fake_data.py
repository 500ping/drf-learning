# Clean db before using this
# python manage.py flush
# python manage.py shell < fake_date.py

from django.utils import timezone
import random
from piggybank.models import Currency, Transaction, Category
from django.contrib.auth.models import User
from decimal import Decimal

# Create user
# Superuser
user = User.objects.create_user('500ping', password='Cacto_123')
user.is_superuser=True
user.is_staff=True
user.save()
# Normal user
user = User.objects.create_user('test', password='Cacto_123')
user.is_staff=True
user.save()

users = list(User.objects.all())

# Create currency
Currency.objects.bulk_create([
    Currency(code="VND", name="Việt Nam đồng"),
    Currency(code="USD", name="United State Dollar"),
    Currency(code="EUR", name="Euro"),
])

# Create Category
Category.objects.bulk_create([
    Category(user=random.choice(users), name="Pets"),
    Category(user=random.choice(users), name="Hobby"),
    Category(user=random.choice(users), name="Home"),
])

# Create Transactions
txs = []
currencies = list(Currency.objects.all())
# categories = list(Category.objects.all())

for i in range(1000):
    user = random.choice(users)
    categories = list(Category.objects.filter(user=user))
    tx = Transaction(user=user, amount=random.randrange(Decimal(1), Decimal(1000)), currency=random.choice(currencies), date=timezone.now() - timezone.timedelta(days=random.randint(1, 365)), description="", category=random.choice(categories))
    txs.append(tx)

Transaction.objects.bulk_create(txs)

print(Transaction.objects.count())






