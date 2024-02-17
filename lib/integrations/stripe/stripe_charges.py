import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_APIKEY

def get_charge(id):
    return stripe.Charge.retrieve(id)