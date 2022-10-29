import abc
from django.shortcuts import render
from django.http import HttpResponse, QueryDict
from project.models import Organization, User_connection, Application, Invitation, User, License
from lib.utils.common import *
from django.contrib.auth.decorators import login_required
import json
from lib import parameters,validators
from datetime import date
from datetime import datetime
from django.db.models import Q
from ..views import Codes, create_license_dict, response, create_app_dict, create_user_dict, create_org_dict

def licenses(request):
    #List all licenses
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    org = get_api_org(request)

    if(org == None):
        return response(Codes.bad_request, "Couldn't solve the target organization")

    con = is_connected(request, org)
    if(not con):
        return response(Codes.unauthorized, "User is not part of the organization")

    all_licenses = License.objects.filter(application__organization=org)
    results = []
    for lic in all_licenses:
        if(has_app_permissions(con, lic.application)):
            results.append(create_license_dict(lic))
    return response(Codes.ok, results)

def users(request, userid=None):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    org = get_api_org(request)

    if(org == None):
        return response(Codes.bad_request, "Couldn't solve the target organization")

    con = is_connected(request, org)
    if(not con):
        return response(Codes.unauthorized, "User is not part of the organization")

    if(request.method == "GET"):
        name = request.GET.get("name")
        page = request.GET.get("page")
        order = request.GET.get("order")
        try:
            page = int(page)
        except:
            page = 0
            
        conns = User_connection.objects.filter(organization=org)
        if(not order or order==""):
            order = "name" #default filter
                
        if(order == "date"):
            conns = conns.order_by("added")
        results = []
        for connection in conns:
            if(name and name.lower() not in connection.user.first_name.lower() and name.lower() not in connection.user.last_name.lower()):
                continue
            user_dict = create_user_dict(connection.user)
            user_dict["joined"] = str(connection.added)
            results.append(user_dict)
        if(order == "name"):
            results = sorted(results, key=lambda d: d['lastname']) 
        return response(Codes.ok, results)

    if(request.method == "POST"):
        mail = request.POST.get("email");
        if(mail):
            mail = mail.strip()
        else:
            return response(Codes.bad_request, "Email is missing")

        if(not has_permission(con, parameters.Permissions.Add_users)):
            return response(Codes.unauthorized)

        user = None
        try:
            user = User.objects.get(email=mail)
        except:
            user = None
        if(not user):
            return response(Codes.not_found, "User was not found")

        if(User_connection.objects.filter(user=user, organization=org).exists()):
            return response(Codes.bad_request, "User is already in the organization")

        new_con = User_connection(user=user, organization=org)
        new_con.save()
        return response(Codes.ok, create_user_dict(user))

    if(request.method == "DELETE"):
        if(not userid):
            return response(Codes.bad_request, "User id was missing")
        if(not has_permission(con, parameters.Permissions.Remove_users)):
            return response(Codes.unauthorized)

        try:
            userid = int(userid)
        except:
            return response(Codes.bad_request, "Invalid user id")

        if(userid == request.user.id):
            return response(Codes.bad_request, "You can't remove yourself")

        user = None
        try:
            user = User.objects.get(id=userid)
        except:
            user = None

        if(user == None):
            return response(Codes.bad_request, "User doesn't exist")

        user_con = User_connection.objects.filter(user=user, organization=org)
        user_con.delete()
        if(user.organization != None and org.id == user.organization.id):
            user.organization = None
        user.save()
        return response(Codes.ok)

def applications(request):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    org = get_api_org(request)

    if(org == None):
        return response(Codes.bad_request, "Couldn't solve the target organization")

    con = is_connected(request, org)
    if(not con):
        return response(Codes.unauthorized, "User is not part of the organization")

    if(request.method == "POST"):
        #Create new application

        name = request.POST.get("name")
        bio = request.POST.get("bio")
        #Permission handling
        if(not has_permission(con, parameters.Permissions.Create_apps)):
            return response(Codes.unauthorized)

        if(name): 
            name = name.strip()
            if("," in name):
                #Cant use , in name because permissions are separated with , (Messes up permission handling)
                return response(Codes.bad_request, "Character ',' is not allowed in applications name")
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

        app = Application(name=name, organization=org, bio=bio, creator=request.user)
        app.save()
            
        per_added = add_app_permission(con, app)

        if(per_added):
            return response(Codes.ok, create_app_dict(app))
        return response(Codes.internal, "Couldn't add app permissions")

    if(request.method == "GET"):
        #Get all apps in organizations (with permissions)
        apps = Application.objects.filter(organization=org).order_by("created")
        results = [];
        for app in apps:
            if((not has_app_permissions(con, app.name) and not has_permission(con, parameters.Permissions.Access_all_apps))):
                continue

            results.append(create_app_dict(app))
        return response(Codes.ok, results)

def permissions(request, userid):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    org = get_api_org(request)

    if(org == None):
        return response(Codes.bad_request, "Couldn't solve the target organization")

    con = is_connected(request, org)
    if(not con):
        return response(Codes.unauthorized, "User is not part of the organization")

    if(not userid):
        return response(Codes.bad_request, "User id was missing")
            
    user_con = user_is_connected(userid, org)
    if(not user_con):
        return response(Codes.bad_request, "User is not in the organization")

    if(request.method == "POST" or request.method == "UPDATE"):
        method = request.method
        if(method == "POST"):
            perms = request.POST.get("permissions")
        elif(method == "UPDATE"):
            upd_data = QueryDict(request.body)
            perms = upd_data.get("permission")

        if(not perms):
            if(method == "UPDATE"):
                return response(Codes.bad_request, "Permissions missing")
            if(method == "POST"):
                perms = ""
 
        if(not has_permission(con, parameters.Permissions.All)):
            return response(Codes.unauthorized)
            
        if(method == "POST"):
            perms = perms.split(",")
            user_con.permissions = ""
        all_perms = parameters.Permission_groups.All_permissions.by_name
        all_apps = Application.objects.filter(organization=org)
        if(method == "POST"):
            for perm in perms:
                if((not has_permission(user_con, parameters.Permissions.Access_all_apps)) and perm[0:4] == "app_"):
                    #Permission for application
                    app_name = perm[4:len(perm)]
                    app = all_apps.filter(name=app_name)
                    if(len(app) > 0):
                        print(app_name)
                        if(not has_app_permissions(user_con, app_name)):
                            print("ADDED")
                            add_app_permission(user_con, app_name)
                    continue
                #Organization permission
                if(perm in all_perms):
                    #permissions exists
                    if(not has_permission(user_con, all_perms[perm])):
                        add_permission(user_con, perm)
            user_con.save()
        elif(method == "UPDATE"):
            if((not has_permission(user_con, parameters.Permissions.Access_all_apps)) and perms[0:4] == "app_"):
                #Permission for application
                app_name = perms[4:len(perms)]
                app = all_apps.filter(name=app_name)
                if(len(app) > 0):
                    if(not has_app_permissions(user_con, app_name)):
                        add_app_permission(user_con, app_name, True)
            elif(perms in all_perms):
                if(not has_permission(user_con, all_perms[perms])):
                    add_permission(user_con, perms, True)
        return response(Codes.ok)

    if(request.method == "GET"):
        perms = user_con.permissions.split(",")
        res = {
            "general": [],
            "applications":[]
        }
        all_perms = parameters.Permission_groups.All_permissions.by_name
        for perm in perms:
            perm = perm.strip()
            if(is_app_permission(perm)):
                res["applications"].append(get_app_perm_name(perm))
            elif(perm in all_perms):
                res["general"].append(perm)

        return response(Codes.ok, res)