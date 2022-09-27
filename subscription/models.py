from django.db import models
from django.conf import settings
from django.db.models import signals

from accounts.models import *
from market.models import *
# from chart.models import *

# from choices import *

MEMBERSHIP_CHOICES = (
    ('trial', 'Trial'),
    ('basic', 'Basic'),
    ('professional', 'Professional'),
    ('enterprise', 'Enterprise'),
)

RECURRENCE_UNIT_CHOICES = (
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('yearly', 'Yearly'),
    ('lifetime', 'Lifetime'),
)

TRANSACTION_CHOICES = (
    ('paid', 'Paid'),
    ('waiting', 'Waiting'),
    ('expired', 'Expired'),
)

# Create your models here.
class Package(models.Model):
	title = models.CharField(max_length=30, choices=MEMBERSHIP_CHOICES, default='trial', null=True, blank=True)
	slug = models.SlugField(max_length=255, null=True, blank=True)
	description = models.TextField(max_length=500, null=True, blank=True)

	def __str__(self):
		return self.title


class TickerCost(models.Model):
	ticker = models.ForeignKey(MarketDetail, on_delete=models.CASCADE, related_name='ticker_cost', null=True, blank=True)
	billing_period = models.PositiveIntegerField(default=1, null=True, blank=True)
	billing_unit = models.CharField(choices=RECURRENCE_UNIT_CHOICES, default='weekly', max_length=16, null=True, blank=True)
	price = models.DecimalField(default=10000, max_digits=16, decimal_places=2, null=True, blank=True)
	quota = models.PositiveIntegerField(default=1, null=True, blank=True)

	def __str__(self):
		return str(self.price)


class IndicatorCost(models.Model):
	# indicator = models.ForeignKey(ChartOption, on_delete=models.CASCADE, related_name='indicator_cost', null=True, blank=True)
	billing_period = models.PositiveIntegerField(default=1, null=True, blank=True)
	billing_unit = models.CharField(choices=RECURRENCE_UNIT_CHOICES, default='weekly', max_length=16, null=True, blank=True)
	price = models.DecimalField(default=10000, max_digits=16, decimal_places=2, null=True, blank=True)
	quota = models.PositiveIntegerField(default=1, null=True, blank=True)

	def __str__(self):
		return str(self.price)


class PackageCost(models.Model):
	subscription = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='subscription_package', null=True, blank=True)
	ticker = models.ForeignKey(MarketDetail, on_delete=models.CASCADE, related_name='ticker_package', null=True, blank=True)
	# indicator = models.ForeignKey(ChartOption, on_delete=models.CASCADE, related_name='indicator_package', null=True, blank=True)
	billing_period = models.PositiveIntegerField(default=1, null=True, blank=True)
	billing_unit = models.CharField(choices=RECURRENCE_UNIT_CHOICES, default='weekly', max_length=16, null=True, blank=True)
	price = models.DecimalField(default=0, max_digits=16, decimal_places=2, null=True, blank=True)
	quota = models.PositiveIntegerField(default=1, null=True, blank=True)

	def __str__(self):
		return str(self.price)


class Subscription(models.Model):
	member = models.ForeignKey(Profile, related_name='member_subscription', on_delete=models.CASCADE, null=True, blank=True)
	subscription = models.ForeignKey(Package, related_name='subscription_subscription', on_delete=models.SET_NULL, null=True)
	# ticker = models.ForeignKey(TickerCost, related_name='subscription_subscription', on_delete=models.SET_NULL, null=True)
	# indicator = models.ForeignKey(IndicatorCost, related_name='subscription_subscription', on_delete=models.SET_NULL, null=True)
	# price = models.ForeignKey(PackageCost, related_name='price_subscription', on_delete=models.CASCADE, null=True, blank=True)
	begin_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	expired_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
	# quantity = models.IntegerField(null=True, blank=True)
	active = models.BooleanField(default=False, null=True, blank=True)
	status = models.CharField(max_length=50, choices=TRANSACTION_CHOICES, default='expired', null=True, blank=True)
	# active = models.CharField(max_length=50, choices=STATUS_CHOICES, default='cancel', null=True, blank=True)

	def __str__(self):
		# return self.member
		return str(self.member)

	def is_paid(self):
		return self.status == "expired" or self.status == "paid"

	# def save(self, *args, **kwargs):
	# 	super().save(*args, **kwargs)
	# 	self.buyer.money += self.value
	# 	self.buyer.save()
	# 	self.seller.money -= self.value
	# 	self.seller.save()

