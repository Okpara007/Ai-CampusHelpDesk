from django.urls import path
from . import views

app_name = "userschema"


urlpatterns=[
    path('signin/', views.signin, name='signin'),
    # path('google-login-verify/', views.google_verification, name='google_verification'),
    path('register/', views.register, name='register'),
    path('logout/', views.loggout, name='logout'),
]