import stripe
from django.conf import settings
from lib import parameters
from lib.utils import common
stripe.api_key = settings.STRIPE_APIKEY

def get_recurring_data(license):
    #Determines if the stripe product should be recurring or not
    if(license.subscription_type == parameters.License.Subscription_period_type.never):
        raise Exception("Stripe integration: Cannot create recurring price with subscription type: " + str(license.subscription_type) + " (" +  parameters.License.Subscription_period_type.text[license.subscription_type] + ")")
        return
    
    interval = parameters.License.Subscription_period_type.text[license.subscription_type][:-1]
    interval_count = license.subscription_period
    return {
        "interval": interval,
        "interval_count": interval_count
    }

def create(license, product):
    if(license.price == None):
        raise Exception("Stripe integration: Cannot create price object with price value: " + str(license.price))
        return

    price = common.price_to_scents(license.price)
    print("PRICE: " + str(price))
    res = None
    if(license.subscription_type != parameters.License.Subscription_period_type.never):
        recurring_ob = get_recurring_data(license)
        res = stripe.Price.create(
            unit_amount=int(price),
            currency="usd",
            recurring=recurring_ob,
            product=product["id"],
        )
    else:
        res = stripe.Price.create(
            unit_amount=int(price),
            currency="usd",
            product=product["id"],
        )
    return res