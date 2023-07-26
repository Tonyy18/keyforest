from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from lib.utils import api_utils
from lib.integrations.stripe import stripe_checkout, stripe_customers
from django.views.decorators.csrf import csrf_exempt
import json
from project.models import Checkout_session
from lib import parameters
from lib.integrations.stripe import stripe_checkout, stripe_events
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_APIKEY

@login_required
def new_session(request, licenseId):
    license = api_utils.get_license_by_id(licenseId, True)
    if(license == None):
        #License not found
        return None
    session = stripe_checkout.create_session(request, license)
    return redirect(session["url"])

@csrf_exempt
def webhook(request):
    data = json.loads(request.body)

    try:
        event = stripe.Event.construct_from(
        data, stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    
    if(data["type"].startswith("checkout.")):
        stripe_checkout.handle_events(data)

    if(data["type"] == "payment_intent.succeeded"):
        if(data["data"]["object"]["charges"]["data"][0]["invoice"] == None):
            #one time payment. Recurring products has invoices. Here its "none"
            stripe_events.payment_succeeded(data)
            pass

    if(data["type"] == "customer.subscription.created"):
        stripe_events.new_subscription(data)

    if(data["type"] == "customer.subscription.updated"):
        stripe_events.update_subscription(data)

    if(data["type"] == "customer.subscription.deleted"):
        stripe_events.subscription_deleted(data)

    if(data["type"] == "invoice.created"):
        stripe_events.new_invoice(data)
    
    if(data["type"] == "invoice.updated"):
        stripe_events.update_invoice(data)

    if(data["type"] == "invoice.payment_failed"):
        pass
        #stripe_events.update_invoice(data)

    return HttpResponse(status=200)