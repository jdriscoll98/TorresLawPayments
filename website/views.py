import datetime
import requests
import schedule
import time
from decimal import * 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.urls import reverse
from django.shortcuts import render


from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from .models import Client
from .utils import get_payments, get_total, get_end_date, create_payment_objects
from .forms import NewClientForm

from sendsms import api
from twilio.rest import Client as TwilioClient

# Application Views


# Home Page
class HomePageView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        context = {}
        today = datetime.datetime.today()
        start_date = datetime.datetime(today.year, today.month, 1)
        end_date = datetime.datetime(today.year, today.month, get_end_date(start_date))
        payments = get_payments(start_date, end_date)
        context['payments'] = payments
        context['total'] = get_total(payments)
        context['form'] = NewClientForm()
        context['start_date'] = start_date.strftime("%b %d %Y ")
        context['end_date'] = end_date.strftime("%b %d %Y")
        return render(self.request, 'website/home_page.html', context)

    def post(self, *args, **kwargs):
        form = NewClientForm(self.request.POST)
        if form.is_valid():
            data = form.cleaned_data    
            client = Client(
                name = data["name"],
                email = data["email"],
                phone_number = data["phone_number"],
                total_amount_due = data["total_amount_due"],
                monthly_payment = data["monthly_payment"],
                first_payment_date = data["first_payment_date"]
            )
            client.save()
            create_payment_objects(client)
            return HttpResponseRedirect(reverse('website:home_page'))
        else:
            context = {}
            today = datetime.datetime.today()
            start_date = datetime.datetime(today.year, today.month, 1)
            end_date = datetime.datetime(today.year, today.month, get_end_date(start_date))
            payments = get_payments(start_date, end_date)
            context['payments'] = payments
            context['total'] = get_total(payments)
            context['form'] = NewClientForm()
            context['start_date'] = start_date.strftime("%b %d %Y ")
            context['end_date'] = end_date.strftime("%b %d %Y")
            return render(self.request, 'website/home_page.html', context)

class UpdateDates(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        data = self.request.POST
        start_date =  datetime.datetime.strptime(data.get('start-date'), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(data.get('end-date'), "%Y-%m-%d")
        payments = get_payments(start_date, end_date)
        context = {}
        context['payments'] = payments
        context['total'] = get_total(payments)
        context['form'] = NewClientForm()
        context['start_date'] = start_date.strftime("%b %d %Y ")
        context['end_date'] = end_date.strftime("%b %d %Y")
        return render(self.request, 'website/home_page.html', context)


    
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
                amount = Decimal(self.request.POST.get('amount'))
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
    send_mail(
            'Torres Law Test Email',
            'Email Notifications Working',
            'AutoReminder@TorresLawFl.com',
            ['jdriscoll98@ufl.edu'],
            fail_silently=False
        )
    api.send_sms(body='Torres Law Text Messages Working',
                    from_phone='+12055836393', to=['9548091951'])
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
    client_list = []
    for client in clients:
        if (client.next_payment_date - datetime.date.today()).days == 2:
            client_list.append(client)
    for client in client_list:
        send_mail(
            'Upcoming Payment',
            'You have an upcoming payment for Torres Law Firm \n A Fee of $25 or 10 percent of your remaining balance will be added if your payment is late',
            'AutoReminder@TorresLawFl.com',
            [client.email],
            fail_silently=False,
        )
        api.send_sms(body='This is a reminder that you have an upcoming payment for Torres Law Firm \n' +
                        'A Fee of $25 or 10 percent of your remaining balance will be added if your payment is late',
                        from_phone='+12055836393', to=[client.phone_number])
    print('sent reminders')

def start_reminders(request):
    job()
    return JsonResponse({})


