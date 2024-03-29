from project.models import User_connection, Organization, Application, User
import uuid
import inspect
from lib import parameters
from time import strftime, localtime
import random
import string
import time
from datetime import datetime

def is_connected(request, id):
    if(type(id) is Organization):
        o = User_connection.objects.filter(organization=id, user=request.user)
    else:
        o = User_connection.objects.filter(organization__id=id, user=request.user)
    if(not o.exists()):
        return False
    return o[0]

def user_is_connected(user,id):
    o = None
    if(type(user) is User):
        if(type(id) is Organization):
            o = User_connection.objects.filter(organization=id, user=user)
        else:
            o = User_connection.objects.filter(organization__id=id, user=user)
    else:
        if(type(id) is Organization):
            o = User_connection.objects.filter(organization=id, user_id=user)
        else:
            o = User_connection.objects.filter(organization__id=id, user_id=user)
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

def has_specific_permission(con, permission):
    per_split = con.permissions.split(",")
    if(inspect.isclass(permission)):
        if(permission.name in per_split):
            return True
    elif(permission in per_split):
        return True
    return False

def random_id():
    return uuid.uuid1()

def has_app_permissions(con, app):
    app_name = app
    if(type(app_name) is Application):
        app_name = app.name
    if(has_permission(con, parameters.Permissions.Access_all_apps) or has_permission(con, "app_" + app_name)):
        return True
    return False

def add_permission(con, permission, save=False):
    if(has_permission(con, parameters.Permissions.All)):
        return con
    if(has_specific_permission(con, permission)):
        #Already has one
        return False
    if(not isinstance(permission, str)):
        #Permission class
        permission = permission.name
    if("," in permission):
        return False
    if(con.permissions.strip() == "" or permission == "*"):
        con.permissions = permission
    else:
        con.permissions = con.permissions + "," + permission
    if(save):
        con.save()
    return con

def is_app_permission(permission):
    permission = permission.strip()
    return permission[0:4] == "app_"

def get_app_perm_name(permission):
    permission = permission.strip()
    if(is_app_permission(permission)):
        return permission[4:len(permission)]
    return False

def add_app_permission(con, app, save=False):
    name = None
    if(type(app) is Application):
        name = app.name
    else:
        name = app
    return add_permission(con, "app_" + name, save)

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

def price_to_scents(price):
    intr = str(price).replace("[0]*$", "")
    if("." in intr):
        sp = intr.split(".")
        if(len(sp) != 2):
            raise Exception("Invalid price format")
        if(len(sp[1]) < 2):
            intr += "0"
    intr = intr.replace(".", "")
    return int(intr)

def epoch_to_date(stamp):
    return strftime('%Y-%m-%d', localtime(stamp))

def epoch_is_expired(epoch):
    epoch = int(epoch)
    current_epoch = int(time.time())
    return (current_epoch - epoch) >= 0 

def cents_to_dollars(num):
    return int(num) / 100

def get_current_date():
    return datetime.date(datetime.now())

def get_random_string(length = 10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

def format_date(date, format = "%d.%m.%Y"):
    return date.strftime(format)