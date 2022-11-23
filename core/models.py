from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from accounts.models import *

from cities_light.models import City, Country

# Create your models here.
class Schedule(models.Model):
    # user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False)
    full_name = models.CharField(max_length=255, null=True, blank=False)
    phone_number = PhoneNumberField(null=True, blank=False)
    # city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering=('full_name',)
        verbose_name ='Schedule Home'
        verbose_name_plural='Schedule Home'

    def __str__(self):
        return self.full_name
