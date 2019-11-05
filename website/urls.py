from django.conf.urls import url

from .views import *

# Application Routes (URLs)


app_name = 'website'

urlpatterns = [

    # Home Page
    url(r'^$', HomePageView.as_view(), name='home_page'),

    # Profile Page
    url(r'^dashboard$', DashboardView.as_view(), name='dashboard'),
]
