from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
import datetime
# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    first_payment_date = models.DateField(auto_now=False, auto_now_add=False, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("website:home_page")

class Payment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=False, auto_now_add=False, blank=True)

    def __str__(self):
        return str(self.client) + ' | ' +  self.payment_amount + ' | ' + self.payment_date


    

    
class Reminder(models.Model):
    in_progress = models.BooleanField(default=False)

    def __str__(self):
        return "Sending Reminders: {}".format(self.in_progress)
