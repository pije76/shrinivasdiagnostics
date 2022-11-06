from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .otp.views import OTPViewSet

router = DefaultRouter(trailing_slash=True)
router.register('otps', OTPViewSet, basename='otp')

urlpatterns = [
    path('', include(router.urls)),
]
