import datetime
import requests
import schedule
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.urls import reverse


from django.http import JsonResponse, HttpResponse

from .models import Client

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
        context["clients"] =  Client.objects.all()
        total = 0
        for client in Client.objects.all():
            total += client.total_amount_due
        context['total'] = total
        return context
        
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

class SendUpcomingPayment(View):
    def get(self, *args, **kwargs):
        clients = Client.objects.all()
        client_list = []
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
        return HttpResponse()

class SendLatePayment(View):
    def get(self, *args, **kwargs):
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
        return HttpResponse()


def job():
    # requests.get(reverse('website:send_reminders'))
    # requests.get(reverse('website:send_late'))
    print('sending reminders')

schedule.every(.1).minutes.do(job).tag('reminders')


    

def start_reminders(request):
    while True:
        schedule.run_pending()
    return JsonResponse({})

def stop_reminders(request):
    schedule.clear('reminders')
    return JsonResponse({})
