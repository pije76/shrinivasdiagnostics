from django.shortcuts import render
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, HttpResponseRedirect, get_object_or_404

from .models import *
from .forms import *
from order.models import *

from bootstrap_modal_forms.generic import BSModalLoginView

# Create your views here.

def create_billingaddress(request):
    page_title = _('Billing Address | ShrinivasDiagnostic')
    form = Add_BillingForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect ('home')
    context = {
        "form":form,
        "page_title": page_title,
    }
    return render(request, 'checkout/add_address.html', context)


def update_billingaddress(request, id):
    post = get_object_or_404(Address, id=id)
    form = Update_BillingForm(instance=post)
    user_id = Profile.objects.get(email=request.user)
    page_title = _('Checkout | ShrinivasDiagnostic')
    user_address = Address.objects.filter(user=user_id)
    print("user_address", user_address)

    if request.method == "POST":
        form = Update_BillingForm(request.POST or None, instance=post)

        if form.is_valid():
            post = Post.objects.get(id=1)
            post.title = "update title"
            form.save()

            messages.success(request, _(page_title + ' form was updated.'))
            return render(request, "checkout/update_address.html", context)
        else:
            messages.warning(request, form.errors)
    else:
        context = {
            "form": form,
            "page_title": page_title,
            "user_address": user_address,
        }

    return render(request, "checkout/update_address.html", context)
