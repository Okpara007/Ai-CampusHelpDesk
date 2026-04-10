from django import forms

from userschema.models import CustomUser

from .models import Announcement, Appointment, AssessmentRecord, Doctor, FAQEntry, Patient, StudentResource


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["full_name", "gender", "phone", "text"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "bg-transparent border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "PlaceHolder": "Full name",
                    "required": True,
                }
            ),
            "gender": forms.Select(
                attrs={
                    "class": "bg-[#0F162B] border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "PlaceHolder": "Gender",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "bg-transparent border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "PlaceHolder": "(000) 000-000",
                    "required": True,
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "block p-2.5 w-full text-sm text-gray-500 bg-transparent rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "placeholder": "what do you plan on using Medicalasst for?...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].empty_label = "Gender"


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["full_name", "department", "gender", "phone", "clinic", "address", "text"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "bg-transparent border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "PlaceHolder": "Full name",
                    "required": True,
                }
            ),
            "department": forms.Select(
                attrs={
                    "class": "bg-[#0F162B] border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "PlaceHolder": "Specialty",
                    "required": True,
                }
            ),
            "gender": forms.Select(
                attrs={
                    "class": "bg-[#0F162B] border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "PlaceHolder": "Gender",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "bg-transparent border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "PlaceHolder": "(000) 000-000",
                    "required": True,
                }
            ),
            "clinic": forms.TextInput(
                attrs={
                    "class": "bg-transparent border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "PlaceHolder": "clinic name",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "bg-transparent border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "PlaceHolder": "Clinic address",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "block p-2.5 w-full text-sm text-gray-500 bg-transparent rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "placeholder": "what do you plan on using Medicalasst for?...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].empty_label = "Services"
        self.fields["gender"].empty_label = "Gender"


DATE = [
    ("Day", "Day"),
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
]

TIME = [
    ("Time", "Time"),
    ("10:00am - 11:00am", "10:00am - 11:00am"),
    ("11:30am - 12:30pm", "11:30am - 12:30pm"),
    ("1:00pm - 2:00pm", "1:00pm - 2:00pm"),
    ("2:30pm - 3:30pm", "2:30pm - 3:30pm"),
    ("4:00pm - 5:00pm", "4:00pm - 5:00pm"),
]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "fullname",
            "services",
            "phone",
            "area",
            "city",
            "state",
            "postal",
            "email",
            "date",
            "appt_time",
            "symptoms",
        ]
        widgets = {
            "fullname": forms.TextInput(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "Full name",
                    "required": True,
                }
            ),
            "services": forms.Select(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "Services",
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "(000) 000-000",
                    "required": True,
                }
            ),
            "area": forms.TextInput(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "Area",
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "City",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "State",
                }
            ),
            "postal": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "Postal",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "Enter your email",
                }
            ),
            "dob": forms.TextInput(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "date of birth",
                    "required": True,
                }
            ),
            "date": forms.Select(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "Day",
                    "required": True,
                },
                choices=DATE,
            ),
            "appt_time": forms.Select(
                attrs={
                    "class": "w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md",
                    "PlaceHolder": "Time",
                    "required": True,
                },
                choices=TIME,
            ),
            "symptoms": forms.Textarea(
                attrs={
                    "class": "block p-2.5 w-full text-sm text-gray-500 bg-transparent rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                    "placeholder": "Say your issue?...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["services"].empty_label = "Services"


class AssessmentRecordForm(forms.ModelForm):
    class Meta:
        model = AssessmentRecord
        fields = [
            "student",
            "course",
            "assessment_type",
            "subject",
            "score",
            "max_score",
            "exam_date",
            "note",
        ]
        widgets = {
            "exam_date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.TextInput(attrs={"placeholder": "Optional note"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = CustomUser.objects.filter(role=CustomUser.ROLE_STUDENT)


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "message", "category", "is_active"]


class StudentResourceForm(forms.ModelForm):
    class Meta:
        model = StudentResource
        fields = ["title", "resource_type", "course", "semester", "file", "external_url", "description"]


class FAQEntryForm(forms.ModelForm):
    class Meta:
        model = FAQEntry
        fields = ["question", "answer", "keywords", "department", "is_active"]
