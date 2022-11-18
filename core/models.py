from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from accounts.models import *

from cities_light.models import City, Country

# Create your models here.
class Schedule(models.Model):
    # user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering=('name',)
        verbose_name ='Schedule'
        verbose_name_plural='Schedules'

    def __str__(self):
        return self.name
