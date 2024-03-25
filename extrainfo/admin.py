from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register([Gender, Patient, Doctor, Department, Appointment])