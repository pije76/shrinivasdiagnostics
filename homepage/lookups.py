from django.db.models import Q

from shop.models import *
from .models import *

# from cities_light.models import City
from selectable.base import ModelLookup
from selectable.registry import registry

class ProductLookup(ModelLookup):
    model = Product
    search_fields = ('title__icontains', )

# @register('productlookup')
# class ProductLookup(LookupChannel):
#     model = Product

#     def get_query(self, q, request):
#         return self.model.objects.filter(title=q)

#     def format_item_display(self, item):
#         return u"<span class='search-container' id='test_search_header_form'>%s</span>" % item.title

# class MarketWidget(s2forms.ModelSelect2Mixin):
# class MarketWidget(ModelLookup):
#     model = MarketDetail
#     search_fields = [
#         # "id__icontains",
#         "ticker_code__icontains",
#     ]
#     # empty_label = "Type & choose..."
#     # dependent_fields = {'location_region': 'region_id'}
#     # max_results = 100

#     def get_item_value(self, item):
#         return item.ticker_name
#         # return "%s" % (item.ticker_name)

#     def get_item_label(self, item):
#         return item.ticker_name
#         # return "%s" % (item.ticker_name)


# # class SectorWidget(s2forms.ModelSelect2Mixin):
# class SectorWidget(ModelLookup):
#     model = MarketSector
#     search_fields = [
#         "title__icontains",
#     ]
#     # dependent_fields = {'location_region': 'region_id'}
#     # max_results = 100


# # class BoardWidget(s2forms.ModelSelect2Mixin):
# class BoardWidget(ModelLookup):
#     model = MarketBoard
#     search_fields = [
#         "title__icontains",
#     ]
#     # dependent_fields = {'location_region': 'region_id'}
#     # max_results = 100

# registry.register(MarketWidget)
# registry.register(SectorWidget)
# registry.register(BoardWidget)
registry.register(ProductLookup)
