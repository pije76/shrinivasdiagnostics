from django.urls import path, re_path

from .views import *

app_name='order'

urlpatterns = [
    path('', checkout, name='checkout'),
    path('callback/', callback, name='callback'),
    # path('paymenthandler/', paymenthandler, name='paymenthandler'),
]
