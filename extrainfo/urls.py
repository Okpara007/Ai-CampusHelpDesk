from django.urls import path
from . import views

app_name = "information"


urlpatterns=[
    path('', views.patient_n_doctor, name='patndoc'),
    path('appoint/', views.appoint, name='appointment'),
]