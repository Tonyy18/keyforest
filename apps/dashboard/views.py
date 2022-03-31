from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from common.parameters import User
from project.models import Organization, User_connection, Application, License
from common.utils import *
from common.parameters import Permissions
# Create your views here.

def error(request, text):
    return render(request, "dashboard/error.html", {"text": text})

def verify_con(request, id):
    if(request.user.organization == None):
        return {
            "success": False,
            "data": redirect("/dashboard/organizations")
        }
    con = is_connected(request, id)
    if(not con):
        return {
            "success": False,
            "data": error(request, "You are not part of this organization")
        }
    if(request.user.organization != con.organization):
        request.user.organization = con.organization
        request.user.save()
    return {
        "success": True,
        "data": con
     }

def verify_app_access(con, id, app_id):
    app = Application.objects.filter(organization_id = id, id=app_id)
    data =  {
        "success": False,
        "data": HttpResponseNotFound()
    }
    if(not app.exists()):
        return data
    app = app[0]
    if(not has_app_permissions(con, app)):
        return data
    data["success"] = True
    data["data"] = app
    return data

@login_required
def entry(request):
    #Root of dashboard
    if(request.user.organization == None):
        return organizations(request)
    return summary(request, request.user.organization.id)

@login_required
def organizations(request):
    #List all organizations
    if(User_connection.objects.filter(user=request.user).exists()):
        return render(request, "dashboard/organizations.html", {
            "page": "organizations"
        })
    return HttpResponseNotFound()

@login_required
def summary(request, id):
    #specific organization
    con = is_connected(request, id)
    if(request.user.organization == None):
        if(con):
            request.user.organization = con.organization
            request.user.save()
        else:
            return redirect("/dashboard/organizations")
    elif(con):
        request.user.organization = con.organization
        request.user.save()
    if(not con):
        return error(request, "You are not part of this organization")
    edit = has_permission(con, Permissions.Edit_org)
    return render(request, "dashboard/summary.html", {
        "page": "summary",
        "edit": edit
    })

@login_required
def applications(request, id):
    #List applications
    con = verify_con(request, id)
    if(con["success"] == False):
        return con["data"]
    con = con["data"]
    showbtn = has_permission(con, Permissions.Create_apps)
    return render(request, "dashboard/apps.html", {
        "page": "apps",
        "showBtn": showbtn
    })

@login_required
def users(request, id):
    #User management
    con = verify_con(request, id)
    if(con["success"] == False):
        return con["data"]
    con = con["data"]
    add_users = has_permission(con, Permissions.Add_users)
    remove_users = has_permission(con, Permissions.Remove_users)
    edit_perms = has_permission(con, Permissions.All)
    return render(request, "dashboard/users.html", {
        "page": "users",
        "add_users": add_users,
        "remove_users": remove_users,
        "edit_perms": edit_perms
    })

@login_required
def app(request, id, app_id):
    #specific application
    con = verify_con(request, id)
    if(con["success"] == False):
        return con["data"]
    con = con["data"]

    valid_app = verify_app_access(con, id, app_id)
    if(valid_app["success"] == False):
        return error(request, "App not found or you are missing permissions")
    app = valid_app["data"]

    return render(request, "dashboard/application.html", {
        "page": "apps",
        "app": app
    })

@login_required
def new_license(request, id, app_id = None):
    #create license for an application
    con = verify_con(request, id)
    if(con["success"] == False):
        return con["data"]
    con = con["data"]

    if(app_id != None):
        valid_app = verify_app_access(con, id, app_id)
        if(valid_app["success"] == False):
            return error(request, "App not found or you are missing permissions")
        app = valid_app["data"]
    else:
        app = None

    return render(request, "dashboard/new_license.html", {
        "page": "apps",
        "app": app
    })

@login_required
def license(request, id, app_id, lic_id):
    con = verify_con(request, id)
    if(con["success"] == False):
        return con["data"]
    con = con["data"]

    valid_app = verify_app_access(con, id, app_id)
    if(valid_app["success"] == False):
        return error(request, "App not found or you are missing permissions")
    app = valid_app["data"]

    lic = None
    try:
        lic = License.objects.get(application=app, id=lic_id)
    except:
        return error(request, "License not found within the application")
    return render(request, "dashboard/license.html", {
        "page": "licenses",
        "app": app,
        "license": lic
    })

@login_required
def all_licenses(request, id):
    con = verify_con(request, id)
    if(con["success"] == False):
        return con["data"]
    con = con["data"]

    return render(request, "dashboard/all_licenses.html", {
        "page": "licenses"
    })