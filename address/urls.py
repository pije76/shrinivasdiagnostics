from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.urls import path, re_path, include
from django.views.generic import RedirectView

from .views import *
from . import views

app_name = 'address'

urlpatterns = [
    path('add/', create_billingaddress, name='create_billingaddress'),
    path('change-address/<id>/', update_billingaddress, name='update_billingaddress'),
]

