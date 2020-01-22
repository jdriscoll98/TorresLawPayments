from django.test import TestCase
from django.apps import apps
from website.apps import WebsiteConfig
from django.test import Client

from django.contrib.auth.models import User
from django.urls import reverse

import datetime

from .utils import get_end_date, get_payments, create_payment_objects, get_total
from .forms import NewClientForm
from .models import Payment, Client as LawClient

# Create your tests here.
class AppTests(TestCase):
    def setUp(self):
        self.testClient = Client()
        self.testUser = User.objects.create(username='testUser')
        self.testUser.set_password('abc12345')
        self.testUser.save()
        self.testClient.login(username='testUser', password='abc12345')
        today = datetime.datetime.today()
        start_date = datetime.datetime(today.year, today.month, 1)
        self.law_client = LawClient.objects.create(
            name = 'test',
            email = 'test@gmail.com',
            phone_number = '0000000000',
            total_amount_due = 1000,
            monthly_payment = 100,
            admin_fee = 25,
            first_payment_date = start_date
        )
        create_payment_objects(self.law_client)
        self.form_data = {
            'name': 'newClient',
            'email': 'newClient@gmail.com',
            'phone_number': '9548091951',
            'total_amount_due': 1000,
            'monthly_payment': 100,
            'admin_fee': 25,
            'first_payment_date': '1/31/2020'
        }

    def test_website_config(self):
        self.assertEqual(WebsiteConfig.name, 'website')
        self.assertEqual(apps.get_app_config('website').name, 'website')

    def test_homepage_response(self):
        response = self.testClient.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_context(self):
        response = self.testClient.get('/')
        today = datetime.datetime.today()
        start_date = datetime.datetime(today.year, today.month, 1)
        end_date = datetime.datetime(
            today.year, today.month, get_end_date(start_date))
        payments = get_payments(start_date, end_date)
        self.assertEqual(
            response.context['start_date'], start_date.strftime("%b %d %Y "))
        self.assertEqual(
            response.context['end_date'], end_date.strftime("%b %d %Y")
        )
        self.assertEqual(
            list(response.context['payments']), list(payments)
        )
        self.assertEqual(response.context['total'], get_total(payments))

    def test_new_client_form(self):
        form = NewClientForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_new_client_form_bad_number(self):
        form_data = self.form_data
        form_data['phone_number'] ='954809195'
        form = NewClientForm(data=self.form_data)
        self.assertFalse(form.is_valid())
    
    def test_new_client_form_bad_monthly_payment(self):
        form_data = self.form_data
        form_data['monthly_payment'] = -1
        form = NewClientForm(data=form_data)
        self.assertEquals(form.errors['monthly_payment'], [
                          u"Please enter a positive value"])

    def test_new_client_form_bad_total_amount(self):
        form_data = self.form_data
        form_data['total_amount_due'] = -1
        form = NewClientForm(data=form_data)
        self.assertEquals(form.errors['total_amount_due'], [
                          u"Please enter a positive value"])


    def test_create_client_pass(self):
        self.testClient.post(reverse('website:home_page'), {
            'name': 'newClient', 
            'email': 'newClient@gmail.com',
            'phone_number': '9548091951',
            'total_amount_due': 1000,
            'monthly_payment': 100,
            'admin_fee': 25,
            'first_payment_date': '1/31/2020'
        })
        self.assertEqual(LawClient.objects.get(pk=2).name, 'newClient')

    def test_create_client_fail(self):
        form_data = self.form_data
        form_data['monthly_payment'] = -1 # create an intentional error
        response = self.testClient.post(reverse('website:home_page'), form_data)
        context = {}
        today = datetime.datetime.today()
        start_date = datetime.datetime(today.year, today.month, 1)
        end_date = datetime.datetime(
            today.year, today.month, get_end_date(start_date))
        payments = get_payments(start_date, end_date)
        context['payments'] = payments
        context['total'] = get_total(payments)
        context['form'] = NewClientForm()
        context['start_date'] = start_date.strftime("%b %d %Y ")
        context['end_date'] = end_date.strftime("%b %d %Y")
        self.assertEqual(
            response.context['start_date'], start_date.strftime("%b %d %Y "))
        self.assertEqual(
            response.context['end_date'], end_date.strftime("%b %d %Y")
        )
        self.assertEqual(
            list(response.context['payments']), list(payments)
        )
        self.assertEqual(response.context['total'], get_total(payments))

    def test_update_dates_post(self):
        data = {
            'start-date': '2020-2-1',
            'end-date': '2020-2-28'
        }
        response = self.testClient.post(reverse('website:update_dates'), data)
        start_date = datetime.datetime.strptime(
            data.get('start-date'), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(data.get('end-date'), "%Y-%m-%d")
        payments = get_payments(start_date, end_date)
        context = {}
        context['payments'] = payments
        context['total'] = get_total(payments)
        context['form'] = NewClientForm()
        context['start_date'] = start_date.strftime("%b %d %Y ")
        context['end_date'] = end_date.strftime("%b %d %Y")
        self.assertEqual(
            response.context['start_date'], start_date.strftime("%b %d %Y "))
        self.assertEqual(
            response.context['end_date'], end_date.strftime("%b %d %Y")
        )
        self.assertEqual(
            list(response.context['payments']), list(payments)
        )
        self.assertEqual(response.context['total'], get_total(payments))



    def test_client_absolute_url(self):
        response = self.testClient.get(self.law_client.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_payment_string(self):
        payment = Payment.objects.get(pk=1)
        self.assertEqual(str(payment), str(payment.client) + ' | ' + str(payment.amount) + ' | ' + str(payment.date))



    

    


