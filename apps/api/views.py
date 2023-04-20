import abc
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from project.models import Organization, User_connection, Application, Invitation, User
from lib.utils.common import *
from lib.utils import api_utils
from django.contrib.auth.decorators import login_required
import json
from lib import parameters,validators
from lib.utils import api_utils
from datetime import date
from datetime import datetime
from django.db.models import Q

def permissions(request):
    if(not request.user.is_authenticated):
        return api_utils.response(api_utils.Codes.unauthorized)

    if(request.method == "GET"):
        permissions = parameters.Permission_groups.All_permissions.by_name
        res = []
        for perm in permissions:
            res.append(perm)
        return api_utils.response(api_utils.Codes.ok, res)

def organizations(request):
    if(not request.user.is_authenticated):
        return api_utils.response(api_utils.Codes.unauthorized)

    if(request.method == "GET"):
        #Search organizations by name
        name = request.GET.get("name")
        if(name == None):
            code = api_utils.Codes.bad_request
            code["error"] = "Organization name is missing"
        else:
            orgs = Organization.objects.filter(name__icontains=name)
            results = []
            for org in orgs:
                results.append(api_utils.create_org_dict(org))
            code = api_utils.Codes.ok
            code["data"] = results
        return api_utils.response(code)

def applications(request):
    #Search applications by name
    if(not request.user.is_authenticated):
        return api_utils.response(api_utils.Codes.unauthorized)
    
    if(request.method == "GET"):
        name = request.GET.get("name")
        if(name == None):
            code = api_utils.Codes.bad_request
            code["error"] = "Applications name is missing"
        else:
            code = api_utils.get_applications_by_name(name)
        return api_utils.response(code)

