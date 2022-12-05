from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from accounts.models import *

# from cities_light.models import City, Country

# Create your models here.
LABEL = (
	('doctor', 'Doctor'),
	('patient', 'Patient')
)

CATEGORY_CHOICES = (
	('organ', 'Organ'),
	('condition', 'Condition'),
	# ('test', 'Test'),
	# ('packages', 'Packages')
)

ORGAN = (
	('adrenal-gland', 'Adrenal gland'),
	('bone', 'Bone'),
	('heart', 'Heart'),
	('kidney', 'Kidney'),
	('liver', 'Liver'),
	('pancreas', 'Pancreas'),
	('thyroid', 'Thyroid'),
)

CONDITION = (
	('diabetes', 'Diabetes'),
	('industrial-diseases', 'Industrial diseases'),
	('myasthenia-gravis', 'Myasthenia gravis'),
	('nutritional-disorders', 'Nutritional disorders'),
)

def pdf_upload_path(instance, filename):
	return f'upload/report/{instance.created_date.strftime("%Y-%m-%d")}_test_{filename}'

def upload_path_category(instance, filename):
	return os.path.join('upload/category/', format(instance.title), filename)


class Category(models.Model):
	# title = models.CharField(max_length=255, null=True, blank=False, db_index=True)
	title = models.CharField(max_length=255, null=True, blank=True)
	category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default="organ", null=True, blank=True)
	slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
	image = models.ImageField(upload_to=upload_path_category, blank=True, null=True)

	class Meta:
		ordering=('title',)
		verbose_name ='category'
		verbose_name_plural='categories'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('shop:product_list_by_category', args=[self.slug])

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	@property
	def image_url(self):
		if self.image and hasattr(self.image, 'url'):
			return self.image.url


class Product(models.Model):
	title = models.CharField(max_length=255, null=True, blank=False, db_index=True)
	slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
	# category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default="organ", null=True, blank=True)
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
		ordering = ('title',)
		index_together = (('id','slug'),)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		# return reverse('shop:product_detail', args=[self.id, self.slug])
		return reverse("product_detail", kwargs={"pk" : self.pk})

	def get_add_to_cart_url(self) :
		return reverse("shop:add_to_cart", kwargs={"pk" : self.pk})

	def get_remove_from_cart_url(self) :
		return reverse("shop:remove_from_cart", kwargs={"pk" : self.pk})

