from django import forms
from phonenumber_field.formfields import PhoneNumberField
    
class NewClientForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=254)
    phone_number = forms.PhoneNumberField() # validators should be a list
    total_amount_due = forms.DecimalField(max_digits=10, decimal_places=2)
    monthly_payment = forms.DecimalField(max_digits=10, decimal_places=2)
    admin_fee = forms.DecimalField(max_digits=10, decimal_places=2)
    first_payment_date = forms.DateField()

    def clean_phone_number(self)
