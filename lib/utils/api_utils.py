from project.models import Organization, User_connection, Application, Invitation, User
from lib.utils.common import *
from django.http import HttpResponse, QueryDict
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
        "created": str(app.created),
        "reputation": app.reputation
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
        "duration": lic.duration,
        "expiration": str(lic.expiration),
        "price": lic.price,
        "created": str(lic.created),
        "author": create_user_dict(lic.author)
    }

def find_applications(request, query, limit=None):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)
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