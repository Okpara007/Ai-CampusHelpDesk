from django.db import models
from userschema.models import *
# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length = 100)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

STATUS=[
    ('New','New'),
    ('Pending','Pending'),
    ('Process','Process'),
    ('closed','Closed')
]

class Appointment(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fullname= models.CharField(max_length=100, blank=True, null=True)
    services= models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    phone= models.CharField(max_length=100, blank=True, null=True)
    area= models.CharField(max_length=100, blank=True, null=True)
    city= models.CharField(max_length=100, blank=True, null=True)
    state= models.CharField(max_length=100, blank=True, null=True)
    postal= models.CharField(max_length=100, blank=True, null=True)
    email= models.EmailField(max_length=100,blank=True, null=True)
    dob = models.DateField(max_length=200,blank=True, null=True)
    date = models.CharField(max_length=200,blank=True, null=True)
    appt_time = models.CharField(max_length=100,blank=True, null=True)
    symptoms= models.TextField(blank=True, null=True)
    status= models.CharField(max_length=100, choices=STATUS, default='new')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    closed= models.DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return self.created_by.email

        

class Patient(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    full_name = models.CharField(max_length= 100, null= True, blank= True)
    gender = models.ForeignKey(Gender, on_delete = models.CASCADE, null= True, blank= True)
    phone = models.CharField(max_length= 100, null= True, blank= True)
    text = models.TextField(blank=True, null=True)

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}: {self.full_name}'


class Doctor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    full_name = models.CharField(max_length= 100, null= True, blank= True)
    department= models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete = models.CASCADE, null= True, blank= True)
    phone = models.CharField(max_length= 100, null= True, blank= True)
    clinic = models.CharField(max_length= 100, null= True, blank= True)
    address = models.CharField(max_length= 200, null= True, blank= True)
    text = models.TextField(blank=True, null=True)

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.email





