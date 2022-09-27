from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager

GENDER_CHOICES = (
    ("male", _('Male')),
    ("female", _('Female')),
    ("unknown", _('Unknown'))
)

# Create your models here.
class Profile(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name='Email Address', error_messages={'unique':"This email has already been registered.",}, max_length=255, unique=True)
    phone_number = PhoneNumberField(blank=True)
    birth_date = models.DateField(null=True, blank=False)
    gender = models.IntegerField(choices=GENDER_CHOICES, default='unknown')

    # is_active = models.BooleanField(default=False, blank=True, null=True)
    # is_staff = models.BooleanField(default=False)
    # is_admin = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    email_verified = models.BooleanField(default=False, null=True, blank=True)
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

    # def update_completion_level(self):
    #   self.completion_level = self.get_completion_level()
    #   self.save()

    # def has_perm(self, perm, obj=None):
    #   "Does the user have a specific permission?"
    #   # Simplest possible answer: Yes, always
    #   return True

    # def has_module_perms(self, app_label):
    #   "Does the user have permissions to view the app `app_label`?"
    #   # Simplest possible answer: Yes, always
    #   return True

    # @property
    # def is_staff(self):
    #   "Is the user a member of staff?"
    #   # Simplest possible answer: All admins are staff
    #   # return self.is_admin
    #   return self.is_staff

    # @property
    # def name(self):
    #   return f'{self.first_name} {self.last_name}'

    # def save(self, *args, **kwargs):
    #   self.sun_sign = str(self.birth_date)
    #   self.sun_sign = self.name
    # #     get_nataldate = self.birth_date
    # #     get_tz = ts.utc(get_nataldate)
    # #     sun_sign = get_geo_sun(get_tz)
    # #     if self.sun_sign is None:
    # #         self.sun_sign = get_zodiac(sun_sign)
    #   super().save(*args, **kwargs)

    # # def save(self, birth_date=False, *args, **kwargs):
    # def save(self, birth_date, *args, **kwargs):
    #   get_nataldate = self.birth_date
    #   print(self.get_nataldate)
    #   # if sun_sign:
    #   #   small = rescale_image(self.image,width=100,height=100)
    #   #   self.image_small = SimpleUploadedFile(name,small_pic)
    #   super().save(*args, **kwargs)


    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url

    def avatar_thumb(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return mark_safe('<img src="%s" style="width: 60px; height: 60px" />' % self.avatar.url)
        else:
            return _('No Avatar')

    avatar_thumb.short_description = _('Avatar')


# def save_post(sender, instance, **kwargs):
#   print("Pre save")


# pre_save.connect(save_post, sender=Profile)

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#   if created:
#       Profile.objects.create(user=instance)
#   instance.memberprofile.save()

# class CustomSignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=255, required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'password1')
