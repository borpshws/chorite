from datetime import datetime
import sys
import django
from django.shortcuts import redirect, render

from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("/app/login")
    else:
        return render(request, "app/index.html")
    
def register_request(request):
    if request.method =="POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect("app:home")
        messages.error(request, "Unsuccessful registration")
    form = NewUserForm()
    return render(request, "app/register.html", context={"register_form":form})

def login_request(request):
    '''Request the login form and log the user in if valid'''
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if not user.is_superuser:
                    messages.success(request, f"You are now logged in as {user.username}.")
                else:
                    messages.success(request, f"Welcome, {user.username} The system time is {datetime.now().strftime('%H:%M:%S')}. Installed Python version {sys.version}. Installed Django version {django.get_version()}. This is an administrator account. No errors present at this time.")
                return redirect("app:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "app/login.html", context={"login_form": form})

def logout_request(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("app:home")