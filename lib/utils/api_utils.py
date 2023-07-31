from project.models import Organization, User_connection, Application, User, License, Purchase, Payment, Subscription, Invoice
from lib.utils.common import *
from django.http import HttpResponse, QueryDict
from lib.integrations.stripe import stripe_subscriptions

import json
class Codes:
    unauthorized = {
        "code": 401,
        "error": "Unauthorized"
    }
    bad_request = {
        "code": 400,
        "error": "Bad request"
    }
    ok = {
        "code": 200,
        "data": {}
    }
    forbidden = {
        "code": 403,
        "error": "Forbidden"
    }
    not_found = {
        "code": 404,
        "error": "Resources was not found"
    }
    internal = {
        "code": 500,
        "error": "Internal server error"
    }

def response(j, message = None):
    if(message != None):
        if(j["code"] == 200):
            j["data"] = message
        else:
            j["error"] = message
    res = HttpResponse(json.dumps(j), content_type="application/json")
    if("code" in j):
        res.status_code = j["code"]
    return res

def create_app_dict(app):
    return {
        "id": app.id,
        "name": app.name,
        "image": app.image.url,
        "bio": app.bio,
        "licenses": app.licenses,
        "organization": create_org_dict(app.organization),
        "creator": create_user_dict(app.creator),
        "created": str(app.created)
    }
def create_org_dict(org):
    return {
        "id": org.id,
        "name": org.name,
        "creator": create_user_dict(org.creator),
        "image": org.image.url,
        "users": org.users,
        "applications": org.applications
    }

def create_user_dict(user):
    return {
        "id": user.id,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "fullname": user.first_name + " " + user.last_name,
        "image": user.image.url
    }

def create_license_dict(lic):
    return {
        "id": lic.id,
        "app": create_app_dict(lic.application),
        "name": lic.name,
        "api_key": str(lic.api_key),
        "bio": lic.bio,
        "parameters": json.loads(lic.parameters),
        "amount": lic.amount,
        "subscription_period": lic.subscription_period,
        "subscription_type": lic.subscription_type,
        "expiration": str(lic.expiration),
        "price": str(lic.price),
        "created": str(lic.created),
        "author": create_user_dict(lic.author)
    }

def create_purchase_dict(purchase):
    return {
        "status": purchase.get_status(),
        "next_invoice": purchase.get_next_invoice_status(),
        "product": create_license_dict(purchase.product),
        "subscription": purchase.subscription != None
    }

def get_applications_by_name(query, limit=None):
    results = []
    if(limit != None):
        try:
            limit = int(limit)
        except:
            limit = 0
        apps = Application.objects.filter(name__icontains=query)[limit:parameters.API.max_app_search]
    else:
        apps = Application.objects.filter(name__icontains=query)
    for app in apps:
        results.append(create_app_dict(app))
    code = Codes.ok
    code["data"] = results
    return code

def get_applications_by_orgId(id, limit=None):
    results = []
    if(limit != None):
        try:
            limit = int(limit)
        except:
            limit = 0
        apps = Application.objects.filter(organization_id=id)[limit:parameters.API.max_org_search]
    else:
        apps = Application.objects.filter(organization_id=id)
    for app in apps:
        results.append(create_app_dict(app))
    code = Codes.ok
    code["data"] = results
    return code

def get_organization_by_id(id):
    try:
        org = Organization.objects.get(id=id)
        return org
    except:
        return None

def get_application_by_id(id):
    try:
        app = Application.objects.get(id=id)
        return app
    except:
        return None

def license_is_valid(license):
    #filter out hidden and expired licenses
    if(license.visible):
        if(license.expiration == None or license.expiration > datetime.date(datetime.now())):
            if(license.amount == None or license.amount > 0):
                return True
    return False

def get_licenses_for_appId(appId, only_valid=False):
    try:
        licenses = License.objects.filter(application=appId)
        if(only_valid == True):
            #Show only licenses that are visible and not expired
            licenses = filter(license_is_valid, licenses)
        return licenses
    except:
        return None

def get_license_by_id(id, only_valid=False):

    try:
        lic = License.objects.get(id=id)
    except:
        return None
    if(only_valid):
        if(license_is_valid(lic)):
            return lic
    else:
        return lic

def get_purchases(user):
    if(isinstance(user, User)):
        user = user.id
    purchases = Purchase.objects.filter(user_id=user).order_by("product__name")
    return purchases

def get_payments(user):
    if(isinstance(user, User)):
        user = user.id
    payments = Payment.objects.filter(user=user).order_by("product__name")
    if(len(payments)):
        return payments
    return None

def get_subscriptions(user):
    if(isinstance(user, User)):
        user = user.id
    subs = Subscription.objects.filter(user=user).order_by("product__name")
    return subs

def get_invoices(user):
    if(isinstance(user, User)):
        user = user.id
    subs = Invoice.objects.filter(user=user).order_by("product__name")
    return subs

def cancel_purchase(p):
    if(isinstance(p, int)):
        try:
            p = Purchase.objects.get(id=p)
        except:
            return response(Codes.bad_request, "Purchase with id (" + str(id) + ") was not found")

    if(not isinstance(p, Purchase)):
        raise Exception("Trying to cancel a purchase without a purchase object")
    
    if(p.subscription == None):
        #one time purchase
        p.status = parameters.Stripe.Purchase.Status.canceled
        p.save()
        return response(Codes.ok, create_purchase_dict(p))
    else:
        try:
            stripe_subscriptions.delete_subscription(p)
            p.subscription.cancel_at_period_end = True
            p.subscription.save()
            p.status == parameters.Stripe.Purchase.Status.canceled
            p.save()
            return response(Codes.ok, create_purchase_dict(p))
        except Exception as e:
            print(str(e))
            return response(Codes.internal, "Integration error")
    
