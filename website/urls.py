from django.conf.urls import url

from .views import *

# Application Routes (URLs)


app_name = 'website'

urlpatterns = [

    # Home Page
    url(r'^$', HomePageView.as_view(), name='home_page'),
    url(r'^make-payment/$', MakePayment.as_view(), name='make_payment'),
    url(r'^send-reminders/$', SendUpcomingPayment.as_view(), name='send_reminders'),
    url(r'^send-late-reminders/$', SendLatePayment.as_view(), name='send_late'),

    # Profile Page
]
