from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm 
from django.contrib.auth import password_validation, authenticate
from django import forms
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        del self.fields["password2"]
        self.fields["email"].widget.attrs.update({"class": "w-full px-8 py-3 mb-2 shadow-sm rounded-lg font-medium bg-transparent border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-transparent", "placeholder": "Email"})
        self.fields["password1"].widget.attrs.update({"class": "password w-full mt-5 px-8 py-3 shadow-sm rounded-lg font-medium bg-transparent border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-transparent", "placeholder": "Password"})

    class Meta:
        model = CustomUser
        fields = ('email', 'password1')
        
    def clean_password1(self): # Check that the two password entries match 
        password1 = self.cleaned_data.get("password1") 
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:

            # Method inherited from BaseForm
            self.add_error('password1', error)
        return password1

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.password = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({'autofocus': True, "class": "w-full px-8 py-3 mb-2 shadow-sm rounded-lg font-medium bg-transparent border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-transparent", "placeholder": "Email"})
        self.fields["password"].widget.attrs.update({"class": "password w-full mt-5 px-8 py-3 shadow-sm rounded-lg font-medium bg-transparent border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-transparent", "placeholder": "Password"})
    
    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")

    #     if email and password:
    #         self.user = authenticate(email=email, password=password)

    #         if self.user is None:
    #             raise forms.ValidationError("User Does Not Exist.")
    #         if not self.user.check_password(password):
    #             raise forms.ValidationError("Password Does not Match.")
    #         if not self.user.is_active:
    #             raise forms.ValidationError("User is not Active.")

    #     return super(LoginForm, self).clean(*args, **kwargs)

    # def get_user(self):
    #     return self.user




# def my_login_view(request):
#     form = LoginForm(request.POST)
#     if form.is_valid():
#         username = form.cleaned_data["username"]
#         password = form.cleaned_data["password"]
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('/Skolar/')
#             return HttpResponse('<h1>Page was found</h1>')
#         return render(request, "login.html", {'form': form})
#     return render(request, "login.html", {'form': form})



