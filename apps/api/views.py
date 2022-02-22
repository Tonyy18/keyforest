import abc
from django.shortcuts import render
from django.http import HttpResponse
from project.models import Organization, User_connection
from django.contrib.auth.decorators import login_required
import json
from common import parameters
from datetime import date
from datetime import datetime


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

class _User:
    def organizations(request):
        if(not request.user.is_authenticated):
            return response(Codes.unauthorized)

        if(request.method == "GET"):
            #List all user related organizations
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
                    "added": conn.added.strftime("%d-%m-%Y"),
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
            if(name): name = name.strip()
            if(about): 
                about = about.strip()
            else:
                about = ""
            if(len(name) < parameters.Organization.min_name_length):
                code = Codes.forbidden
                code["error"] = "Organizations name was too short. " + str(parameters.Organization.min_name_length) + " letters minimum"
                return response(code)
            if(len(name) > parameters.Organization.max_name_length):
                code = Codes.forbidden
                code["error"] = "Organizations name was too long. " + str(parameters.Organization.max_name_length) + " letters at max"
                return response(code)
            if(about and len(about) > parameters.Organization.max_bio_length):
                code = Codes.forbidden
                code["error"] = "Organizations description was too long. " + str(parameters.Organization.max_bio_length) + " letters at max"
                return response(code)
            else:
                org_count = len(Organization.objects.filter(creator=request.user))
                if(org_count >= parameters.User.org_count):
                    code = Codes.forbidden
                    code["error"] = "Current user has created maximum amount of organizations (%d)"%org_count
                    return response(code)
                if(Organization.objects.filter(name=name).exists()):
                    code = Codes.forbidden
                    code["error"] = "Organization called '%s' already exists"%name
                    return response(code)
                else:
                    org = Organization(name=name, about=about, creator=request.user)
                    org.save()
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
                        "joined": str(date.today().strftime("%y-%m-%d")),
                        "users": org.users,
                        "applications": org.applications
                    }
                    request.user.profile.organization = org
                    request.user.save()
                    return response(code)

class _Organization:

    def applications(request):
        if(not request.user.is_authenticated):
            return response(Codes.unauthorized)

        if(request.method == "POST"):
            #Create new application

            org_id = request.POST.get("org_id")
            org = None
            if(org_id):
                _org = Organization.objects.filter(id=org_id)
                if(len(_org) > 0):
                    org = _org[0]
            elif(request.user.profile.organization != None):
                org = request.user.profile.organization

            if(org == None):
                code = Codes.bad_request
                code["error"] = "Couldn't solve the target organization"
                return response(code)

            con = User_connection.objects.filter(user=request.user, organization=org)
            if(len(con) == 0):
                code = Codes.unauthorized
                code["error"] = "User is not part of the organization"
                return response(code)
            con = con[0]

            name = request.POST.get("name")
            bio = request.POST.get("bio")
            if(not permission(con, "create_apps")):
                return response(Codes.unauthorized)

            if(name): 
                name = name.strip()
            else:
                code = Codes.forbidden
                code["error"] = "Application name is missing"
                return response(code)
            if(bio):
                bio = bio.strip()
            else:
                bio = ""
            
            if(len(name) < parameters.Application.min_name_length):
                code = Codes.forbidden
                code["error"] = "Application name was too short. " + str(parameters.Application.min_name_length) + " letters minimum"
                return response(code)
            if(len(name) > parameters.Application.max_name_length):
                code = Codes.forbidden
                code["error"] = "Application name was too long. " + str(parameters.Application.max_name_length) + " letters at max"
                return response(code)



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
                results.append({
                    "id": org.id,
                    "name": org.name,
                    "creator": org.creator.first_name + " " + org.creator.last_name,
                    "image": org.image.url,
                })
            code = Codes.ok
            code["data"] = results
        return response(code)
