from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from .managers import UserManager

from shop.models import *

from phonenumber_field.modelfields import PhoneNumberField
# from cities_light.models import *

GENDER_CHOICES = (
	("male", _('Male')),
	("female", _('Female')),
	# ("unknown", _('Unknown'))
)

RELATION_CHOICES = (
	("father", _('Father')),
	("mother", _('Mother')),
	("spouse", _('Spouse')),
	("son", _('Son')),
	("daughter", _('Daughter')),
	("family", _('Family'))
)

# Create your models here.
class Profile(AbstractBaseUser, PermissionsMixin):
	full_name = models.CharField(max_length=255, null=True, blank=True)
	username = models.CharField(max_length=255, blank=True, null=True)
	email = models.EmailField(verbose_name='Email', error_messages={'unique':"This email has already been registered.",}, max_length=255, unique=True)
	phone_number = PhoneNumberField(null=True, blank=False)
	otp = models.CharField(max_length=12, null=True, blank=True)
	phone_verified = models.BooleanField(default=False)
	birth_date = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=255, choices=GENDER_CHOICES, default=None, blank=True, null=True)

	is_active = models.BooleanField(default=True, blank=True, null=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	objects = UserManager()
	# EMAIL_FIELD = "email"
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["phone_number"]

	class Meta:
		verbose_name = _('Profile')
		verbose_name_plural = _("Profile")

	def __str__(self):
		return self.email

	def clean(self):
	  super().clean()
	  self.email = self.__class__.objects.normalize_email(self.email)

	def clean_title(self):
		return self.cleaned_data['full_name'].capitalize()


	# def get_display_name(self):
	#   if self.full_name != '':
	#       return self.full_name
	#   else:
	#       return self.username

	# def get_name(self):
	#   full_name = '%s %s' % (self.first_name, self.last_name)
	#   return full_name.strip()
	#   # return self.email

	# def get_short_name(self):
	#   return self.first_name
		# return self.email

	# def email_user(self, subject, message, from_email=None, **kwargs):
	# 	send_mail(subject, message, from_email, [self.email], **kwargs)

	# def verify_email(self):
	#   if self.email_verified is False:
	#       secret = uuid.uuid4().hex[:20]
	#       self.email_secret = secret
	#       html_message = render_to_string("email/verify_email.html", {"secret": secret})
	#       send_mail("Verify Hairbnb Account", strip_tags(html_message), settings.EMAIL_FROM, [self.email], html_message=html_message,)
	#       self.save()
	#   return


class Patient(models.Model):
	full_name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(verbose_name='Email', error_messages={'unique':"This email has already been registered.",}, max_length=255, unique=True)
	phone_number = PhoneNumberField(null=True, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=255, choices=GENDER_CHOICES, default=None, blank=True, null=True)
	relation = models.CharField(max_length=255, choices=RELATION_CHOICES, default=None, blank=True, null=True)
	user_patient = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False, related_name='user_patient')
	test_package = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='test_patient')

	class Meta:
		verbose_name = _('Patient')
		verbose_name_plural = _("Patient")

	def __str__(self):
		return self.full_name
	
