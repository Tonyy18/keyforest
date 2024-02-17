from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lib.utils import api_utils
from lib.integrations.stripe import stripe_checkout
from lib.utils import common
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from project.models import License

@login_required
def checkoutPage(request, licenseId, extraData=None):
    license = licenseId
    if(type(licenseId) is str or type(licenseId) is int):
        license = api_utils.get_license_by_id(licenseId, True)

    if(license == None or type(license) is not License):
        #License not found
        return HttpResponseNotFound()
    data = {
        "license": license
    }
    if(extraData):
        data = common.merge_two_dicts(data, extraData)
    stripe_account = license.get_stripe_account()
    if(stripe_account == None):
        data["error"] = "Error in organizations payment integrations"
    return render(request, "checkout/checkout_page.html", data)

def checkoutSuccess(request, sessionId, licenseId):
    try:
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
