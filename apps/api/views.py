from django.shortcuts import render
from django.http import HttpResponse
from project.models import Organization, User_connection
from django.contrib.auth.decorators import login_required
import json
from . import parameters

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

def response(j):
    res = HttpResponse(json.dumps(j), content_type="application/json")
    if("code" in j):
        res.status_code = j["code"]
    return res

class User:
    def organizations(request):
        if(not request.user.is_authenticated):
            return response(Codes.unauthorized)

        if(request.method == "GET"):
            results = []
            connection = User_connection.objects.filter(user=request.user)
            for conn in connection:
                results.append({
                    "id": conn.organization.id,
                    "name": conn.organization.name,
                    "creator": {
                        "id": conn.organization.creator.id,
                        "name": conn.organization.creator.first_name + " " + conn.organization.creator.last_name,
                        "image": conn.organization.creator.profile.image.url
                    },
                    "image": conn.organization.image.url,
                    "joined": str(conn.added),
                    "users": conn.organization.users,
                    "applications": conn.organization.applications
                })
            code = Codes.ok
            code["data"] = results
            return response(code)
        
        if(request.method == "POST"):
            #Create new organization
            name = request.POST.get("name")
            about = request.GET.get("about")
            if(len(name) < parameters.Organization.min_name_length):
                code = Codes.forbidden
                code["error"] = "Organizations name was too short. " + str(parameters.Organization.min_name_length) + " letters minimum"
                return response(code)
            if(len(name) > parameters.Organization.max_name_length):
                code = Codes.forbidden
                code["error"] = "Organizations name was too long. " + str(parameters.Organization.max_name_length) + " letters at max"
                return response(code)
            else:
                org_count = len(Organization.objects.filter(creator=request.user))
                if(org_count >= parameters.User.org_count):
                    code = Codes.forbidden
                    code["error"] = "Current user has created maximum amount of organizations (%d)"%org_count
                    return response(code)
                if(Organization.objects.filter(name=name).exists()):
                    code = Codes.forbidden
                    code["error"] = "Organizations called '%s' already exists"%name
                    return response(code)
                else:
                    org = Organization(name=name, creator=request.user)
                    org.save()
                    connection = User_connection(user=request.user, organization=org)
                    connection.save()
                    code = Codes.ok
                    code["data"] = {
                        "id": org.id,
                        "name": org.name,
                        "creator": {
                            "id": org.creator.id,
                            "name": org.creator.first_name + " " + org.creator.last_name,
                            "image": org.creator.profile.image.url
                        },
                        "image": org.image.url,
                        "joined": str(connection.added),
                        "users": org.users,
                        "applications": org.applications
                    }
                    request.user.profile.organization = org
                    request.user.save()
                    return response(code)

def organizations(request):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    if(request.method == "GET"):
        #Search organizations by name
        name = request.GET.get("name")
        max_results = parameters.Server.max_org_search
        if(name == None):
            code = Codes.bad_request
            code["error"] = "Organization name is missing"
        else:
            limit = request.GET.get("limit")
            try:
                limit = int(limit)
                if(limit > max_results):
                    limit = max_results
            except:
                limit = max_results
            orgs = Organization.objects.filter(name__icontains=name)[0:limit]
            results = []
            for org in orgs:
                results.append({
                    "id": org.id,
                    "name": org.name,
                    "creator": org.creator.first_name + " " + org.creator.last_name,
                    "image": org.image.url,
                })
            code = Codes.ok
            code["data"] = results
        return response(code)
