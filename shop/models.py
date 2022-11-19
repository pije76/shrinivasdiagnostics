from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .constants import *

from accounts.models import *

from cities_light.models import City, Country

# Create your models here.
LABEL = (
	('doctor', 'Doctor'),
	('patient', 'Patient')
)

PAYMENT_STATUS = (
	('success', 'Success'),
	('failure', 'Failure'),
	('pending', 'Pending')
)

def pdf_upload_path(instance, filename):
	return f'test_package/{instance.created_date.strftime("%Y-%m-%d")}_test_{filename}'


class Category(models.Model):
	name = models.CharField(max_length=255, null=True, blank=False, db_index=True)
	slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

	class Meta:
		ordering=('name',)
		verbose_name ='category'
		verbose_name_plural='categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
	name = models.CharField(max_length=255, null=True, blank=False, db_index=True)
	slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
	tags = models.CharField(max_length=255, null=True, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
	discount_price = models.DecimalField(_("Discount Price"), max_digits=10, decimal_places=2, blank=True, null=True)
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	# label = models.CharField(choices=LABEL, max_length=7)
	## Patient ##
	prerequisites = models.CharField(_("Pre-Requisites"), max_length=255, null=True, blank=True)
	# TAT #
	samplecutoff = models.CharField(_("Sample Cut Off"), max_length=255, null=True, blank=True)
	report = models.FileField(upload_to=pdf_upload_path, blank=True)
	## Doctor ##
	component = models.CharField(max_length=255, null=True, blank=True)
	speciment = models.CharField(max_length=255, null=True, blank=True)
	method = models.CharField(max_length=255, null=True, blank=True)
	cutofftime = models.CharField(_("Cut Off Time"), max_length=255, null=True, blank=True)
	quantitytemperature = models.CharField(_("Quantity and Temperature"), max_length=255, null=True, blank=True)

	class Meta:
		ordering = ('name',)
		index_together = (('id','slug'),)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		# return reverse('shop:product_detail', args=[self.id, self.slug])
		return reverse("product_detail", kwargs={"pk" : self.pk})

	def get_add_to_cart_url(self) :
		return reverse("shop:add_to_cart", kwargs={"pk" : self.pk})

	def get_remove_from_cart_url(self) :
		return reverse("shop:remove_from_cart", kwargs={"pk" : self.pk})


class Order(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=False, related_name='order_user')
	ordered = models.BooleanField(default=False)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False, related_name='order_product')
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f"{self.quantity} of {self.product.name}"
		# return f"{self.id}-{self.name}-{self.status}"

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
