from django.shortcuts import render
from django.http import HttpResponse
from lib.utils.common import *
from lib.utils import api_utils
import json
# Create your views here.
def market_index(request):
    return render(request, "marketplace/index.html")

def searchPage(request, query):
    data = []
    if(query != None):
        query = query.strip()
        if(query):
            apps = api_utils.find_applications(query)
            data = apps
    return render(request, "marketplace/search_page.html", {
        "query": query,
        "data": json.dumps(data)
    })

def sellerPage(request, orgId):
    org = api_utils.get_organization_by_id(orgId)
    if(org != None):
        return render(request, "marketplace/seller_page.html", {
            "org": org
        })
    return render(request, "marketplace/seller_page.html")