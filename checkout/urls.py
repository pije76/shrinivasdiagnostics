from django.urls import path, re_path

from .views import *

app_name='checkout'

urlpatterns = [
    path('', checkout, name='checkout'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
    path('add/', update_billingaddress, name='update_billingaddress'),
    path('update/', update_billingaddress, name='update_billingaddress'),
]
