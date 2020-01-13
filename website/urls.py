from django.conf.urls import url

from .views import *

# Application Routes (URLs)


app_name = 'website'

urlpatterns = [

    # Home Page
    url(r'^$', HomePageView.as_view(), name='home_page'),
    url(r'^update-dates$', UpdateDates.as_view(), name='update_dates'),
    url(r'^make-payment/$', MakePayment.as_view(), name='make_payment'),
    url(r'^update-client/month-detail/(?P<pk>\d+)$',
        UpdateClient.as_view(), name='edit_client'),
    url(r'^start-reminders/$', start_reminders, name='start_reminders'),
    url(r'^month-detail/(?P<low>\d+)/(?P<high>\d+)/$',
        MonthDetail.as_view(), name='month_detail'),

    # Profile Page
]
