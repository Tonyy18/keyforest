from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as _logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def logout(request):
    _logout(request)
    return redirect("/")

def landingpage(request):
    return render(request, "index/index.html")

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
        if(len(firstname) < 2):
            data["errors"]["firstname"] = "Firstname is too short"
        elif(len(firstname) > 30):
            data["errors"]["firstname"] = "Firstname is too long"
        else:
            success = success + 1

        if(len(lastname) < 2):
            data["errors"]["lastname"] = "Lastname is too short"
        elif(len(lastname) > 30):
            data["errors"]["lastname"] = "Lastname is too long"
        else:
            success = success + 1

        validEmail = False
        try:
            validate_email(email)
            validEmail = True
        except:
            data["errors"]["email"] = "Invalid email"

        try:
            if(validEmail):
                User.objects.get(email=email)
                data["errors"]["email"] = "Email is already in use"
        except:
            success = success + 1

        if(len(password) < 3):
            data["errors"]["password"] = "Password is too short"
        elif(len(password) > 50):
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
