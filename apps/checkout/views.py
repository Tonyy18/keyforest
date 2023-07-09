from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lib.utils import api_utils
from lib.integrations.stripe import stripe_checkout
from lib.utils import common

@login_required
def checkoutPage(request, licenseId, extraData=None):
    license = api_utils.get_license_by_id(licenseId, True)
    if(license == None):
        #License not found
        return None
    data = {
        "license": license,
    }
    if(extraData):
        data = common.merge_two_dicts(data, extraData)
    return render(request, "checkout/checkout_page.html", data)

def checkoutSuccess(request, sessionId, licenseId):
    try:
        session = stripe_checkout.get_session(sessionId)
        return render(request, "checkout/success.html")
    except:
        pass

def checkoutCancelled(request, sessionId, licenseId):
    return checkoutPage(request, licenseId, extraData={
        "status": {
            "type": "error",
            "message": "The session was cancelled"
        }
    })
