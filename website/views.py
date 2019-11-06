from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .forms import PaymentForm
from .models import Client

# Application Views


# Home Page
class HomePageView(LoginRequiredMixin, CreateView):
    template_name = 'website/home_page.html'
    model =  Client
    fields = (
        'name', 'email', 'phone_number', 'total_amount_due', 'payment_amount', 'next_payment_date'
    )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"] =  Client.objects.filter(paid=False)
        return context
        

