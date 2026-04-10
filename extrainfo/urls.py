from django.urls import path

from . import views

app_name = "information"

urlpatterns = [
    path("", views.patient_n_doctor, name="patndoc"),
    path("appoint/", views.appoint, name="appointment"),
    path("results/manage/", views.manage_results, name="manage_results"),
    path("results/student/", views.student_results, name="student_results"),
    path("results/parent/", views.parent_results, name="parent_results"),
    path("content/manage/", views.manage_content, name="manage_content"),
    path("content/announcement/<int:pk>/edit/", views.edit_announcement, name="edit_announcement"),
    path("content/announcement/<int:pk>/delete/", views.delete_announcement, name="delete_announcement"),
    path("content/resource/<int:pk>/edit/", views.edit_resource, name="edit_resource"),
    path("content/resource/<int:pk>/delete/", views.delete_resource, name="delete_resource"),
    path("content/faq/<int:pk>/edit/", views.edit_faq, name="edit_faq"),
    path("content/faq/<int:pk>/delete/", views.delete_faq, name="delete_faq"),
    path("api/announcements/", views.api_announcements, name="api_announcements"),
    path("api/resources/", views.api_resources, name="api_resources"),
    path("api/results/", views.api_results, name="api_results"),
]
