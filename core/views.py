from django.shortcuts import render
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from .models import *
from .forms import *

# Create your views here.
class HomeView(TemplateView):
    template_name = "core/home.html"
