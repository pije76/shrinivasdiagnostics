import pyotp

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

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


class UOTPManagerQuerySet(models.QuerySet):
	def generate(self, issuer):
		"""Create new otp object if valid_until greather than now
		or update if valid_until lower than now"""
		secret = pyotp.random_base32()
		otp = pyotp.TOTP(secret).now()
		valid_until = timezone.now() + timezone.timedelta(hours=2)
		valid_until_timestamp = valid_until \
			.replace(microsecond=0) \
			.timestamp()

		data = {
			'valid_until': valid_until,
			'valid_until_timestamp': valid_until_timestamp,
			'secret': secret,
			'otp': otp
		}

		instance, _created = self.filter(valid_until__gt=timezone.now()) \
			.update_or_create(**data, defaults={'issuer': issuer})

		return instance

	def validate(self, issuer, otp, secret):
		"""Return True if valid and False if invalid"""
		try:
			instance = self.get(issuer=issuer, otp=otp, secret=secret)
		except ObjectDoesNotExist:
			return False
		
		if instance.valid_until < timezone.now():
			return False
			
		totp = pyotp.TOTP(instance.secret)
		return totp.verify(instance.otp)

	def get_user_from_issuer(self, issuer):
		"""Get user instance from issuer"""
		try:
			return Profile.objects.get(phone_number=issuer)
		except ObjectDoesNotExist:
			return None

	def get_or_create_user_from_issuer(self, issuer):
		"""If user not exists create one"""
		fake_username = issuer
		fake_email = '{}@gmail.com'.format(issuer)
		fake_password = '{}'.format(issuer)

		user = self.get_user_from_issuer(issuer)
		if user is None:
			user = Profile.objects.create_user(fake_username, fake_email, fake_password)
			user.phone_number = issuer
			user.save()

		return user


class UOTP(models.Model):
	class PurposeChoices(models.TextChoices):
		SIGNIN = 'signin', _("Sign In")

	create_at = models.DateTimeField(auto_now_add=True, db_index=True)
	update_at = models.DateTimeField(auto_now=True)

	issuer = models.CharField(
        max_length=255,
        help_text=_("One of Email or Msisdn"),
    )
	purpose = models.CharField(
		max_length=15, 
		choices=PurposeChoices.choices,
		default=PurposeChoices.SIGNIN
	)
	otp = models.CharField(max_length=10, db_index=True)
	secret = models.CharField(max_length=255, db_index=True)
	valid_until = models.DateTimeField(blank=True, null=True, editable=False)
	valid_until_timestamp = models.IntegerField(blank=True, null=True)

	objects = UOTPManagerQuerySet.as_manager()

	def __str__(self) -> str:
		return self.otp
