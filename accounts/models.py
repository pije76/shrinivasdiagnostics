from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager

GENDER_CHOICES = (
	("male", _('Male')),
	("female", _('Female')),
	# ("unknown", _('Unknown'))
)

RELATION_CHOICES = (
	("father", _('Male')),
	("mother", _('Female')),
	("spouse", _('Spouse')),
	("son", _('Son')),
	("daughter", _('Daughter')),
	("family", _('Family'))
)

# Create your models here.
class Profile(AbstractBaseUser, PermissionsMixin):
	name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(verbose_name='Email Address', error_messages={'unique':"This email has already been registered.",}, max_length=255, unique=True)
	phone_number = PhoneNumberField(blank=True)
	birth_date = models.DateField(null=True, blank=False)
	gender = models.CharField(max_length=255, choices=GENDER_CHOICES, default=None, blank=True, null=True)

	is_active = models.BooleanField(default=False, blank=True, null=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	# date_joined = models.DateTimeField(default=timezone.now)

	# email_verified = models.BooleanField(default=False, null=True, blank=True)
	# membership_type = models.CharField(max_length=255, choices=MEMBERSHIP_CHOICES, default='trial', null=True, blank=True)

	# email_secret = models.CharField(max_length=20, default="", blank=True)
	# is_email_validated = models.BooleanField(default=False)

	# form_submitted = models.BooleanField(default=False, null=True, blank=True)
	# completion_level = models.PositiveSmallIntegerField(default=0, verbose_name=_('Profile completion percentage'), null=True, blank=True)
	# personal_info_is_completed = models.BooleanField(default=False, verbose_name=_('Personal info completed'), null=True, blank=True)

	objects = UserManager()
	# EMAIL_FIELD = "email"
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["phone_number"]
	# REQUIRED_FIELDS = []

	class Meta:
		verbose_name = _('Profile')
		verbose_name_plural = _("Profile")

	# def __str__(self):
	#   return self.username
		# return str(self.username)
		# return "User profile: %s" % self.username
		# return self.email

	# def clean(self):
	#   super().clean()
	#   self.sun_sign = self.name
	#   self.email = self.__class__.objects.normalize_email(self.email)

	def clean_title(self):
		return self.cleaned_data['name'].capitalize()



	# def get_completion_level(self):
	#   completion_level = 0
	#   if self.email_verified:
	#       completion_level += 50
	#   if self.personal_info_is_completed:
	#       completion_level += 50
	#   return completion_level

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

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)

	# def verify_email(self):
	#   if self.email_verified is False:
	#       secret = uuid.uuid4().hex[:20]
	#       self.email_secret = secret
	#       html_message = render_to_string("email/verify_email.html", {"secret": secret})
	#       send_mail("Verify Hairbnb Account", strip_tags(html_message), settings.EMAIL_FROM, [self.email], html_message=html_message,)
	#       self.save()
	#   return


class Address(models.Model):
	address = models.CharField(max_length=255, null=True, blank=True)
	state = models.CharField(max_length=255, null=True, blank=True)
	city = models.CharField(max_length=255, null=True, blank=True)
	location = models.CharField(max_length=255, null=True, blank=True)
	pin_code = models.CharField(max_length=255, null=True, blank=True)

	class Meta:
		verbose_name = _('Address')
		verbose_name_plural = _("Address")

	def __str__(self):
		return self.address


class Patient(models.Model):
	# profile = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='patient_profile', null=True, blank=True)
	name = models.CharField(max_length=255, null=True, blank=True)
	email = models.EmailField(verbose_name='Email Address', error_messages={'unique':"This email has already been registered.",}, max_length=255, unique=True)
	phone_number = PhoneNumberField(blank=True)
	birth_date = models.DateField(null=True, blank=False)
	gender = models.CharField(max_length=255, choices=GENDER_CHOICES, default=None, blank=True, null=True)
	relation = models.CharField(max_length=255, choices=RELATION_CHOICES, default=None, blank=True, null=True)

	class Meta:
		verbose_name = _('Patient')
		verbose_name_plural = _("Patient")

	def __str__(self):
		return self.name

