from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from common.parameters import User
from project.models import Organization, User_connection
from common.utils import is_connected, has_permission
from common.parameters import Permissions
# Create your views here.

def error(request, text):
    return render(request, "dashboard/error.html", {"text": text})

@login_required
def organizations(request):
    if(User_connection.objects.filter(user=request.user).exists()):
        return render(request, "dashboard/organizations.html", {
            "page": "organizations"
        })
    return HttpResponse("You are not part of any organization")

@login_required
def org(request, id):
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
    return render(request, "dashboard/org.html", {
        "page": "summary",
        "edit": edit
    })

@login_required
def applications(request, id):
    if(request.user.organization == None):
        return redirect("/dashboard/organizations")
    con = is_connected(request, id)
    if(not con):
        return error(request, "You are not part of this organization")
    request.user.organization = con.organization
    request.user.save()
    showbtn = has_permission(con, Permissions.Create_apps)
    return render(request, "dashboard/apps.html", {
        "page": "apps",
        "showBtn": showbtn
    })

@login_required
def users(request, id):
    if(request.user.organization == None):
        return redirect("/dashboard/organizations")
    con = is_connected(request, id)
    if(not con):
        return error(request, "You are not part of this organization")
    request.user.organization = con.organization
    request.user.save()
    add_users = has_permission(con, Permissions.Add_users)
    remove_users = has_permission(con, Permissions.Remove_users)

    return render(request, "dashboard/users.html", {
        "page": "users",
        "add_users": add_users,
        "remove_users": remove_users
    })