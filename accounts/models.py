from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from .managers import UserManager

from phonenumber_field.modelfields import PhoneNumberField
from cities_light.models import City, Country



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
	name = models.CharField(max_length=255, null=True, blank=True)
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
		return self.cleaned_data['name'].capitalize()


	# def get_display_name(self):
	#   if self.name != '':
	#       return self.name
	#   else:
	#       return self.username

	# def get_name(self):
	#   name = '%s %s' % (self.first_name, self.last_name)
	#   return name.strip()
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


class Address(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False, related_name='user_address')
	address = models.CharField(max_length=255, null=True, blank=True)
	state = models.CharField(max_length=255, null=True, blank=True)
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	location = models.CharField(max_length=255, null=True, blank=True)
	pin_code = models.CharField(max_length=255, null=True, blank=True)
	zip = models.CharField(max_length=100, null=True, blank=True)

	class Meta:
		verbose_name = _('Address')
		verbose_name_plural = _("Address")

	def __str__(self):
		return self.address

	def get_total_price(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total


class Patient(models.Model):
	user_patient = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False, related_name='user_patient')
	name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(verbose_name='Email', error_messages={'unique':"This email has already been registered.",}, max_length=255, unique=True)
	phone_number = PhoneNumberField(blank=True)
	birth_date = models.DateField(null=True, blank=False)
	gender = models.CharField(max_length=255, choices=GENDER_CHOICES, default=None, blank=True, null=True)
	relation = models.CharField(max_length=255, choices=RELATION_CHOICES, default=None, blank=True, null=True)

	class Meta:
		verbose_name = _('Patient')
		verbose_name_plural = _("Patient")

	def __str__(self):
		return self.name
	
