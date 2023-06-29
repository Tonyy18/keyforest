import stripe
from django.conf import settings
from lib.integrations.stripe import stripe_prices
from lib import parameters
stripe.api_key = settings.STRIPE_APIKEY

def create(license):
    print(parameters.Server.url + license.image.url)
    res = stripe.Product.create(
        name=license.name,
        description=license.bio,
        images=[parameters.Server.url + license.image.url]
    )
    return res