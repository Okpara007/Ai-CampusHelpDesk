from django.contrib import admin

from .models import (
    Announcement,
    Appointment,
    AssessmentRecord,
    ContentAuditLog,
    Course,
    Department,
    Doctor,
    FAQEntry,
    Gender,
    Patient,
    StudentResource,
)


admin.site.register([Gender, Patient, Doctor, Department, Appointment, Course, StudentResource, AssessmentRecord])


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_active", "published_at")
    list_filter = ("category", "is_active")
    search_fields = ("title", "message")


@admin.register(FAQEntry)
class FAQEntryAdmin(admin.ModelAdmin):
    list_display = ("question", "department", "is_active", "updated_at")
    list_filter = ("is_active", "department")
    search_fields = ("question", "answer", "keywords")


@admin.register(ContentAuditLog)
class ContentAuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "actor", "action", "content_type", "object_id", "summary")
    list_filter = ("action", "content_type", "created_at")
    search_fields = ("summary", "actor__email")
