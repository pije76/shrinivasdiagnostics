from django.contrib import admin
# from django.contrib.auth import views
from django.urls import path, re_path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView

# from accounts import views
from .views import *
from . import views

# from accounts.views import SignUpAutoComplete

app_name = 'accounts'

urlpatterns = [
    path('', login_view_modal, name='login_view_modal'),
]

