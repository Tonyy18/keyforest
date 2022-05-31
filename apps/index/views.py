from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.validators import validate_email
from project.models import User
from django.contrib.auth import authenticate, login, logout as _logout
from django.contrib.auth.decorators import login_required
from common import parameters
from project.models import User_connection

# Create your views here.
def logout(request):
    _logout(request)
    return redirect("/")

def landingpage(request):
    testbench = False
    dashboard = False
    if(request.user.is_authenticated):
        if(request.user.role in parameters.Role.testbench_access):
            testbench = True
        if(User_connection.objects.filter(user=request.user).exists()):
            dashboard = True
    return render(request, "index/index.html", {
        "testbench": testbench,
        "dashboard": dashboard
    })

def signin(request):
    data = {"error": ""}
    if(request.method == "POST"):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if(user is not None):
            login(request, user)
            if(request.GET.get("next")):
                return redirect(request.GET.get("next"))
            return redirect("/")
        else:
            data["error"] = "Wrong user credentials"

    return render(request, "index/signin.html", data)

def register(request):
    data = {"errors":{}}

    if(request.method == "POST"):
        #form request
        firstname = request.POST.get("firstname")
        data["firstname"] = firstname
        lastname = request.POST.get("lastname")
        data["lastname"] = lastname
        email = request.POST.get("email")
        data["email"] = email
        password = request.POST.get("password")
        data["password"] = password

        success = 0
        if(len(firstname) < parameters.User.min_firstname_length):
            data["errors"]["firstname"] = "Firstname is too short"
        elif(len(firstname) > parameters.User.max_firstname_length):
            data["errors"]["firstname"] = "Firstname is too long"
        else:
            success = success + 1

        if(len(lastname) < parameters.User.min_lastname_length):
            data["errors"]["lastname"] = "Lastname is too short"
        elif(len(lastname) > parameters.User.max_lastname_length):
            data["errors"]["lastname"] = "Lastname is too long"
        else:
            success = success + 1

        validEmail = False
        if(len(email) <= parameters.User.max_email_length):
            try:
                validate_email(email)
                validEmail = True
            except:
                data["errors"]["email"] = "Invalid email"
        else:
            data["errors"]["email"] = "Email is too long"

        try:
            if(validEmail):
                User.objects.get(email=email)
                data["errors"]["email"] = "Email is already in use"
        except:
            success = success + 1

        if(len(password) < parameters.User.min_password_length):
            data["errors"]["password"] = "Password is too short"
        elif(len(password) > parameters.User.max_password_length):
            data["errors"]["password"] = "Password is too long"
        else:
            success = success + 1
        
        if(success == 4):
            #All fields are valid
            user = User(first_name = firstname, last_name=lastname, email=email)
            user.set_password(password)
            user.save()
            return redirect("/")

    return render(request, "index/register.html", data)
