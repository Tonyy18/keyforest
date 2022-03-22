import abc
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from project.models import Organization, User_connection, Application, Invitation, User, License
from common.utils import *
from django.contrib.auth.decorators import login_required
import json
from common import parameters,validators
from datetime import date
from datetime import datetime
from django.db.models import Q
from ..views import Codes, response, create_app_dict, create_user_dict, create_org_dict

def license(request):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    org = get_api_org(request)

    if(org == None):
        return response(Codes.bad_request, "Couldn't solve the target organization")

    con = is_connected(request, org)
    if(not con):
        return response(Codes.unauthorized, "User is not part of the organization")

    if(request.method == "POST"):
        appid = request.POST.get("app_id")
        if(not appid):
            return response(Codes.bad_request, "App id is missing")
        app = Application.objects.filter(organization=org, id=appid)
        if(not app.exists()):
            return response(Codes.bad_request, "App not found in the organization")
        
        app = app[0]
        if(not has_app_permissions(con, app.name)):
            return response(Codes.unauthorized, "You dont have permissions for this application")
        
        name = request.POST.get("name")
        if(name):
            name = name.strip()
        amount = request.POST.get("amount")
        if(amount):
            amount = amount.strip()
        expiration = request.POST.get("expiration")
        if(expiration):
            expiration = expiration.strip()
        price = request.POST.get("price")
        if(price):
            price = price.strip()
        duration = request.POST.get("duration")
        if(duration):
            duration = duration.strip()
        desc = request.POST.get("desc")
        if(desc):
            desc = desc.strip()
        params = request.POST.get("params")
        if(params):
            params = params.strip()
        #Validation
        if(len(name) < parameters.License.min_name_length):
            return response(Codes.bad_request, "License name is too short")
        if(len(name) > parameters.License.max_name_length):
            return response(Codes.bad_request, "License name is too long")
        
        if(len(desc) > parameters.License.max_bio_length):
            return response(Codes.bad_request, "License description is too long")
        
        lic = License.objects.filter(application=app, name=name)
        if(lic.exists()):
            return response(Codes.bad_request, "License with the same name already exists")
        
        ob = License(application=app, name=name)

        if(amount):
            try:
                amount = int(amount)
            except:
                return response(Codes.bad_request, "Invalid amount argument")
            if(amount < 1):
                return response(Codes.bad_request, "Amount cannot be less than 1")

            ob.amount = amount

        if(expiration):
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
                
        if(duration):
            try:
                duration = int(duration)
            except:
                return response(Codes.bad_request, "Invalid duration argument")
            if(duration < 1):
                return response(Codes.bad_request, "Duration cannot be less than 1")

            ob.duration = duration

        if(price):
            try:
                price = float(price)
            except:
                return response(Codes.bad_request, "Invalid price argument")

            ob.price = price

        if(desc):
            ob.bio = desc

        if(params):
            try:
                params = json.loads(params)
            except:
                return response(Codes.bad_request, "Invalid parameters argument")
            if(len(params) > parameters.License.parameter_count):
                return response(Codes.bad_request, "Too many parameters. maximum of " + str(parameters.License.parameter_count))
            for key in params:
                if(len(key) > parameters.License.parameter_name_max_length):
                    return response(Codes.bad_request, "One of the parameter names is too long")
                if(len(params[key]) > parameters.License.parameter_value_max_length):
                    return response(Codes.bad_request, "One of the parameter values is too long")
            ob.parameters = json.dumps(params)

        ob.visible = True
        ob.api_key = random_id()
        ob.save()
        return response(Codes.ok)
        

        