from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, logout, get_user_model
from django.contrib.auth import login as auth_login


from .forms import *
from .models import *

# Create your views here.

usermodel = get_user_model()


def signin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username = email, password = password)
            if user is None:
                raise forms.ValidationError("User Does Not Exist.")
            elif not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            elif not user.is_active:
                raise forms.ValidationError("User is not Active.")
            else:
                auth_login(request, user, backend='userschema.emailauth.EmailBackend')
                return redirect('assistant:index')
        else:
            form = LoginForm()
            return render(request, 'auth/signin.html', {'form': form})
    else:
        return render(request, 'auth/signin.html', {'form':form})


# def google_verification(request):
#     if request.user.is_authenticated:
#         # Check if the user has a Google social account
#         try:
#             google_account = SocialAccount.objects.get(provider='google', user=request.user)
#             messages.success(request, "You're already signed up with Google.")
#             return redirect('assistant:index')
#         except SocialAccount.DoesNotExist:
#             messages.error(request, "You will have to signup first")
#             return redirect('userschema:register')
#     else:
#             messages.warning(request, "Please do login first")
#             return redirect('userschema:signin')

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user= usermodel.objects.create_user(username = form.cleaned_data['email'], email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
                user.save()
                # user = authenticate(email = request.POST['email'], password = request.POST['password1'])
                auth_login(request, user, backend='userschema.emailauth.EmailBackend')
                return redirect('assistant:index')
            except user.DoesNotExist:
                return Http404
        else:
            error_message = 'Error with password'
            return render(request, 'auth/register.html', {'error_message': error_message})
    else:
        return render(request, 'auth/register.html', {'form':form})


def loggout(request):
    logout(request)
    return redirect('userschema:signin')


