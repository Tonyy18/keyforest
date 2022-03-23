import abc
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from project.models import Organization, User_connection, Application, Invitation, User
from common.utils import *
from django.contrib.auth.decorators import login_required
import json
from common import parameters,validators
from datetime import date
from datetime import datetime
from django.db.models import Q

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
        "api_key": lic.api_key,
        "bio": lic.bio,
        "parameters": json.loads(lic.parameters),
        "amount": lic.amount,
        "duration": lic.duration,
        "expiration": str(lic.expiration),
        "price": lic.price,
        "created": lic.created,
        "author": create_user_dict(lic.author)
    }

def permissions(request):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    if(request.method == "GET"):
        permissions = parameters.Permission_groups.All_permissions.by_name
        res = []
        for perm in permissions:
            res.append(perm)
        return response(Codes.ok, res)

def organizations(request):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    if(request.method == "GET"):
        #Search organizations by name
        name = request.GET.get("name")
        if(name == None):
            code = Codes.bad_request
            code["error"] = "Organization name is missing"
        else:
            limit = request.GET.get("limit")
            try:
                limit = int(limit)
            except:
                limit = 0
                
            orgs = Organization.objects.filter(name__icontains=name)[limit:parameters.API.max_org_search]
            results = []
            for org in orgs:
                results.append(create_org_dict(org))
            code = Codes.ok
            code["data"] = results
        return response(code)
