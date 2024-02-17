
from project.models import Application, License
from lib.utils.common import *
from django.db.models import Q
from lib.utils.api_utils import Codes, response
from lib.statistics import selling_statistics

def statistics(request, appid, licenseid):
    if(not request.user.is_authenticated):
        return response(Codes.unauthorized)

    org = get_api_org(request)

    if(org == None):
        return response(Codes.bad_request, "Couldn't solve the target organization")

    con = is_connected(request, org)
    if(not con):
        return response(Codes.unauthorized, "User is not part of the organization")

    license = License.objects.filter(application__organization=org, application=appid, id=licenseid)
    if(not license.exists()):
        return response(Codes.bad_request, "App not found in the organization")
    
    ob = {
        
    }
    stat_type = request.GET.get("type")
    type_value = request.GET.get("value")
    if(type_value):
        try:
            type_value = int(type_value)
        except:
            type_value == None
    if(stat_type):
        stat_type = stat_type.strip().lower()
        #add subtypes
    else:
        ob = selling_statistics.get_licenses_sold_in_year(license[0],until_now=True)

    return response(Codes.ok, ob)