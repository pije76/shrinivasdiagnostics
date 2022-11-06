import pyotp

from django.test import TestCase
from .models import UOTP


class UOTPTestCase(TestCase):
	def setUp(self) -> None:
		super().setUp()

		self.issuer = '0811600600'
		self.instance = UOTP.objects.generate(self.issuer)
		self.otp = self.instance.otp
		self.secret = self.instance.secret

	def test_uotp_generated(self):
		instance = UOTP.objects.get(issuer=self.issuer)
		self.assertEqual(instance.secret, self.secret)
		self.assertEqual(instance.otp, self.otp)

	def test_uotp_is_valid(self):
		is_valid = UOTP.objects.validate(self.issuer, self.otp, self.secret)
		self.assertEqual(is_valid, True)

	def test_uotp_is_otp_invalid(self):
		is_valid = UOTP.objects.validate(self.issuer, '122425', self.secret)
		self.assertEqual(is_valid, False)

	def test_uotp_is_secret_invalid(self):
		is_valid = UOTP.objects.validate(self.issuer, self.otp, 'secret53985398539')
		self.assertEqual(is_valid, False)
	
	def test_create_and_get_user_from_issuer(self):
		user = UOTP.objects.get_or_create_user_from_issuer(self.issuer)
		self.assertEqual(user.id, 1)

		user_otp = UOTP.objects.get_user_from_issuer(self.issuer)
		self.assertEqual(user_otp.phone_number, self.issuer)
