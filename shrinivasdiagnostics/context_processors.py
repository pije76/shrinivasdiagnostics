"""shrinivasdiagnostics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from shop.views import *
from order.views import *
from accounts.views import *
from .models import *

import datetime

# For _footer_bottom.html template file
def current_year_context_processor(request):
    current_datetime = datetime.datetime.now()
    return {
        'current_year': current_datetime.year
    }


# For _footer.html template file
def posts_context_processor(request):
    posts = Product.objects.order_by('-updated')  # By updated date.

    return {
        'posts': posts
    }

def context_processor(request):
   context = {}
   context['service_list'] = Product.objects.all()
   return context
