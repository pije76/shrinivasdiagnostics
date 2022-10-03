from rest_framework import viewsets, status as response_status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import smart_str

from .serializers import CreateOTPSerializer


class OTPViewSet(viewsets.ViewSet):
	lookup_field = 'otp'
	permission_classes = (AllowAny,)

	def initialize_request(self, request, *args, **kwargs):
		self.context = {'request': request}
		return super().initialize_request(request, *args, **kwargs)
		
	def list(self, request):
		return Response('Not implemented yet', status=response_status.HTTP_403_FORBIDDEN)

	@transaction.atomic
	def create(self, request):
		serializer = CreateOTPSerializer(
			data=request.data,
			context=self.context
		)

		if serializer.is_valid(raise_exception=True):
			try:
				serializer.save()
			except DjangoValidationError as e:
				return Response(smart_str(e), status=response_status.HTTP_403_FORBIDDEN)
			return Response(serializer.data, status=response_status.HTTP_200_OK)
		return Response(serializer.errors, status=response_status.HTTP_406_NOT_ACCEPTABLE)
