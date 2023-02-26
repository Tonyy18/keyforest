import abc
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from project.models import Organization, User_connection, Application, Invitation, User
from lib.utils.common import *
from lib.utils import api_utils
from django.contrib.auth.decorators import login_required
import json
from lib import parameters,validators
from datetime import date
from datetime import datetime
from django.db.models import Q

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
            orgs = Organization.objects.filter(name__icontains=name)
            results = []
            for org in orgs:
                results.append(create_org_dict(org))
            code = Codes.ok
            code["data"] = results
        return response(code)

def applications(request):
    #Search applications by name
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)
    
    if(request.method == "GET"):
        name = request.GET.get("name")
        if(name == None):
            code = Codes.bad_request
            code["error"] = "Applications name is missing"
        else:
            code = api_utils.find_applications(request, name)
        return api_utils.response(code)

