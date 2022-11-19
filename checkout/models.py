from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import *

from accounts.models import *
from shop.models import *

# Create your models here.
class Checkout(models.Model) :
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False, related_name='checkout_user')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    items = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.email

    @property
    def get_total_price(self):
        total_sum = 0
        for order_item in self.items.all():
            total_sum += order_item.get_final_price()
        return total_sum


class Payment(models.Model):
    # name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False, related_name='payment_user')
    payment_id = models.CharField(_("Payment ID"), max_length=36, null=False, blank=False)
    razorpay_order_id = models.CharField(_("Order ID"), max_length=40, null=False, blank=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = models.CharField(_("Payment Status"), default=PaymentStatus.PENDING, max_length=254, blank=False, null=False)
    signature_id = models.CharField(_("Signature ID"), max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.id}-{self.user}-{self.amount}-{self.status}"

    @property
    def get_total_price(self):
        total_sum = 0
        for order_item in self.items.all():
            total_sum += order_item.get_final_price()
        return total_sum

    @property
    def total_price(self):
        return sum([item.total_price for item in self.items.all()])
