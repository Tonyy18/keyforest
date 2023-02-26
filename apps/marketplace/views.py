from django.shortcuts import render
from django.http import HttpResponse
from lib.utils.common import *
from lib.utils import api_utils
import json
# Create your views here.
def market_index(request):
    return render(request, "marketplace/index.html")

def search(request, query):
    data = []
    if(query != None):
        query = query.strip()
        if(query):
            apps = api_utils.find_applications(request, query)
            data = apps
    return render(request, "marketplace/search.html", {
        "query": query,
        "data": json.dumps(data)
    })