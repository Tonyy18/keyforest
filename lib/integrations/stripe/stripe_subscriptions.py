import stripe
from project.models import *
from django.conf import settings
stripe.api_key = settings.STRIPE_APIKEY

def delete_subscription(id):
    if(isinstance(id, Purchase)):
        id = id.subscription.stripe_id
    elif(isinstance(id, Subscription)):
        id = id.stripe_id

    stripe.Subscription.modify(
        id,
        cancel_at_period_end=True
    )