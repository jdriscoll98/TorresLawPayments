import datetime


from .models import Reminder, Client, Payment
from django.db.models import Q


def get_clients(start_date, end_date):
    payments = Payment.objects.filter(Q(date__gte=start_date) & Q(date__lte=end_date))
    return [payment.client for payment in payments]

def get_total(start_date, end_date):
    payments = Payment.objects.filter(Q(date__gte=start_date) & Q(date__lte=end_date))
    return sum([payment.amount for payment in payments])

def get_end_date(start_date):
    if start_date.month % 2 != 0:
        return 31
    elif start_date.month == 2:
        return 28
    else:
        return 30
