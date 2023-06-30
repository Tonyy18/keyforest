from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from lib.utils import api_utils
from lib.integrations.stripe import stripe_checkout, stripe_customers
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def new_session(request, licenseId):
    license = api_utils.get_license_by_id(licenseId, True)
    if(license == None):
        #License not found
        return None
    url = stripe_checkout.create_session(request, license)
    return redirect(url)

@csrf_exempt
def webhook(request):
    #payment_intent.succeeded link checkout session paymentintent id
    #invoice.payment_succeeded includes product id 
    data = json.loads(request.body)
    if(data["type"] == "payment_intent.succeeded"):
        #not recurring
        pass
    if(data["type"] == "invoice.payment_succeeded"):
        #recurring
        print(data)
        print("")
        print("")
        pass
    return HttpResponse(status=200)