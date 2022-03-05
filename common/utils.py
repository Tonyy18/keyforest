from project.models import User_connection
import uuid
import inspect
from . import parameters
def is_connected(request, id):
    o = User_connection.objects.filter(organization__id=id, user=request.user)
    if(not o.exists()):
        return False
    return o[0]

def has_permission(con, permission):
    per_split = con.permissions.split(",")
    print(permission)
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