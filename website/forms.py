from django import forms
    
class NewClientForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=254)
    phone_number = forms.CharField(max_length=17, blank=True) # validators should be a list
    total_amount_due = forms.DecimalField(max_digits=10, decimal_places=2)
    monthly_payment = forms.DecimalField(max_digits=10, decimal_places=2)
    first_payment_date = forms.DateField(auto_now=False, auto_now_add=False, blank=True)
