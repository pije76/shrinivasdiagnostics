from django.urls import path, include

from .views import *
# from . import views

app_name = 'homepage'

urlpatterns = [
    # path('', views.MembershipView.as_view(), name='index'),
    path('', index, name='index'),
]
