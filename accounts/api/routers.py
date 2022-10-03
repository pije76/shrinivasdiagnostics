from django.urls import path, include
from accounts.api.v1 import routers

urlpatterns = [
    path('accounts/v1/', include((routers, 'accounts_api_v1'), namespace='accounts_api_v1')),
]
