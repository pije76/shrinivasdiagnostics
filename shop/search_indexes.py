from django.utils import timezone

from haystack import indexes
from haystack.fields import CharField

from .models import Product

import datetime

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name='/var/www/html/shrinivasdiagnostics/templates/search/indexes/shop/product_text.txt')
    # text = indexes.CharField(document=True, use_template=True)
    # title = indexes.CharField(model_attr='title', faceted=True)
    title = indexes.EdgeNgramField(model_attr='title')
    get_absolute_url = indexes.EdgeNgramField(model_attr='get_absolute_url')
    samplecutoff = indexes.EdgeNgramField(model_attr='samplecutoff')
    report = indexes.EdgeNgramField(model_attr='report')
    speciment = indexes.EdgeNgramField(model_attr='speciment')
    price = indexes.EdgeNgramField(model_attr='price')
    # description = indexes.EdgeNgramField(model_attr="description", null=True)
    # category = indexes.CharField(model_attr='category', faceted=True)

    # We add this for autocomplete.
    title_auto = indexes.EdgeNgramField(model_attr='title')

    # suggestions = indexes.FacetCharField()

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # return self.get_model().objects.filter(available="True")
        return Product.objects.filter(available="True")
