from project.models import Application, License, Purchase
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
from django.db.models import Count
import collections

def get_apps_sold_in_year(app, until_now=False):
    if(type(app) is not Application):
        app = Application.objects.get(id=app)
        if(len(app) == 0):
            return None
    ob = {}
    #Select all within the current year grouped by months
    purchases = Purchase.objects.filter(date__year=datetime.now().year, product__application=app).annotate(month=TruncMonth('date')).values('month').annotate(c=Count('id')).values('month', 'c')
    for p in purchases:
        ob[str(p["month"].month)] = p["c"]
    until = 13
    if(until_now == True):
        until = datetime.now().month + 1
    for a in range(1, until):
        if(str(a) not in ob):
            ob[str(a)] = 0
    return collections.OrderedDict(sorted(ob.items()))

def get_apps_sold_last_days(app, days=None):
    if(type(app) is not Application):
        app = Application.objects.get(id=app)
    ob = {}
    if(days == None):
        #default
        days = 5
    purchases = Purchase.objects.filter(product__application=app).values("date").annotate(count=Count("id")).order_by("-date")[:days]
    for p in purchases:
        date = p["date"].strftime("%b %d")
        ob[date] = p["count"]
    return ob

def get_licenses_sold_in_year(license, until_now=False):
    if(type(license) is not License):
        license = Application.objects.get(id=license)
    ob = {}
    #Select all within the current year grouped by months
    purchases = Purchase.objects.filter(date__year=datetime.now().year, product=license).annotate(month=TruncMonth('date')).values('month').annotate(c=Count('id')).values('month', 'c')
    for p in purchases:
        ob[str(p["month"].month)] = p["c"]
    until = 13
    if(until_now == True):
        until = datetime.now().month + 1
    for a in range(1, until):
        if(str(a) not in ob):
            ob[str(a)] = 0
    return collections.OrderedDict(sorted(ob.items()))