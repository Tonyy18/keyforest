from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from lib.parameters import User
from project.models import Organization, User_connection, Application, License, Stripe_account
from lib.utils.common import *
from lib.utils import api_utils
from lib.parameters import Permissions
from lib.integrations.stripe import stripe_connect, stripe_event_objects
from stripe.error import PermissionError
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

    default_stripe_account = None
    stripe_accounts = Stripe_account.objects.filter(organization=con.organization)
    stripe_usable = []
    for acc in stripe_accounts:
        if(acc.is_usable() == False):
            continue
        if(acc.default == True):
            default_stripe_account = acc
        stripe_usable.append(acc)

    return render(request, "dashboard/new_license.html", {
        "page": "apps",
        "app": app,
        "default_stripe_account": default_stripe_account,
        "stripe_accounts": stripe_usable
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
    except License.DoesNotExist:
        return error(request, "License not found within the application")
    amount_sold = api_utils.get_licenses_sold(lic)
    active = api_utils.get_licenses_activated(lic)
    return render(request, "dashboard/license.html", {
        "page": "licenses",
        "app": app,
        "license": lic,
        "data": {
            "amount_sold": amount_sold,
            "active": active
        }
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

@login_required
def stripe(request, id):
    con = verify_con(request, id)
    if(con["success"] == False):
        return con["data"]
    con = con["data"]
    if(has_permission(con, Permissions.Stripe_connect) == False):
        return error(request, "You dont have required permissions")
    
    if(request.method == "POST"):
        #set stripe account as default for organization
        default_acc_param = request.POST.get("default_account")
        if(default_acc_param != None):
            default_account = Stripe_account.objects.filter(organization=request.user.organization, default=True)
            #Invalidate previous defaults
            default_account.update(default=False)
            #Set new as default
            new_default_account = Stripe_account.objects.filter(organization=request.user.organization, account_id=default_acc_param)
            new_default_account.update(default=True)

    accounts = Stripe_account.objects.filter(organization=request.user.organization)
    active = []
    disabled = []

    default_found = False
    for account in accounts:
        if(account.default == True):
            default_found = True
        account.convert_json_fields()
        if(account.is_usable()):
            if(account.default == True):
                active.insert(0, account)
                continue
            active.append(account)
        else:
            disabled.append(account)

    data = {
        "page": "stripe",
        "active_accounts": active,
        "disabled_accounts": disabled,
        "default_found": default_found
    }

    return render(request, "dashboard/stripe.html", data)