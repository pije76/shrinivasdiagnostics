from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import *

from accounts.models import *
from address.models import *
from shop.models import *

PAYMENT_TYPE = (
    ('online', 'Online'),
    ('cash', 'Cash On Order'),
)

PAYMENT_STATUS = (
    ('success', 'Success'),
    ('failure', 'Failure'),
    ('waiting', 'Waiting'),
    ('pending', 'Pending'),
)

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False, related_name='order_user')
    item_order = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False, related_name='order_product')
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.user.ordered
        return f"{self.product}: {self.quantity}"
        # return f"{self.id}-{self.title}-{self.status}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
    #     get_total_item_price_float = float(get_total_item_price)
    #     get_total_discount_item_price_float = float(get_total_discount_item_price)
        return self.get_total_item_price() - self.get_total_discount_item_price()
        # return self.get_total_item_price_float() - self.get_total_discount_item_price_float()

    @property
    def get_final_price(self):
        if self.product.discount_price:
            discount_price = self.get_total_discount_item_price
            return discount_price
        item_price = self.get_total_item_price
        return item_price


class Checkout(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False, related_name='checkout_user')
    amount = models.FloatField(null=True, blank=False)
    status = models.CharField(default="pending", choices=PAYMENT_STATUS, max_length=254, blank=False, null=False)
    provider_order_id = models.CharField(max_length=40, null=False, blank=False)
    signature_id = models.CharField(max_length=128, null=False, blank=False)
    payment_type = models.CharField(default="cash", choices=PAYMENT_TYPE, max_length=36, null=False, blank=False)
    payment_id = models.CharField(max_length=32, null=False, blank=False)
    # payment_id = models.CharField(primary_key=False, editable=False, max_length=10)
    # payment_name = models.CharField(max_length=100)

    ordered = models.BooleanField(default=False)
    # ordered = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name='checkout_ordered')
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    checkout_date = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Order)

    def __str__(self):
        return self.payment_id

    @property
    def get_total_price(self):
        total_sum = 0
        for order_item in self.items.all():
            total_sum += order_item.get_final_price()
        return total_sum

    @property
    def total_price(self):
        return sum([item.total_price for item in self.items.all()])

