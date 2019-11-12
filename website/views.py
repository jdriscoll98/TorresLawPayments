import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import View

from twilio.twiml.messaging_response import messaging_response
from django_twilio.decorators import twilio_view

from django.http import JsonResponse, HttpResponse

from .models import Client

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
        email_list = []
        for client in clients:
            if (client.next_payment_date - datetime.date.today()).days == 2:
                email_list.append(client.email)
        
        send_mail(
            'Upcoming Payment', 
            'You have an upcoming payment for Torres Law Firm', 
            'AutoReminder@TorresLawFl.com',
            email_list,
            fail_silently=False,
        )
        twiml = '<Response><Message>Hello from your Django app!</Message></Response>'
        return HttpResponse(twiml, content_type='text/xml')

class SendLatePayment(View):
    def get(self, *args, **kwargs):
        clients = Client.objects.all()
        email_list = []
        for client in clients:
            if (client.next_payment_date - datetime.date.today()).days <= -2:
                email_list.append(client.email)
        send_mail(
            'Late Payment',
            'This is a reminder that you missed a payment to Torres Law Firm \n' + 
            'A Fee of $25 or 10 percent of your remaining balance will be added',
            'AutoReminder@TorresLawFl.com',
            email_list,
            fail_silently=False
        )
        return HttpResponse()
