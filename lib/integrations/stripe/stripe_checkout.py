import stripe
from django.conf import settings
from django.shortcuts import redirect
from lib import parameters
from lib.utils import common
from lib import parameters
from lib.integrations.stripe import stripe_customers
from project.models import License
from lib.integrations.stripe.stripe_prices import get_application_fee

stripe.api_key = settings.STRIPE_APIKEY

def get_session_mode(license):
    #Single payment or recurring subscription
    if(license.subscription_period != None):
        if(license.subscription_type != parameters.License.Subscription_period_type.never):
            return "subscription"
    return "payment"

def create_session(request, license: License):

    if(request.user.stripe_customer_id == None):
        stripe_customers.create(request.user)
        
    account_id = license.get_stripe_account().account_id

    success_url = parameters.Server.url + '/checkout/{CHECKOUT_SESSION_ID}/' + str(license.id) + "/success"
    cancel_url = parameters.Server.url + '/checkout/{CHECKOUT_SESSION_ID}/' + str(license.id) + "/cancelled"
    mode = get_session_mode(license)

    #This data is only used on nonrecurring products eg. no subscription
    pay_data = {
        "metadata": {
            "user": request.user.id,
            "product": license.id
        },
        "application_fee_amount": get_application_fee(license),
        "transfer_data": {
            "destination": account_id
        }
    }

    sub_data = {
        "metadata": {
            "user": request.user.id,
            "product": license.id
        },
        "application_fee_percent": get_application_fee(license),
        "transfer_data": {
            "destination": account_id
        }
    }

    if(license.subscription_type != parameters.License.Subscription_period_type.never):
        #Dont use payment_intent_data for subscription purchase
        pay_data = None
    else:
        #Dont use subscription_data for no subscription purchase
        sub_data = None

    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price": license.stripe_price_id,
                "quantity": 1
            }
        ],
        mode=mode,
        success_url=success_url,
        payment_intent_data=pay_data,
        subscription_data=sub_data,
        cancel_url=cancel_url,
        customer=request.user.stripe_customer_id
    )
    return session

def get_session(id):
    res = stripe.checkout.Session.retrieve(
        id,
    )
    return res