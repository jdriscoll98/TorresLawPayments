import datetime


from .models import Reminder, Client

def get_clients(low, high):
    today = datetime.date.today()
    current_clients = []
    for client in Client.objects.all():
        if (client.next_payment_date - today).days <= high and (client.next_payment_date - today).days > low:
            current_clients.append(client)
    return current_clients

def get_total(clients):
    total = 0
    for client in clients:
        total += client.total_amount_due
    return total
