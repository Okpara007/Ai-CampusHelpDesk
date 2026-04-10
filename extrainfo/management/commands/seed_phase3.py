from datetime import date

from django.core.management.base import BaseCommand

from extrainfo.models import (
    Announcement,
    AssessmentRecord,
    Course,
    Department,
    FAQEntry,
    StudentResource,
)
from userschema.models import CustomUser


class Command(BaseCommand):
    help = "Seed phase 3 demo data (roles, courses, announcements, FAQs, resources, marks)."

    def handle(self, *args, **options):
        cs_dept, _ = Department.objects.get_or_create(name="Computer Science")
        bus_dept, _ = Department.objects.get_or_create(name="Business Administration")

        cs_course, _ = Course.objects.get_or_create(
            name="BSc Computer Science",
            defaults={
                "department": cs_dept,
                "duration": "4 years",
                "description": "Undergraduate program focused on software and systems.",
                "fees": "1200 USD/semester",
            },
        )
        bba_course, _ = Course.objects.get_or_create(
            name="BBA Management",
            defaults={
                "department": bus_dept,
                "duration": "4 years",
                "description": "Business and management foundation program.",
                "fees": "1100 USD/semester",
            },
        )

        admin_user, _ = CustomUser.objects.get_or_create(
            email="admin@campusdesk.local",
            defaults={
                "username": "admin@campusdesk.local",
                "role": CustomUser.ROLE_ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user.set_password("Password123!")
        admin_user.save()

        staff_user, _ = CustomUser.objects.get_or_create(
            email="staff@campusdesk.local",
            defaults={
                "username": "staff@campusdesk.local",
                "role": CustomUser.ROLE_STAFF,
                "is_staff": True,
            },
        )
        staff_user.set_password("Password123!")
        staff_user.save()

        student_user, _ = CustomUser.objects.get_or_create(
            email="student@campusdesk.local",
            defaults={
                "username": "student@campusdesk.local",
                "role": CustomUser.ROLE_STUDENT,
            },
        )
        student_user.set_password("Password123!")
        student_user.save()

        parent_user, _ = CustomUser.objects.get_or_create(
            email="parent@campusdesk.local",
            defaults={
                "username": "parent@campusdesk.local",
                "role": CustomUser.ROLE_PARENT,
                "linked_student": student_user,
            },
        )
        parent_user.linked_student = student_user
        parent_user.set_password("Password123!")
        parent_user.save()

        Announcement.objects.get_or_create(
            title="Admission Application Deadline",
            defaults={
                "message": "Applications for 2026 close on May 30.",
                "category": "Admissions",
                "is_active": True,
            },
        )
        Announcement.objects.get_or_create(
            title="Mid-Semester Exams",
            defaults={
                "message": "Mid-semester exam timetable has been published.",
                "category": "Exams",
                "is_active": True,
            },
        )

        FAQEntry.objects.get_or_create(
            question="How do I apply for admission?",
            defaults={
                "answer": "Complete the online form, upload required documents, and pay the application fee.",
                "keywords": "admission,apply,application",
                "department": cs_dept,
                "is_active": True,
            },
        )
        FAQEntry.objects.get_or_create(
            question="How do I check exam schedules?",
            defaults={
                "answer": "Open Student Resources and select Schedule for your course and semester.",
                "keywords": "exam,schedule,timetable",
                "department": cs_dept,
                "is_active": True,
            },
        )

        StudentResource.objects.get_or_create(
            title="CS Year 1 Timetable",
            resource_type="timetable",
            course=cs_course,
            semester="100",
            defaults={
                "external_url": "https://example.edu/timetable/cs-100",
                "description": "Weekly class timetable for CS 100 level.",
            },
        )
        StudentResource.objects.get_or_create(
            title="BBA Orientation Booklet",
            resource_type="booklet",
            course=bba_course,
            semester="100",
            defaults={
                "external_url": "https://example.edu/booklets/bba-orientation",
                "description": "Orientation details and academic calendar.",
            },
        )

        AssessmentRecord.objects.get_or_create(
            student=student_user,
            course=cs_course,
            assessment_type=AssessmentRecord.TYPE_WEEKLY,
            subject="Programming Fundamentals",
            score=18,
            max_score=25,
            exam_date=date(2026, 4, 1),
            defaults={"created_by": staff_user, "note": "Week 1 quiz"},
        )
        AssessmentRecord.objects.get_or_create(
            student=student_user,
            course=cs_course,
            assessment_type=AssessmentRecord.TYPE_PT1,
            subject="Programming Fundamentals",
            score=20,
            max_score=25,
            exam_date=date(2026, 4, 5),
            defaults={"created_by": staff_user, "note": "PT1"},
        )
        AssessmentRecord.objects.get_or_create(
            student=student_user,
            course=cs_course,
            assessment_type=AssessmentRecord.TYPE_PT2,
            subject="Programming Fundamentals",
            score=22,
            max_score=25,
            exam_date=date(2026, 4, 8),
            defaults={"created_by": staff_user, "note": "PT2"},
        )

        self.stdout.write(self.style.SUCCESS("Phase 3 demo data seeded."))
        self.stdout.write("Demo users:")
        self.stdout.write("- admin@campusdesk.local / Password123!")
        self.stdout.write("- staff@campusdesk.local / Password123!")
        self.stdout.write("- student@campusdesk.local / Password123!")
        self.stdout.write("- parent@campusdesk.local / Password123!")
