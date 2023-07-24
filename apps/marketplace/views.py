from django.shortcuts import render
from django.http import HttpResponse
from lib.utils.common import *
from lib.utils import api_utils
from lib.integrations.stripe import stripe_checkout
from datetime import datetime
import json
from django.contrib.auth.decorators import login_required
# Create your views here.
def market_index(request):
    return render(request, "marketplace/index.html")

def searchPage(request, query):
    data = []
    if(query != None):
        query = query.strip()
        if(query):
            apps = api_utils.get_applications_by_name(query)
            data = apps
    return render(request, "marketplace/search_page.html", {
        "query": query,
        "apps": data["data"]
    })

def sellerPage(request, orgId):
    org = api_utils.get_organization_by_id(orgId)
    if(org != None):
        apps = api_utils.get_applications_by_orgId(orgId)
        return render(request, "marketplace/seller_page.html", {
            "org": org,
            "apps": apps["data"]
        })

def appPage(request, orgId, appId):
    org = api_utils.get_organization_by_id(orgId)
    if(org != None):
        app = api_utils.get_application_by_id(appId)
        licenses = []
        if(app != None):
            licenses = api_utils.get_licenses_for_appId(app.id, only_valid=True)
        return render(request, "marketplace/app_page.html", {
            "org": org,
            "app": app,
            "licenses": licenses
        })

@login_required
def accountPage(request):
    purchases = api_utils.get_purchases(request.user)
    payments = api_utils.get_payments(request.user)
    subscriptions = api_utils.get_subscriptions(request.user)
    subs = {}
    sub_payment_ids = []
    results = []
    if(subscriptions):
        for sub in subscriptions:
            if(sub.period_id not in subs):
                subs[sub.period_id] = {"childs": []}
            if("header" not in subs[sub.period_id]):
                subs[sub.period_id]["header"] = sub.payment
            else:
                subs[sub.period_id]["childs"].append(sub.payment)
            sub_payment_ids.append(sub.payment.id)

        for sub in subs:
            results.append(subs[sub])
    
    if(payments):
        for pay in payments:
            if(pay.id not in sub_payment_ids):
                results.append({"header": pay})

    return render(request, "marketplace/account_page.html", {
        "purchases": purchases,
        "payments": results
    })