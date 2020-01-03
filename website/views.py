import datetime
import requests
import schedule
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.urls import reverse


from django.http import JsonResponse, HttpResponse

from .models import Client, Reminder
from .utils import get_clients, get_total

from sendsms import api
from twilio.rest import Client as TwilioClient

# Application Views


# Home Page
class HomePageView(LoginRequiredMixin, CreateView):
    template_name = 'website/home_page.html'
    model =  Client
    fields = (
        'name', 'email', 'phone_number', 'total_amount_due', 'payment_amount'
    )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = get_clients(-365, 30)
        next_clients = get_clients(30, 60)
        next_3_clients = get_clients(60, 90)
        context['clients'] = clients
        context['total'] = get_total(clients)
        context['next_total'] = get_total(next_clients)
        context['3_total'] = get_total(next_3_clients)
        context['sending'] = Reminder.objects.get(pk=1).in_progress
        return context
    
class UpdateClient(LoginRequiredMixin, UpdateView):
    template_name = 'website/edit_client.html'
    model = Client
    fields = '__all__'
        
class MakePayment(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        if self.request.is_ajax:
            data = {
                'success': False
            }
            try:
                client = Client.objects.get(pk=self.request.POST.get('pk'))
                amount = int(self.request.POST.get('amount'))
                client.total_amount_due -= amount
                if client.total_amount_due <= 0:
                    client.delete()
                    data['success'] = True
                    return JsonResponse(data)
                date = client.next_payment_date
                if date.month == 12:
                    year = date.year + 1
                    month = 1
                else:
                    year = date.year
                    month = date.month + 1
                client.next_payment_date = datetime.date(year, month, 15)
                client.save()
                data['success'] = True
            except Exception as e:
                print(e)
            return JsonResponse(data)

class MonthDetail(LoginRequiredMixin, TemplateView):
    template_name = 'website/month_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        clients = get_clients(int(kwargs.get('low')), int(kwargs.get('high')))
        context['clients'] = clients
        context['total'] = get_total(clients)
        return context



def job():
    clients = Client.objects.all()
    client_list = []
    for client in clients:
        if (client.next_payment_date - datetime.date.today()).days <= -2:
            client_list.append(client)
    for client in client_list:
        send_mail(
            'Late Payment',
            'This is a reminder that you missed a payment to Torres Law Firm \n' +
            'A Fee of $25 or 10 percent of your remaining balance will be added',
            'AutoReminder@TorresLawFl.com',
            [client.email],
            fail_silently=False
        )
        api.send_sms(body='This is a reminder that you missed a payment to Torres Law Firm \n' +
                        'A Fee of $25 or 10 percent of your remaining balance will be added',
                        from_phone='+12055836393', to=[client.phone_number])
    for client in clients:
        if (client.next_payment_date - datetime.date.today()).days == 2:
            client_list.append(client)
    for client in client_list:
        send_mail(
            'Upcoming Payment',
            'You have an upcoming payment for Torres Law Firm',
            'AutoReminder@TorresLawFl.com',
            [client.email],
            fail_silently=False,
        )
        api.send_sms(body='TEST MESSAGE',
                     from_phone='+12055836393', to=[client.phone_number])
    print('sent reminders')



    

def start_reminders(request):
    schedule.every(2).days.at('9:00').do(job).tag('reminders')
    reminder = Reminder.objects.get(pk=1)
    reminder.in_progress = True
    reminder.save()
    while True:
        schedule.run_pending()
    return JsonResponse({})

def stop_reminders(request):
    schedule.clear('reminders')
    reminder = Reminder.objects.get(pk=1)
    reminder.in_progress = False
    reminder.save()
    return JsonResponse({})
