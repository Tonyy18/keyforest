import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_APIKEY

def get_invoice(id):
    return stripe.Invoice.retrieve(
        id,
    )