from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from lib.utils import api_utils
from lib.integrations.stripe import stripe_checkout, stripe_customers
from django.views.decorators.csrf import csrf_exempt
import json
from lib import parameters
from lib.integrations.stripe import stripe_checkout, stripe_events, stripe_connect
import stripe
from django.conf import settings
from lib.utils import common
stripe.api_key = settings.STRIPE_APIKEY
from lib.utils.api_utils import Codes, response
from project.models import Stripe_account
from django.shortcuts import render
from apps.checkout import views as checkout_views

@login_required
def new_session(request, licenseId):
    license = api_utils.get_license_by_id(licenseId, True)
    data = {}
    if(license == None):
        #License not found
        data["error"] = "Product does not exist"
        return checkout_views.checkoutPage(request, license, data)

    stripe_account = license.get_stripe_account()
    if(stripe_account == None):
        data["error"] = "Error in organizations payment integrations"
        return checkout_views.checkoutPage(request, license, data)

    session = stripe_checkout.create_session(request, license)
    return redirect(session["url"])

def get_connect_url(request):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    org = common.get_api_org(request)
    if(org == None):
        return response(Codes.bad_request, "Couldn't solve the target organization")
    con = common.is_connected(request, org)
    if(not con):
        return response(Codes.unauthorized, "User is not part of the organization")
    
    if(common.has_permission(con, parameters.Permissions.Stripe_connect) == False):
        return response(Codes.unauthorized)

    if(request.method == "GET"):

        stripe_account = stripe_connect.create_account(org)
        if("id" not in stripe_account):
            return response(Codes.internal, "Internal error: Account id not found in the response")
        account_id = stripe_account["id"]
        link = stripe_connect.link_account(request.user, account_id)
        if("url" not in link):
            return response(Codes.internal, "Internal error: Redirect url not found in the response")

        return response(Codes.ok, link["url"])

def get_all_connected_accounts(request):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    if(request.user.has_role(parameters.Role.Admin) == False):
        return response(Codes.unauthorized, "This endpoint is intended to adminstrations only")

    limit = 100
    limit_param = request.GET.get("limit")
    if(limit_param != None):
        try:
            limit = int(limit_param)
        except:
            pass
    accounts = stripe_connect.get_connected_accounts(limit)
    return response(Codes.ok, accounts["data"])

@csrf_exempt
def webhook(request):
    data = json.loads(request.body)

    try:
        event = stripe.Event.construct_from(
        data, stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    if(data["type"] == "payment_intent.succeeded"):
        if(data["data"]["object"]["invoice"] == None):
            #one time payment. Recurring products has invoices. Here its "none"
            stripe_events.payment_succeeded(data)

    if(data["type"] == "customer.subscription.created"):
        stripe_events.new_subscription(data)

    if(data["type"] == "customer.subscription.updated"):
        stripe_events.update_subscription(data)

    if(data["type"] == "customer.subscription.deleted"):
        stripe_events.subscription_deleted(data)

    if(data["type"] == "invoice.created"):
        stripe_events.new_invoice(data)
    
    if(data["type"] == "invoice.updated"):
        stripe_events.update_invoice(data)

    if(data["type"] == "invoice.payment_failed"):
        pass
        #stripe_events.update_invoice(data)

    if(data["type"] == "account.updated"):
        stripe_events.update_account(data)

    if(data["type"] == "account.application.deauthorized"):
        stripe_events.application_deauthorized(data)

    return HttpResponse(status=200)