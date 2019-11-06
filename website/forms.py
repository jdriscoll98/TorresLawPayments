from django import forms
from phonenumber_field.formfields import PhoneNumberField

class PaymentForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=200, required=True)
    phone_number = PhoneNumberField()
    
