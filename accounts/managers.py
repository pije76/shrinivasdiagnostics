from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from datetime import datetime


class UserManager(BaseUserManager):
    use_in_migrations = True

    # def _create_user(self, email, password, **extra_fields):
    # def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    #     """
    #     Creates and saves a User with the given email and password.
    #     """
    #     now = timezone.now()
    #     if not email:
    #         raise ValueError('The given email must be set')
    #     email = self.normalize_email(email)
    #     # user = self.model(email=email, **extra_fields)
    #     user = self.model(email=email, is_staff=False, is_active=True, is_superuser=False, last_login=now, date_joined=now, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user


    # def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_superuser', False)
        # return self._create_user(email, password, **extra_fields)
        # return self._create_user(email, password, False, False, **extra_fields)

    def create_user(self,email,phone_number,password=None):
        if not email:
            raise ValueError("Users must enter an email address.")
        if not phone_number:
            raise ValueError("Users must enter a phone_number.")
        user = self.model(email= self.normalize_email(email), phone_number = phone_number,)
        user.set_password=password
        user.save(using=self._db)
        return user

    # def create_user(self, email, password=None, username=""):
    #   """
    #   Creates and saves a User with the given email and password.

    #   NOTE: Argument 'username' is needed for social-auth. It is not actually used.
    #   """
    #   if not email:
    #       raise ValueError('Users must have an email address.')

    #   # Validate email is unique in database
    #   if MemberProfile.objects.filter(email = self.normalize_email(email).lower()).exists():
    #       raise ValueError('This email has already been registered.')

    #   user = self.model(email=self.normalize_email(email).lower(),)

    #   user.set_password(password)

    #   # Save and catch IntegrityError (due to email being unique)
    #   try:
    #       user.save(using=self._db)

    #   except IntegrityError:
    #       raise ValueError('This email has already been registered.')

    #   return user


    # def create_superuser(self, email, password, **extra_fields):
    #   extra_fields.setdefault('is_superuser', True)

    #   if extra_fields.get('is_superuser') is not True:
    #       raise ValueError('Superuser must have is_superuser=True.')

    #   return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **kwargs):
        user = self.model(email=email, is_staff=True, is_admin=True, is_superuser=True, is_active=True, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
