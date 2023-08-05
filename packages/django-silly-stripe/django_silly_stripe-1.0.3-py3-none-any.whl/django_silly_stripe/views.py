import json

import stripe

from django.shortcuts import redirect
from django.http import (
    JsonResponse,
    )
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from django_silly_stripe.conf import SILLY_STRIPE as dss_conf
from django_silly_stripe.helpers import dev_log
from django_silly_stripe.models import (
    Product,
    Price,
    Customer,
    Subscription,
    )

if dss_conf['AUTO_SET'] == 'CLASSIC':
    from django_silly_stripe.views_classic import *

if dss_conf['AUTO_SET'] == 'SPA':
    from django_silly_stripe.views_api import *


@csrf_exempt
def webhook(request):
    if request.method != 'POST':
        return JsonResponse({"message": "Method not allowed"}, status=405)
    stripe_payload = request.body
    dev_log("===WEBHOOK: stripe_payload: ")
    dev_log(stripe_payload)

    try:
        event = stripe.Event.construct_from(
            json.loads(stripe_payload), stripe.api_key
        )
        dev_log("=== event type: ", event.type)
    except ValueError:
        # Invalid payload
        return JsonResponse({"message": "Invalid payload"}, status=400)

    # Handle the event
    match event.type:
        case "customer.subscription.updated":
            sub_id = event.data.object.id
            dev_log(event)
            if not Subscription.objects.filter(id=sub_id).exists():
                sub = Subscription(
                    id=sub_id,
                    customer=Customer.objects.get(id=event.data.object.customer),
                    product=Product.objects.get(id=event.data.object.plan.product),
                    status=event.data.object.status,
                    start_time=event.data.object.current_period_start,
                    end_time=event.data.object.current_period_end,
                    cancel_at_period_end=event.data.object.cancel_at_period_end,
                )
                sub.save()
            else:
                sub = Subscription.objects.get(id=sub_id)
                sub.status = event.data.object.status
                sub.start_time = event.data.object.current_period_start
                sub.end_time = event.data.object.current_period_end
                sub.cancel_at_period_end = event.data.object.cancel_at_period_end
                sub.save()

        case "customer.subscription.deleted":
            sub_id = event.data.object.id
            if Subscription.objects.filter(id=sub_id).exists():
                sub = Subscription.objects.get(id=sub_id)
                sub.delete()

        case _:
            dev_log('Unhandled event type {}'.format(event.type))
            pass

    return JsonResponse({"message": "event handeled"}, status=200)


# ======================================================================
# Admin interface views

@permission_required('is_staff')
def initialize_dss_from_stripe(request):
    """Initializer in the admin interface"""
    Product.objects.all().delete()
    Price.objects.all().delete()
    stripe.api_key = dss_conf["DSS_SECRET_KEY"]
    products = stripe.Product.list(limit=100)
    for product in products:
        new_product = Product(
            id=product.id,
            name=product.name,
            description=product.description,
            metadata=product.metadata,
            images=product.images,
            active=product.active,
        )
        new_product.save()
    prices = stripe.Price.list(limit=100)
    for price in prices:
        new_price = Price(
            id=price.id,
            product=Product.objects.get(id=price.product),
            unit_amount=price.unit_amount,
            currency=price.currency,
            recurring_interval=price.recurring['interval'],
            recurring_interval_count=price.recurring['interval_count'],
            metadata=price.metadata,
            active=price.active,
        )
        new_price.save()
    messages.add_message(
        request, messages.SUCCESS, (
            'Database succesfully updated from Stripe with products and prices'
            )
        )
    return redirect('admin:index')
