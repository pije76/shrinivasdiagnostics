from django.shortcuts import render
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import *
from .forms import *

# Create your views here.
def homepage(request):
	titles = _('Check the Best Blood Test &amp; Pathology Lab in India with Shrinivas Diagnostics Labs')

	context = {
		'titles': titles,
	}

	return render(request, 'core/home.html', context)

