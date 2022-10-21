import abc
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from project.models import Organization, User_connection, Application, Invitation, User
from lib.utils import *
from django.contrib.auth.decorators import login_required
import json
from lib import parameters,validators
from datetime import date
from datetime import datetime
from django.db.models import Q
from ..views import Codes, response, create_app_dict, create_user_dict, create_org_dict

def organizations(request):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    if(request.method == "GET"):
        #List all user related organizations
        results = []
        connection = User_connection.objects.filter(user=request.user)
        for conn in connection:
            org_dict = create_org_dict(conn.organization)
            org_dict["added"] = str(conn.added)
            results.append(org_dict)
        return response(Codes.ok, results)
        
    if(request.method == "POST"):
        #Create new organization
        name = request.POST.get("name")
        about = request.POST.get("about")
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
                request.user.organization = org
                request.user.save()
                return response(Codes.ok, create_org_dict(org))