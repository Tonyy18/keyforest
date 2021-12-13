from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.api.parameters import User
from project.models import Organization, User_connection
from lib import permission
# Create your views here.

def has_connection(request, id):
    o = User_connection.objects.filter(organization__id=id, user=request.user)
    if(not o.exists()):
        return False
    return o[0]

def has_permission(con, permission):
    if(permission in con.permissions or "*" in con.permissions):
        return True
    return False

def error(request, text):
    return render(request, "dashboard/error.html", {"text": text})

@login_required
def organizations(request):
    if(request.user.profile.organization == None):
        return HttpResponse("You're not part of any organization yet")
    return render(request, "dashboard/organizations.html")

@login_required
def org(request, id):
    if(request.user.profile.organization == None):
        return HttpResponse("You're not part of any organization yet")
    con = has_connection(request, id)
    if(not con):
        return error(request, "This site doesn't exist")
    request.user.profile.organization = con.organization
    request.user.save()
    return render(request, "dashboard/org.html", {"data": con})

@login_required
def applications(request, id):
    if(request.user.profile.organization == None):
        return HttpResponse("You're not part of any organization yet")
    con = has_connection(request, id)
    if(not con):
        return error(request, "This site doesn't exist")
    showbtn = False #Create application button
    if(has_permission(con, "create_apps")):
        showbtn = True
    return render(request, "dashboard/apps.html", {"showBtn": showbtn})