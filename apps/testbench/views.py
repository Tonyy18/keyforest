from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from common import parameters

# Create your views here.
@login_required
def landingpage(request):
    if(request.user.profile.role in parameters.Role.testbench_access):
        return render(request, "testbench/index.html")