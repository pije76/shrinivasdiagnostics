from django.db import models
from django.urls import reverse

from accounts.models import *

from cities_light.models import City, Country

# Create your models here.
LABEL = (
    ('doctor', 'Doctor'),
    ('patient', 'Patient')
)

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product')
    tags = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # image = models.ImageField(upload_to='prodcuts/%Y/%m/%d',blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    label = models.CharField(choices=LABEL, max_length=7)
    ## Patient ##
    prerequisites = models.CharField(max_length=255, null=True, blank=True)
    # TAT #
    samplecutoff = models.CharField(max_length=255, null=True, blank=True)
    report = models.TextField(blank=True)
    note = models.TextField(blank=True)
    ## Doctor ##
    component = models.CharField(max_length=255, null=True, blank=True)
    speciment = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(max_length=255, null=True, blank=True)
    cutofftime = models.CharField(max_length=255, null=True, blank=True)
    quantitytemperature = models.CharField(max_length=255, null=True, blank=True)

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
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total_item_price(self):
        return self.quantity * self.product.price
    
    def get_discount_item_price(self):
        return self.quantity * self.product.discount_price
    
    def get_amount_saved(self):
    #     get_total_item_price_float = float(get_total_item_price)
    #     get_discount_item_price_float = float(get_discount_item_price)
        return self.get_total_item_price() - self.get_discount_item_price()
        # return self.get_total_item_price_float() - self.get_discount_item_price_float()
    
    def get_final_price(self):
        if self.product.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()


class Cart(models.Model) :
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    items = models.ManyToManyField(Order)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey('CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.email
    
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class CheckoutAddress(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    zip = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.email


class Payment(models.Model):
    stripe_id = models.CharField(max_length=50)
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email