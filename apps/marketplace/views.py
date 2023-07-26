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
    invoices = api_utils.get_invoices(request.user)

    results = []
    for p in purchases:
        if(p.payment):
            #not a subscription
            results.append({
                "purchase": p
            })
        else:
            #subscription
            res = {"purchase": p, "invoices": []}
            invs = invoices.filter(subscription_stripe_id=p.subscription.stripe_id).order_by("-tk")
            print(len(invs))
            res["invoices"] = invs
            results.append(res)
    
    print(results)

    return render(request, "marketplace/account_page.html", {
        "purchases": results
    })