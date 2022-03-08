from project.models import User_connection, Organization
import uuid
import inspect
from . import parameters
def is_connected(request, id):
    if(type(id) is Organization):
        o = User_connection.objects.filter(organization=id, user=request.user)
    else:
        o = User_connection.objects.filter(organization__id=id, user=request.user)
    if(not o.exists()):
        return False
    return o[0]

def has_permission(con, permission):
    per_split = con.permissions.split(",")
    if(inspect.isclass(permission)):
        if(permission.name in per_split or "*" in per_split):
            return True
    elif(permission in per_split or "*" in per_split):
        return True
    return False

def random_id():
    return uuid.uuid1()

def has_app_permissions(con, app_name):
    if(not (has_permission(con, parameters.Permissions.Access_all_apps) or has_permission(con, "app_" + app_name))):
        return False
    return True

def add_permission(con, permission):
    if(has_permission(con, permission)):
        #Already has one
        return False
    if(not isinstance(permission, str)):
        #Permission class
        permission = permission.name

    con.permissions = con.permissions + "," + permission
    con.save()
    return True

def get_api_org(request):
    org_id = None
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
    elif(request.user.organization != None):
        org = request.user.organization

    return org
