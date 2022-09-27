from django.urls import path, include

from .views import *
# from . import views

app_name = 'subscription'

urlpatterns = [
	# path('', views.MembershipView.as_view(), name='index'),
	path('', index, name='index'),
	path('subscription/', subscription, name='subscription'),
	path('trial/', trial, name='trial'),
	path('basic/', basic, name='basic'),
	path('professional/', professional, name='professional'),
	path('enterprise/', enterprise, name='enterprise'),
	path('plans/<str:planname>/', plan, name='plan'),
	# path('subscribe/', subscribe, name='subscribe'),
	path('checkout/', checkout, name='checkout'),
	path('settings/', settings, name='settings'),
	path('updateaccounts/', updateaccounts, name='updateaccounts'),
]
