from django.conf import settings

def authenticate(stripe):
    stripe.api_key = settings.stripe_api_key