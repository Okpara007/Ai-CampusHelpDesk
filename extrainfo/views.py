from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import *
from .models import *

# Create your views here.

@login_required(login_url='userschema:signin')
def patient_n_doctor(request):
    form = PatientForm()
    forms = DoctorForm()
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        if request.POST.get('submit') == "patient":
            print(form)
            form = PatientForm()
            if request.method == 'POST':
                form = PatientForm(request.POST)
                if form.is_valid():
                    form = form.save(commit= False)
                    form.user = request.user
                    form.save()
                    return redirect('assistant:index')
            else:
                messages.error(request, form.errors)
                return redirect(url)
    
        elif request.POST.get('submit') == "doctor":
            forms = DoctorForm()
            if request.method == 'POST':
                forms = DoctorForm(request.POST)
                if forms.is_valid():
                    forms = forms.save(commit= False)
                    forms.user = request.user
                    forms.save()
                    return redirect('assistant:index')
            else:
                messages.error(request, forms.errors)
                return redirect(url)

    return render(request, 'info/info.html', {'form': form,'forms': forms,})


@login_required(login_url='userschema:signin')
def appoint(request):
    form = AppointmentForm()
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        dob = request.POST['dob']
        if form.is_valid():
            form = form.save(commit= False)
            form.created_by = request.user
            form.dob = dob
            form.save()
            messages.success(request, "Your Appointment has been submitted!")
            return redirect(url)
        else:
            messages.error(request, form.errors)
            return redirect(url)

    return render(request, 'info/appointment.html', {'form':form})


