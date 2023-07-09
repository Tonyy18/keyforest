import stripe
from django.conf import settings
from django.shortcuts import redirect
from lib import parameters
from lib.utils import common
from project.models import Checkout_session

stripe.api_key = settings.STRIPE_APIKEY

def get_session_mode(license):
    #Single payment or recurring subscription
    if(license.subscription_period != None):
        if(license.subscription_type != parameters.License.subscription_types.index("never ending")):
            return "subscription"
    return "payment"

def create_session(request, license):

    if(request.user.stripe_customer_id == None):
        stripe_customers.create(request.user)

    success_url = parameters.Server.url + '/checkout/{CHECKOUT_SESSION_ID}/' + str(license.id) + "/success"
    cancel_url = parameters.Server.url + '/checkout/{CHECKOUT_SESSION_ID}/' + str(license.id) + "/cancelled"
    mode = get_session_mode(license)
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": license.stripe_price_id,
                "quantity": 1
            }
        ],
        mode=mode,
        success_url=success_url,
        cancel_url=cancel_url,
        customer=request.user.stripe_customer_id
    )
    ob = Checkout_session(
        buyer=request.user, 
        product=license,
        created=common.epoch_to_date(session["created"]),
        session_id=session["id"],
        payment_id=session["payment_intent"],
        status=parameters.Stripe.Checkout.Status.open
    )
    ob.save()
    return session

def set_session_completed(data):
    id = data["data"]["object"]["id"]
    try:
        Checkout_session.objects.filter(session_id=id).update(status=parameters.Stripe.Checkout.Status.completed)
    except:
        raise Exception("Failed updating checkout session status id: " + id)

def set_session_expired(data):
    id = data["data"]["object"]["id"]
    try:
        Checkout_session.objects.filter(session_id=id).update(status=parameters.Stripe.Checkout.Status.expired)
    except:
        raise Exception("Failed updating checkout session status, session id: " + id)

def handle_events(data):
    if(data["type"] == "checkout.session.completed"):
        set_session_completed(data)
    if(data["type"] == "checkout.session.expired"):
        set_session_expired(data)

def get_session(id):
    res = stripe.checkout.Session.retrieve(
        id,
    )
    return res