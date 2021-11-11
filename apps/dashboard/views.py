from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from project.models import Organization

# Create your views here.

@login_required
def organizations(request):

    return render(request, "dashboard/organizations.html")

@login_required
def org(request, id):
    o = Organization.objects.filter(id=id)
    if(not o.exists()):
        return render(request, "dashboard/not_exist.html")
    request.user.profile.organization = o[0]
    request.user.save()
    return render(request, "dashboard/org.html", {"org": o[0]})