from rest_framework import serializers
from accounts.models import UOTP


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
		issuer = validated_data.pop('issuer')
		instance = self.Meta.model.objects.generate(issuer)

		return instance
	