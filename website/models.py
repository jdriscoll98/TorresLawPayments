from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    phone_number = PhoneNumberField()
    total_amount_due = models.DecimalField(max_digits=5, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=5, decimal_places=2)
    next_payment_date = models.DateField(auto_now=False, auto_now_add=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("website:home_page")
    
