from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .forms import RegisterForm, UserAuthenticationForm
# Create your views here.


def register(response):
    user = response.user
    if user.is_authenticated:
        return redirect("home")
    
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "Account/register.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect("home")


def login_view(request):

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:

        print(request.POST)
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():

            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = UserAuthenticationForm()
    return render(request=request, template_name="Account/login.html", context={"form": form})
