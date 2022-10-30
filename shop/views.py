from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

# from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
# from haystack.query import SearchQuerySet

from .models import *
from .forms import *

import stripe
stripe.api_key = settings.STRIPE_KEY

def product_list(request, category_slug=None):
    titles = _('Book Blood Test Online in India with Ease with Shrinivas Diagnostics Labs')
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    context = {
        'titles': titles,
        'category': category,
        'categories': categories,
        'products': products,
    }

    # return render(request,'shop/product/list.html',{'category': category,'categories': categories,'products': products})
    return render(request, 'shop/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk, available=True)
    # titles = _('Book Blood Test Online in India with Ease with Shrinivas Diagnostics Labs')
    # titles = product
    cart_product_form=CartAddProductForm()
    # print(cart_product_form)

    context = {
        # 'titles': titles,
        'product': product,
        'cart_product_form': cart_product_form,
    } 

    # return render(request, 'shop/product/product_detail.html', context)
    return render(request, 'shop/product_detail.html', context)

# @login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item, created = Order.objects.get_or_create(product=item, user = request.user, ordered = False)
    order_qs = Cart.objects.filter(user=request.user, ordered= False)

    if order_qs.exists():
        order = order_qs[0]
        
        if order.items.filter(product__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("shopping_cart")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("shopping_cart")
    else:
        ordered_date = timezone.now()
        order = Cart.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("shopping_cart")

# @login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Cart.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=item.pk).exists():
            order_item = Order.objects.filter(product=item, user=request.user, ordered=False)[0]
            order_item.delete()
            # messages.info(request, "Item \""+order_item.product.product_name+"\" remove from your cart")
            return redirect("shopping_cart")
        else:
            # messages.info(request, "This Item not in your cart")
            return redirect("shopping_cart")
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("shopping_cart")

# @login_required
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Cart.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=item.pk).exists():
            order_item = Order.objects.filter(product=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
                messages.info(request, "Item quantity was updated")
            return redirect("shopping_cart")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("shopping_cart")
    else:
        messages.info(request, "You do not have an Order")
        return redirect("shopping_cart")

def get_add_to_cart_url(request, pk):
    return reverse("core:add-to-cart", pk=pk)

# class OrderSummaryView(LoginRequiredMixin, View):
#     def get(self, *args, **kwargs):
#         try:
#             order = Order.objects.get(user=self.request.user, ordered=False)
#             context = {
#                 'object' : order,
#             }
#             return render(self.request, 'shop/shopping_cart.html', context)
#         except ObjectDoesNotExist:
#             messages.error(self.request, "You do not have an order")
#             return redirect("/")

# shopping_cart = OrderSummaryView.as_view()

def shopping_cart(request):
    try:
        order = Cart.objects.get(user=request.user, ordered=False)
        # product = Product.objects.get(user=request.user, order=False)
        products = Product.objects.filter(available=True)
        # print('order', order)
        # get_total_item_price = product.quantity * product.price

# def get_discount_item_price(self):
# return self.quantity * self.product.discount_price

# def get_amount_saved(self):
# get_total_item_price_float = float(get_total_item_price)
# get_discount_item_price_float = float(get_discount_item_price)
# return self.get_total_item_price_float() - self.get_discount_item_price_float()

# def get_final_price(self):
# if self.product.discount_price:
# return self.get_discount_item_price()
# return self.get_total_item_price()

        context = {
            'object': order,
            'products': products,
        }
        return render(request, 'shop/shopping_cart.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "You do not have an order")
        return redirect("/")

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'shop/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(user=self.request.user, street_address=street_address, apartment_address=apartment_address, country=country, zip=zip)
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()
                return redirect('shop:checkout')
            messages.warning(self.request, "Failed Chekout")
            return redirect('shop:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("shopping_cart")

checkout = CheckoutView.as_view()


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Cart.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, "shop/payment.html", context)

    def post(self, *args, **kwargs):
        order = Cart.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total_price() * 100)  #cents

        try:
            charge = stripe.Charge.create(amount=amount, currency="usd", source=token)

            # create payment
            payment = Payment()
            payment.stripe_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total_price()
            payment.save()

            # assign payment to order
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Success make an order")
            return redirect('/')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect('/')

        except stripe.error.RateLimitError as e:
            messages.error(self.request, "To many request error")
            return redirect('/')

        except stripe.error.InvalidRequestError as e:
            messages.error(self.request, "Invalid Parameter")
            return redirect('/')

        except stripe.error.AuthenticationError as e:
            messages.error(self.request, "Authentication with stripe failed")
            return redirect('/')

        except stripe.error.APIConnectionError as e:
            messages.error(self.request, "Network Error")
            return redirect('/')

        except stripe.error.StripeError as e:
            messages.error(self.request, "Something went wrong")
            return redirect('/')
        
        except Exception as e:
            messages.error(self.request, "Not identified error")
            return redirect('/')

checkout = PaymentView.as_view()

# class ProductView(DetailView):
#     template_name = "shop/product.html"
#     model = Product


# def autocomplete(request):
#     sqs = SearchQuerySet().autocomplete(
#         content_auto=request.GET.get(
#             'query',
#             ''))[
#         :5]
#     s = []
#     for result in sqs:
#         d = {"value": result.title, "data": result.object.slug}
#         s.append(d)
#     output = {'suggestions': s}
#     return JsonResponse(output)


# class FacetedSearchView(BaseFacetedSearchView):

#     form_class = FacetedProductSearchForm
#     facet_fields = ['category', 'brand']
#     template_name = 'shop/product/product_search.html'
#     paginate_by = 3
#     context_object_name = 'object_list'
