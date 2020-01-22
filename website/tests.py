from django.test import TestCase
from django.apps import apps
from website.apps import WebsiteConfig
from django.test import Client

from django.contrib.auth.models import User

import datetime

from .utils import get_end_date, get_payments, create_payment_objects, get_total
from .forms import NewClientForm
from .models import Client as LawCLient

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
        self.law_client = LawCLient.objects.create(
            name = 'test',
            email = 'test@gmail.com',
            phone_number = '0000000000',
            total_amount_due = 1000,
            monthly_payment = 100,
            first_payment_date = start_date
        )
        create_payment_objects(self.law_client)

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

    def test_create_client_pass(self):
        response = self.testClient.post('/', data={
            'name': 'newClient', 
            'email': 'newClient@gmail.com',
            'phone_number': '9548091951',
            'total_amount_due': 1000,
            'monthly_payment': 100,
            'first_payment_date': datetime.datetime(2020, 1, 31)
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LawCLient.objects.get(name='newClient').name, 'newClient')


