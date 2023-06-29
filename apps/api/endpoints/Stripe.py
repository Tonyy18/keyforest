from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from lib.utils import api_utils
from lib.integrations.stripe import stripe_checkout, stripe_customers

@login_required
def new_session(request, licenseId):
    license = api_utils.get_license_by_id(licenseId, True)
    if(license == None):
        #License not found
        return None
    url = stripe_checkout.create_session(request, license)
    return redirect(url)