from project.models import User_connection
def permission(request, permission):
    try:
        q = User_connection.objects.get(organization=request.user.profile.organization, user = request.user)
        print("permissions: " + q.permissions)
        if(permission in q.permissions or "*" in q.permissions):
            return True
        return False
    except:
        return False