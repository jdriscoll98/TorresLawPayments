from django import forms
from phonenumber_field.formfields import PhoneNumberField
    
class NewClientForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=254)
    phone_number = PhoneNumberField() # validators should be a list
    monthly_payment = forms.DecimalField(max_digits=10, decimal_places=2)
    total_amount_due = forms.DecimalField(max_digits=10, decimal_places=2)
    admin_fee = forms.DecimalField(max_digits=10, decimal_places=2)
    first_payment_date = forms.DateField(required=False)

    
    def clean_monthly_payment(self):
        monthly_payment = self.cleaned_data['monthly_payment']

        if monthly_payment < 0:
            raise forms.ValidationError("Please enter a positive value")
        return monthly_payment

    def clean_total_amount_due(self):
        total_amount_due = self.cleaned_data['total_amount_due']
        if total_amount_due < 0:
            raise forms.ValidationError("Please enter a positive value")
        return total_amount_due


    # def clean_phone_number(self, form):
    #     data = self.cleaned_data['phone_number']
    #     if "fred@example.com" not in data:
    #         raise forms.ValidationError("You have forgotten about Fred!")

    #     # Always return a value to use as the new cleaned data, even if
    #     # this method didn't change it.
    #     return data

