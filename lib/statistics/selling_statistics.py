from project.models import Application, License, Purchase
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
from django.db.models import Count

def get_apps_sold_in_year(app):
    if(type(app) is not Application):
        app = Application.objects.filter(id=app)
    ob = {}
    purchases = Purchase.objects.filter(date__year=datetime.now().year, product__application=app).annotate(month=TruncMonth('date')).values('month').annotate(c=Count('id')).values('month', 'c')  #Select all within the current year
    for p in purchases:
        ob[str(p["month"].month)] = p["c"]
    return ob

def get_apps_sold_last_days(app, days=5):
    if(type(app) is not Application):
        app = Application.objects.filter(id=app)
    ob = {}
    start_date = datetime.today() - timedelta(days=days)
    purchases = Purchase.objects.filter(product__application=app, date__gte=start_date)
    for p in purchases:
        date = p.date.strftime("%b %d")
        if(date not in ob):
            ob[date] = 1
        else:
            ob[date] += 1

    return ob