from django.urls import path

from .views import *

app_name = 'core'

urlpatterns = [
    path('', homepage, name='homepage'),
    # path('schedule/', schedule, name='schedule'),
]
