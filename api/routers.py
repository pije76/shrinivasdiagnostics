from django.urls import path, include

from api.views import RootAPIView
from accounts.api import routers as accounts_routers

urlpatterns = [
    path('', RootAPIView.as_view(), name='api'),
    path('', include(accounts_routers)),
]
