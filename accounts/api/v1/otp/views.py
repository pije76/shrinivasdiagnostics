from rest_framework import viewsets, status as response_status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import smart_str

from accounts.models import UOTP

from .serializers import CreateOTPSerializer, UpdateUOTPSerializer


class OTPViewSet(viewsets.ViewSet):
	"""
	POST
	-----

	This method will create or update existing otp
	if previous otp still valid

	Param;

		{
			"issuer": "08911494141"
		}


	PATCH
	------

	Update otp, but real case use for many reason such as signin

	Param;

		No param
	"""

	lookup_field = 'otp'
	permission_classes = (AllowAny,)

	def initialize_request(self, request, *args, **kwargs):
		self.context = {'request': request}
		return super().initialize_request(request, *args, **kwargs)
		
	def list(self, request):
		return Response('Not implemented yet', status=response_status.HTTP_403_FORBIDDEN)

	def get_object(self, otp):
		obj = get_object_or_404(UOTP, otp=otp)
		return obj

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
			return Response(serializer.data, status=response_status.HTTP_201_CREATED)
		return Response(serializer.errors, status=response_status.HTTP_406_NOT_ACCEPTABLE)

	@transaction.atomic
	def partial_update(self, request, otp=None):
		instance = self.get_object(otp=otp)
		serializer = UpdateUOTPSerializer(
			instance=instance,
			data=request.data,
			context=self.context,
			partial=True
		)

		if serializer.is_valid(raise_exception=True):
			try:
				serializer.save()
			except DjangoValidationError as e:
				return Response(smart_str(e), status=response_status.HTTP_403_FORBIDDEN)
			return Response(serializer.data, status=response_status.HTTP_202_ACCEPTED)
		return Response(serializer.errors, status=response_status.HTTP_406_NOT_ACCEPTABLE)
