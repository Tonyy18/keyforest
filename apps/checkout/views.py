from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lib.utils import api_utils
from lib.integrations.stripe import stripe_checkout

@login_required
def checkoutPage(request, licenseId):
    license = api_utils.get_license_by_id(licenseId, True)
    if(license == None):
        #License not found
        return None
    return render(request, "checkout/checkout_page.html", {"license": license})

def checkoutSuccess(request, sessionId, licenseId):
    try:
        session = stripe_checkout.get_session(sessionId)
        return render(request, "checkout/success.html")
    except:
        pass

def checkoutCancelled(request, sessionId, licenseId):
    return render(request, "checkout/cancelled.html")
