import datetime
import math
from dateutil.relativedelta import relativedelta


from .models import Client, Payment
from django.db.models import Q


def get_payments(start_date, end_date):
    payments = Payment.objects.filter(Q(date__gte=start_date) & Q(date__lte=end_date))
    return payments

def get_total(payments):
    return sum([payment.amount for payment in payments])

def get_end_date(start_date):
    if start_date.month % 2 != 0:
        return 31
    elif start_date.month == 2:
        return 28
    else:
        return 30

def create_payment_objects(client):
    months = math.ceil(client.total_amount_due /client.monthly_payment)
    date = client.first_payment_date
    for i in range(months):
        new_payment = Payment.objects.create(client=client, amount= client.monthly_payment,
                                            date=date)
        date = date + relativedelta(months=+1)
        new_payment.save()
    
