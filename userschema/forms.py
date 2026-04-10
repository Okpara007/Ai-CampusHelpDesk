from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email", "role", "password1")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password2"]
        self.fields["email"].widget.attrs.update(
            {
                "class": "w-full px-8 py-3 mb-2 shadow-sm rounded-lg font-medium bg-transparent border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-transparent",
                "placeholder": "Email",
            }
        )
        self.fields["role"].widget.attrs.update(
            {
                "class": "w-full px-8 py-3 mb-2 shadow-sm rounded-lg font-medium bg-transparent border border-gray-200 text-sm focus:outline-none focus:border-gray-400 focus:bg-transparent",
            }
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "password w-full mt-5 px-8 py-3 shadow-sm rounded-lg font-medium bg-transparent border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-transparent",
                "placeholder": "Password",
            }
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error("password1", error)
        return password1


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "role", "linked_student")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "autofocus": True,
                "class": "w-full px-8 py-3 mb-2 shadow-sm rounded-lg font-medium bg-transparent border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-transparent",
                "placeholder": "Email",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": "password w-full mt-5 px-8 py-3 shadow-sm rounded-lg font-medium bg-transparent border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-transparent",
                "placeholder": "Password",
            }
        )
