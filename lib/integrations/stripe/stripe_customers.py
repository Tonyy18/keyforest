import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_APIKEY

def create(user):
    try:
        response = stripe.Customer.create(
            email=user.email,
            name=user.first_name + " " + user.last_name
        )
        user.stripe_customer_id = response["id"]
        user.save()
        return user
    except():
        return False
