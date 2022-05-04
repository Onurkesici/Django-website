from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, "Logged in")
            return redirect("index")
        else:
            messages.add_message(request, messages.ERROR, "Wrong username or wrong password")
            return redirect("login")
    else:
        return render(request, "user/login.html")

def register(request):
    if request.method == "POST":
        
        # get form values
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            # username
            if User.objects.filter(username = username).exists():
                messages.add_message(request, messages.WARNING, "This username is already taken")
                return redirect("register")
            else:
                if User.objects.filter(email = email).exists():
                    messages.add_message(request, messages.WARNING, "This email address has been used before")
                    return redirect("register")
                else:
                    # herşey güzel
                    user = User.objects.create_user(username = username, password = password, email = email)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, "User created")
                    return redirect("login")
        else:       
            messages.add_message(request, messages.WARNING, "Password does not match")
            return redirect("register")
    else:
        return render(request, "user/register.html")

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, "You are logged out.")
    return redirect("index")
