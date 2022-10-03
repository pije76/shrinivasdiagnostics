from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class RootAPIView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = (AnonRateThrottle, UserRateThrottle,)

    def get(self, request, format=None):
        return Response({
            'accounts': {
                'otp': reverse(
                    'accounts_api_v1:otp-list', 
                    request=request,
                    format=format, 
                    current_app='accounts'
                ),
            },
        })
