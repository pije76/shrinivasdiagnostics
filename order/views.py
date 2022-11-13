from django.shortcuts import render
from django.conf import settings

from .models import *

import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# Create your views here.
def my_orders(request):
    context = {
        # 'page_title': page_title,
        # 'form': form,
    }

    return render(request, 'shop/order.html', context)


def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "order/payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    return render(request, "order/payment.html")
