import abc
from django.shortcuts import render
from django.http import HttpResponse
from project.models import Organization, User_connection, Application
from common.utils import has_permission, is_connected, random_id, has_app_permissions
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
                    "added": str(conn.added),
                    "users": conn.organization.users,
                    "applications": conn.organization.applications
                })
            return response(Codes.ok, results)
        
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
                return response(Codes.forbidden, "Organizations name was too short. " + str(parameters.Organization.min_name_length) + " letters minimum")
            if(len(name) > parameters.Organization.max_name_length):
                return response(Codes.forbidden, "Organizations name was too long. " + str(parameters.Organization.max_name_length) + " letters at max")
            if(about and len(about) > parameters.Organization.max_bio_length):
                return response(Codes.forbidden, "Organizations description was too long. " + str(parameters.Organization.max_bio_length) + " letters at max")
            else:
                org_count = len(Organization.objects.filter(creator=request.user))
                if(org_count >= parameters.User.org_count):
                    return response(Codes.forbidden, "Current user has created maximum amount of organizations (%d)"%org_count)
                if(Organization.objects.filter(name=name).exists()):
                    return response(Codes.forbidden, "Organization called '%s' already exists"%name)
                else:
                    org = Organization(name=name, about=about, creator=request.user)
                    org.save()
                    request.user.profile.organization = org
                    request.user.save()
                    return response(Codes.ok, {
                        "id": org.id,
                        "name": org.name,
                        "creator": {
                            "id": org.creator.id,
                            "name": org.creator.first_name + " " + org.creator.last_name,
                            "image": org.creator.profile.image.url
                        },
                        "image": org.image.url,
                        "joined": str(date.today()),
                        "users": org.users,
                        "applications": org.applications
                    })

class _Organization:

    def applications(request):
        if(not request.user.is_authenticated):
            return response(Codes.unauthorized)

        if(request.method == "POST"):
            org_id = request.POST.get("org_id")
        elif(request.method == "GET"):
            org_id = request.GET.get("org_id")
        org = None
        #If organization exists
        if(org_id):
            _org = Organization.objects.filter(id=org_id)
            if(len(_org) > 0):
                org = _org[0]
        elif(request.user.profile.organization != None):
            org = request.user.profile.organization

        if(org == None):
            return response(Codes.bad_request, "Couldn't solve the target organization")

        con = User_connection.objects.filter(user=request.user, organization=org)
        if(len(con) == 0):
            return response(Codes.unauthorized, "User is not part of the organization")
        con = con[0]

        if(request.method == "POST"):
            #Create new application

            #checking the user connection

            name = request.POST.get("name")
            bio = request.POST.get("bio")
            #Permission handling
            if(not has_permission(con, parameters.Permissions.Create_apps)):
                return response(Codes.unauthorized)

            if(name): 
                name = name.strip()
            else:
                return response(Codes.forbidden, "Application name is missing")
            if(bio):
                bio = bio.strip()
            else:
                bio = ""
            #validation
            if(len(name) < parameters.Application.min_name_length):
                return response(Codes.forbidden, "Application name was too short. " + str(parameters.Application.min_name_length) + " letters minimum")
            if(len(name) > parameters.Application.max_name_length):
                return response(Codes.forbidden, "Application name was too long. " + str(parameters.Application.max_name_length) + " letters at max")
            app_count = Application.objects.filter(organization=org).count()
            if(app_count > parameters.Organization.app_count):
                return response(Codes.forbidden, "Organization has its maximum application amount (" + str(parameters.Organization.app_count) + ")")
            if(Application.objects.filter(organization=org, name=name).exists()):
                return response(Codes.forbidden, "Application called " + name + " already exists in the organization")

            app = Application(name=name, organization=org, api_key=random_id(), bio=bio, creator=request.user)
            app.save()
            return response(Codes.ok, {
                "name": name,
                "bio":bio,
                "organization": {
                    "id": org.id,
                    "name": org.name
                }
            })

        if(request.method == "GET"):
            #Get all apps in organizations (with permissions)
            apps = Application.objects.filter(organization=org).order_by("created")
            results = [];
            for app in apps:
                if(not has_app_permissions(con, app.name)):
                    continue

                results.append({
                    "id": app.id,
                    "name": app.name,
                    "image": app.image.url,
                    "bio": app.bio,
                    "licenses": app.licenses,
                    "organization": {
                        "id": app.organization.id
                    },
                    "creator": {
                        "id": app.creator.id,
                        "name": app.creator.first_name + " " + app.creator.last_name,
                        "image": app.organization.creator.profile.image.url
                    },
                    "created": str(app.created)
                })
            return response(Codes.ok, results)
                    
            

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
