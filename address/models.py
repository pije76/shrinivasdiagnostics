from django.db import models
from django.utils.translation import gettext_lazy as _

from cities_light.abstract_models import AbstractCountry, AbstractRegion, AbstractCity, AbstractSubRegion
from cities_light.receivers import connect_default_signals

from accounts.models import *

# Create your models here.
class Country(AbstractCountry):
    pass
connect_default_signals(Country)

class Region(AbstractRegion):
    pass
connect_default_signals(Region)

class SubRegion(AbstractSubRegion):
    pass
connect_default_signals(SubRegion)

class City(AbstractCity):
    timezone = models.CharField(max_length=40)
connect_default_signals(City)


class Address(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False, related_name='user_address')
    address = models.CharField(max_length=255, null=True, blank=True)
    # state = models.CharField(max_length=255, null=True, blank=True)
    state = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    pin_code = models.CharField(max_length=255, null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _("Address")

    def __str__(self):
        return self.address

    def get_address(self):
        return self.address
