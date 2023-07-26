import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_APIKEY

def create(user):
    try:
        if(settings.DEBUG==True):
            #Use stripe test clock
            #We can adjust the time from dashboard to test subscriptions
            response = stripe.Customer.create(
                email=user.email,
                name=user.first_name + " " + user.last_name,
                test_clock="clock_1NY7RtI0rEDBXFZNASIGQuQi"
            )
        else:
            response = stripe.Customer.create(
                email=user.email,
                name=user.first_name + " " + user.last_name
            )
        user.stripe_customer_id = response["id"]
        user.save()
        return user
    except:
        return False
