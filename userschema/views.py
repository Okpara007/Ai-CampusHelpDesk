from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib import messages


from .forms import *
from .models import *

# Create your views here.

usermodel = get_user_model()


def signin(request):
    url = request.META.get('HTTP_REFERER')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username = email, password = password)
            if user is None:
                messages.info(request, "Make sure both the username and password is correct")
                return redirect(url)
            elif not user.is_active:
                messages.error(request, "User is not Active.")
                return redirect(url)
                # raise form.ValidationError("User is not Active.")
            else:
                auth_login(request, user, backend='userschema.emailauth.EmailBackend')
                return redirect('assistant:index')
        else:
            messages.error(request, 'Invalid Login Request: Form not valid')
            return redirect(url)
    else:
        return render(request, 'auth/signin.html', {'form':form})

def register(request):
    url = request.META.get('HTTP_REFERER')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user= usermodel.objects.create_user(username = form.cleaned_data['email'], email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
            user.save()
            auth_login(request, user, backend='userschema.emailauth.EmailBackend')
            return redirect('information:patndoc')
        else:
            messages.error(request, form.errors)
            return redirect(url)
    else:
        return render(request, 'auth/register.html', {'form':form})


def loggout(request):
    logout(request)
    return redirect('userschema:signin')


