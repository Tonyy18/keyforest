from project.models import User_connection

def has_connection(request, id):
    o = User_connection.objects.filter(organization__id=id, user=request.user)
    if(not o.exists()):
        return False
    return o[0]

def has_permission(con, permission):
    if(permission in con.permissions or "*" in con.permissions):
        return True
    return False