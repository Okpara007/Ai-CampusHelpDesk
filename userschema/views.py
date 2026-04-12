from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, logout
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render

from .forms import LoginForm, PublicRegisterForm

usermodel = get_user_model()


def signin(request):
    url = request.META.get("HTTP_REFERER")
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username=email, password=password)
            if user is None:
                messages.info(request, "Make sure both the username and password is correct")
                return redirect(url)
            if not user.is_active:
                messages.error(request, "User is not Active.")
                return redirect(url)
            auth_login(request, user, backend="userschema.emailauth.EmailBackend")
            return redirect("assistant:index")

        messages.error(request, "Invalid Login Request: Form not valid")
        return redirect(url)

    return render(request, "auth/signin.html", {"form": form})


def register(request):
    url = request.META.get("HTTP_REFERER")
    form = PublicRegisterForm()
    if request.method == "POST":
        form = PublicRegisterForm(request.POST)
        if form.is_valid():
            user = usermodel.objects.create_user(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            auth_login(request, user, backend="userschema.emailauth.EmailBackend")
            return redirect("assistant:index")

        messages.error(request, form.errors)
        return redirect(url)

    return render(request, "auth/register.html", {"form": form})


def loggout(request):
    logout(request)
    return redirect("userschema:signin")
