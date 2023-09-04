import abc
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from project.models import Application, License, Purchase
from lib.utils.common import *
from django.contrib.auth.decorators import login_required
import json
from lib import parameters,validators
from datetime import date
from datetime import datetime
from django.db.models import Q
from lib.utils.api_utils import Codes, response, create_app_dict, create_user_dict, create_org_dict, create_license_dict
from lib.integrations.stripe import stripe_products, stripe_prices
import traceback
from django.db.models.functions import TruncMonth
from django.db.models import Count
from lib.statistics import selling_statistics

def licenses(request, appid):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    org = get_api_org(request)

    if(org == None):
        return response(Codes.bad_request, "Couldn't solve the target organization")

    con = is_connected(request, org)
    if(not con):
        return response(Codes.unauthorized, "User is not part of the organization")

    if(not appid):
        return response(Codes.bad_request, "App id is missing")

    app = Application.objects.filter(organization=org, id=appid)
    if(not app.exists()):
        return response(Codes.bad_request, "App not found in the organization")

    app = app[0]
    if(not has_app_permissions(con, app.name)):
        return response(Codes.unauthorized, "You dont have permissions for this application")

    if(request.method == "GET"):
        lics = License.objects.filter(application=app)
        results = []
        for lic in lics:
            results.append(create_license_dict(lic))
        return response(Codes.ok, results)

    if(request.method == "POST"):
        name = request.POST.get("name")
        if(name):
            name = name.strip()
        amount = request.POST.get("amount")
        expiration = request.POST.get("expiration")
        price = request.POST.get("price")
        subscription_period = request.POST.get("subscription_period")
        subscription_type = request.POST.get("subscription_type")
        desc = request.POST.get("desc")
        if(desc):
            desc = desc.strip()
        params = request.POST.get("params")
        #Validation
        if(len(name) < parameters.License.min_name_length):
            return response(Codes.bad_request, "License name is too short")
        if(len(name) > parameters.License.max_name_length):
            return response(Codes.bad_request, "License name is too long")
        
        if(len(desc) > parameters.License.max_bio_length):
            return response(Codes.bad_request, "License description can only be " + str(parameters.License.max_bio_length) + " character long")
        
        lic = License.objects.filter(application=app, name=name)
        if(lic.exists()):
            return response(Codes.bad_request, "License with the same name already exists")
        
        ob = License(application=app, name=name, author=request.user)

        if(amount):
            amount = amount.strip()
            try:
                amount = int(amount)
            except:
                return response(Codes.bad_request, "Invalid amount argument")
            if(amount < 1):
                return response(Codes.bad_request, "Amount cannot be less than 1")

            if(amount > parameters.License.max_amount):
                return response(Codes.bad_request, "Amount is too high")

            ob.amount = amount

        if(expiration):
            expiration = expiration.strip()
            sp = expiration.split("-")
            exp_err = None
            if(len(sp) != 3):
                exp_err = "Invalid expiration date format"

            exp_date = None
            try:
                exp_date = date(int(sp[0]), int(sp[1]), int(sp[2]))
            except:
                exp_err = "Invalid expiration date format"
            if(exp_err != None):
                return response(Codes.bad_request, exp_err)
            
            ob.expiration = exp_date

        if(price):
            price = price.strip()
            price = price.replace(",",".")
            try:
                price = float(price)
            except:
                return response(Codes.bad_request, "Invalid price argument")

            price_str = str(price)
            if("." in price_str):
                sp = price_str.split(".")
                if(len(sp[1]) > 2):
                    return response(Codes.bad_request, "Invalid price argument")

            if(float(price) < parameters.License.min_price):
                return response(Codes.bad_request, "Minimum price is " + str(parameters.License.min_price) + "$")
            elif(price >= parameters.License.min_price):
                if(price > parameters.License.max_price):
                    return response(Codes.bad_request, "Price is too high")
                else:
                    ob.price = price
            else:
                ob.price = None
        else:
            return response(Codes.bad_request, "Minimum price is " + str(parameters.License.min_price) + "$")

        if(subscription_period):
            subscription_period = subscription_period.strip()
            try:
                subscription_period = int(subscription_period)
            except:
                return response(Codes.bad_request, "Invalid subscription period argument")

            if(subscription_period > parameters.License.max_subscription_period):
                return response(Codes.bad_request, "Subscription period is too long")
            
            if(subscription_period < 1):
                subscription_period = None

            ob.subscription_period = subscription_period
            
            if(subscription_period != None):
                if(ob.price == None):
                    return response(Codes.bad_request, "Subscription cannot be set without a price")
                if(not subscription_type):
                    return response(Codes.bad_request, "Subscription type is missing")
                try:
                    subscription_type = int(subscription_type)
                except:
                    return response(Codes.bad_request, "Invalid subscription type argument")
                if(len(parameters.License.Subscription_period_type.text) - 1 < subscription_type):
                    return response(Codes.bad_request, "Invalid subscription type argument")
                ob.subscription_type = subscription_type
            else:
                ob.subscription_type = 0

        if(desc):
            ob.bio = desc

        if(params):
            params = params.strip()
            try:
                params = json.loads(params)
            except:
                return response(Codes.bad_request, "Invalid parameters argument")
            if(len(params) > parameters.License.max_parameter_count):
                return response(Codes.bad_request, "Too many parameters. maximum of " + str(parameters.License.parameter_count))
            for key in params:
                if(len(key) > parameters.License.max_parameter_name_length):
                    return response(Codes.bad_request, "One of the parameter names is too long")
                if(len(params[key]) > parameters.License.max_parameter_value_length):
                    return response(Codes.bad_request, "One of the parameter values is too long")
            ob.parameters = json.dumps(params)

        ob.visible = True

        try:
            stripe_prod = stripe_products.create(ob)
            ob.stripe_product_id = stripe_prod["id"]

            stripe_pre = stripe_prices.create(ob, stripe_prod)
            ob.stripe_price_id = stripe_pre["id"]
        except Exception as e:
            print(traceback.format_exc())
            return response(Codes.internal, "Internal integration error")
        ob.save()
        return response(Codes.ok, create_license_dict(ob))

def statistics(request, appid):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    org = get_api_org(request)

    if(org == None):
        return response(Codes.bad_request, "Couldn't solve the target organization")

    con = is_connected(request, org)
    if(not con):
        return response(Codes.unauthorized, "User is not part of the organization")

    app = Application.objects.filter(organization=org, id=appid)
    if(not app.exists()):
        return response(Codes.bad_request, "App not found in the organization")
    
    ob = {
        
    }
    stat_type = request.GET.get("type")
    type_value = request.GET.get("value")
    if(type_value):
        try:
            type_value = int(type_value)
        except:
            type_value == None
    if(stat_type):
        stat_type = stat_type.strip().lower()
        if(stat_type == "lastdays"):
            days = 300
            if(type_value):
                days = type_value
            ob = selling_statistics.get_apps_sold_last_days(app[0], days)
    else:
        ob = selling_statistics.get_apps_sold_in_year(app[0])

    return response(Codes.ok, ob)

    