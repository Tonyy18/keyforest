import stripe
from django.conf import settings
from django.shortcuts import redirect
from lib import parameters

stripe.api_key = settings.STRIPE_APIKEY
def create_session(request, license):

    if(request.user.stripe_customer_id == None):
        stripe_customers.create(request.user)

    price = str(license.price)
    price = price.replace(".", "")
    success_url = parameters.Server.url + '/checkout/{CHECKOUT_SESSION_ID}/' + str(license.id) + "/success"
    cancel_url = parameters.Server.url + '/checkout/{CHECKOUT_SESSION_ID}/' + str(license.id) + "/cancelled"
    session = stripe.checkout.Session.create(
        line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
            'name': license.name,
            },
            'unit_amount': int(price),
        },
        'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        customer=request.user.stripe_customer_id
    )
    return session.url

def get_session(id):
    res = stripe.checkout.Session.retrieve(
        id,
    )
    return res