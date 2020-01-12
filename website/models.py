from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
import datetime
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    phone_number = PhoneNumberField()
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    first_payment_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("website:home_page")


class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=False, auto_now_add=False, blank=True)

    def __str__(self):
        return str(self.client) + ' | ' + self.payment_amount + ' | ' + self.payment_date


