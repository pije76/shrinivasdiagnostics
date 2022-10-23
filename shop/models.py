from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False, db_index=True)
    slug = models.SlugField(max_length=200, unique=True) 
    
    class Meta:
        ordering=('name',)
        verbose_name ='category'
        verbose_name_plural='categories'
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    slug = models.SlugField(max_length=200,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category_product')
    tags = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    # image = models.ImageField(upload_to='prodcuts/%Y/%m/%d',blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
        ordering=('name',)
        index_together=(('id','slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id, self.slug])

