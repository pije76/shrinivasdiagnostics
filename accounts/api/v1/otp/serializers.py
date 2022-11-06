from django.utils.translation import gettext_lazy as _
from django.contrib.auth import login

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import UOTP

OTP_SECRET_KEY = 'otp_secret'


class BaseOTPSerializer(serializers.ModelSerializer):
	class Meta:
		model = UOTP
		fields = '__all__'


class CreateOTPSerializer(BaseOTPSerializer):
	class Meta(BaseOTPSerializer.Meta):
		fields = ['issuer']

	def to_representation(self, instance):
		response = {
			'issuer': instance.issuer,
			'otp': instance.otp,
		}

		return response

	def create(self, validated_data):
		request = self.context.get('request')
		issuer = validated_data.pop('issuer')
		instance = self.Meta.model.objects.generate(issuer)

		# save temporary secret to session
		request.session[OTP_SECRET_KEY] = instance.secret
		return instance


class UpdateUOTPSerializer(BaseOTPSerializer):
	class Meta(BaseOTPSerializer.Meta):
		fields = ['otp']

	def _force_user_signin(self, request, user):
		login(request, user)
	
	def update(self, instance, validated_data):
		request = self.context.get('request')
		secret = request.session.get(OTP_SECRET_KEY, None)

		if secret is None:
			raise ValidationError({'secret': _("Secret from OTP invalid")})

		if instance.secret != secret:
			raise ValidationError({'secret': _("Secret and OTP not match")})
		
		# signin method
		if instance.purpose == self.Meta.model.PurposeChoices.SIGNIN:
			user = self.Meta.model.objects.get_or_create_user_from_issuer(instance.issuer)
			self._force_user_signin(request, user)

		return instance
