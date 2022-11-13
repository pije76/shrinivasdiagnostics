from django.urls import path, re_path

from .views import *

app_name='order'

urlpatterns = [
    # path('', my_orders, name='my_orders'),
    path('', order_payment, name='order_payment'),
]
