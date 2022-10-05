from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.http import JsonResponse

from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet

from .models import *
from .forms import *

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,'shop/product/list.html',{'category': category,'categories': categories,'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_product_form=CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})


class ProductView(DetailView):
    template_name = "product.html"
    model = Product


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(
        content_auto=request.GET.get(
            'query',
            ''))[
        :5]
    s = []
    for result in sqs:
        d = {"value": result.title, "data": result.object.slug}
        s.append(d)
    output = {'suggestions': s}
    return JsonResponse(output)


class FacetedSearchView(BaseFacetedSearchView):

    form_class = FacetedProductSearchForm
    facet_fields = ['category', 'brand']
    template_name = 'search_result.html'
    paginate_by = 3
    context_object_name = 'object_list'
