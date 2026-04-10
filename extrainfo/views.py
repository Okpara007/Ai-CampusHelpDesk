import hmac
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from userschema.models import CustomUser

from .forms import (
    AnnouncementForm,
    AppointmentForm,
    AssessmentRecordForm,
    DoctorForm,
    FAQEntryForm,
    PatientForm,
    StudentResourceForm,
)
from .models import Announcement, AssessmentRecord, ContentAuditLog, FAQEntry, StudentResource


def _is_staff_or_admin(user):
    return user.is_authenticated and user.role in {CustomUser.ROLE_STAFF, CustomUser.ROLE_ADMIN}


def _is_student(user):
    return user.is_authenticated and user.role == CustomUser.ROLE_STUDENT


def _is_parent(user):
    return user.is_authenticated and user.role == CustomUser.ROLE_PARENT


def _has_valid_api_key(request):
    configured = (getattr(settings, "HELPDESK_API_KEY", "") or "").strip()
    provided = (request.headers.get("X-API-Key") or request.GET.get("api_key") or "").strip()
    return bool(configured and provided and hmac.compare_digest(configured, provided))


def _api_access_granted(request):
    return request.user.is_authenticated or _has_valid_api_key(request)


def _build_results_context(records):
    summary = (
        records.values("assessment_type")
        .annotate(avg_score=Avg("score"), avg_max=Avg("max_score"))
        .order_by("assessment_type")
    )

    weekly = records.filter(assessment_type=AssessmentRecord.TYPE_WEEKLY).order_by("exam_date", "created_at")
    pt = records.filter(assessment_type__in=[AssessmentRecord.TYPE_PT1, AssessmentRecord.TYPE_PT2]).order_by(
        "exam_date", "created_at"
    )

    bar_labels = [item.subject for item in weekly]
    bar_values = [float(item.score) for item in weekly]

    line_labels = [item.subject for item in pt]
    line_student = [float(item.score) for item in pt]

    if line_student:
        avg_score = sum(line_student) / len(line_student)
        max_score = max(line_student)
        line_avg = [avg_score for _ in line_student]
        line_high = [max_score for _ in line_student]
    else:
        line_avg = []
        line_high = []

    pie_labels = [item["assessment_type"].upper() for item in summary]
    pie_values = [float(item["avg_score"] or 0) for item in summary]

    return {
        "summary": summary,
        "bar_labels": json.dumps(bar_labels),
        "bar_values": json.dumps(bar_values),
        "line_labels": json.dumps(line_labels),
        "line_student": json.dumps(line_student),
        "line_avg": json.dumps(line_avg),
        "line_high": json.dumps(line_high),
        "pie_labels": json.dumps(pie_labels),
        "pie_values": json.dumps(pie_values),
    }


def _paginate_queryset(queryset, page_number, per_page=8):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def _log_content_action(*, actor, action, content_type, object_id, summary):
    if not actor.is_authenticated:
        return
    ContentAuditLog.objects.create(
        actor=actor,
        action=action,
        content_type=content_type,
        object_id=object_id,
        summary=summary[:255],
    )


@login_required(login_url="userschema:signin")
def patient_n_doctor(request):
    form = PatientForm()
    forms = DoctorForm()
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        if request.POST.get("submit") == "patient":
            form = PatientForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect("assistant:index")
            messages.error(request, form.errors)
            return redirect(url)

        if request.POST.get("submit") == "doctor":
            forms = DoctorForm(request.POST)
            if forms.is_valid():
                instance = forms.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect("assistant:index")
            messages.error(request, forms.errors)
            return redirect(url)

    return render(request, "info/info.html", {"form": form, "forms": forms})


@login_required(login_url="userschema:signin")
def appoint(request):
    form = AppointmentForm()
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        dob = request.POST.get("dob")
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.dob = dob
            instance.save()
            messages.success(request, "Your Appointment has been submitted!")
            return redirect(url)
        messages.error(request, form.errors)
        return redirect(url)

    return render(request, "info/appointment.html", {"form": form})


@login_required(login_url="userschema:signin")
@user_passes_test(_is_staff_or_admin)
def manage_results(request):
    form = AssessmentRecordForm()

    if request.method == "POST":
        form = AssessmentRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            record.save()
            messages.success(request, "Assessment record added successfully.")
            return redirect("information:manage_results")
        messages.error(request, form.errors)

    records = AssessmentRecord.objects.select_related("student", "course")[:50]
    return render(request, "info/results_manage.html", {"form": form, "records": records})


@login_required(login_url="userschema:signin")
@user_passes_test(_is_staff_or_admin)
def manage_content(request):
    announcement_form = AnnouncementForm(prefix="ann")
    resource_form = StudentResourceForm(prefix="res")
    faq_form = FAQEntryForm(prefix="faq")

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "announcement":
            announcement_form = AnnouncementForm(request.POST, prefix="ann")
            if announcement_form.is_valid():
                announcement = announcement_form.save()
                _log_content_action(
                    actor=request.user,
                    action=ContentAuditLog.ACTION_CREATE,
                    content_type=ContentAuditLog.TYPE_ANNOUNCEMENT,
                    object_id=announcement.id,
                    summary=announcement.title,
                )
                messages.success(request, "Announcement created.")
                return redirect("information:manage_content")
            messages.error(request, announcement_form.errors)
        elif form_type == "resource":
            resource_form = StudentResourceForm(request.POST, request.FILES, prefix="res")
            if resource_form.is_valid():
                resource = resource_form.save()
                _log_content_action(
                    actor=request.user,
                    action=ContentAuditLog.ACTION_CREATE,
                    content_type=ContentAuditLog.TYPE_RESOURCE,
                    object_id=resource.id,
                    summary=resource.title,
                )
                messages.success(request, "Resource created.")
                return redirect("information:manage_content")
            messages.error(request, resource_form.errors)
        elif form_type == "faq":
            faq_form = FAQEntryForm(request.POST, prefix="faq")
            if faq_form.is_valid():
                faq = faq_form.save()
                _log_content_action(
                    actor=request.user,
                    action=ContentAuditLog.ACTION_CREATE,
                    content_type=ContentAuditLog.TYPE_FAQ,
                    object_id=faq.id,
                    summary=faq.question,
                )
                messages.success(request, "FAQ entry created.")
                return redirect("information:manage_content")
            messages.error(request, faq_form.errors)

    query = (request.GET.get("q") or "").strip()
    announcement_sort = request.GET.get("ann_sort") or "newest"
    resource_sort = request.GET.get("res_sort") or "newest"
    faq_sort = request.GET.get("faq_sort") or "question"

    announcements = Announcement.objects.all()
    resources = StudentResource.objects.select_related("course").all()
    faqs = FAQEntry.objects.select_related("department").all()

    if query:
        announcements = announcements.filter(Q(title__icontains=query) | Q(message__icontains=query) | Q(category__icontains=query))
        resources = resources.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(semester__icontains=query)
            | Q(course__name__icontains=query)
        )
        faqs = faqs.filter(
            Q(question__icontains=query)
            | Q(answer__icontains=query)
            | Q(keywords__icontains=query)
            | Q(department__name__icontains=query)
        )

    announcement_sort_map = {
        "newest": "-published_at",
        "oldest": "published_at",
        "title": "title",
    }
    resource_sort_map = {
        "newest": "-created_at",
        "oldest": "created_at",
        "title": "title",
        "type": "resource_type",
    }
    faq_sort_map = {
        "question": "question",
        "updated": "-updated_at",
        "oldest": "updated_at",
    }

    announcements = announcements.order_by(announcement_sort_map.get(announcement_sort, "-published_at"))
    resources = resources.order_by(resource_sort_map.get(resource_sort, "-created_at"))
    faqs = faqs.order_by(faq_sort_map.get(faq_sort, "question"))

    announcements_page = _paginate_queryset(announcements, request.GET.get("ann_page"))
    resources_page = _paginate_queryset(resources, request.GET.get("res_page"))
    faqs_page = _paginate_queryset(faqs, request.GET.get("faq_page"))
    recent_logs = ContentAuditLog.objects.select_related("actor")[:12]

    context = {
        "announcement_form": announcement_form,
        "resource_form": resource_form,
        "faq_form": faq_form,
        "query": query,
        "announcement_sort": announcement_sort,
        "resource_sort": resource_sort,
        "faq_sort": faq_sort,
        "announcements": announcements_page,
        "resources": resources_page,
        "faqs": faqs_page,
        "recent_logs": recent_logs,
    }
    return render(request, "info/content_manage.html", context)


@login_required(login_url="userschema:signin")
@user_passes_test(_is_staff_or_admin)
def edit_announcement(request, pk):
    item = get_object_or_404(Announcement, pk=pk)
    form = AnnouncementForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        announcement = form.save()
        _log_content_action(
            actor=request.user,
            action=ContentAuditLog.ACTION_UPDATE,
            content_type=ContentAuditLog.TYPE_ANNOUNCEMENT,
            object_id=announcement.id,
            summary=announcement.title,
        )
        messages.success(request, "Announcement updated.")
        return redirect("information:manage_content")
    return render(request, "info/content_edit.html", {"form": form, "title": "Edit Announcement"})


@login_required(login_url="userschema:signin")
@user_passes_test(_is_staff_or_admin)
def delete_announcement(request, pk):
    item = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        item_id = item.id
        summary = item.title
        item.delete()
        _log_content_action(
            actor=request.user,
            action=ContentAuditLog.ACTION_DELETE,
            content_type=ContentAuditLog.TYPE_ANNOUNCEMENT,
            object_id=item_id,
            summary=summary,
        )
        messages.success(request, "Announcement deleted.")
    return redirect("information:manage_content")


@login_required(login_url="userschema:signin")
@user_passes_test(_is_staff_or_admin)
def edit_resource(request, pk):
    item = get_object_or_404(StudentResource, pk=pk)
    form = StudentResourceForm(request.POST or None, request.FILES or None, instance=item)
    if request.method == "POST" and form.is_valid():
        resource = form.save()
        _log_content_action(
            actor=request.user,
            action=ContentAuditLog.ACTION_UPDATE,
            content_type=ContentAuditLog.TYPE_RESOURCE,
            object_id=resource.id,
            summary=resource.title,
        )
        messages.success(request, "Resource updated.")
        return redirect("information:manage_content")
    return render(request, "info/content_edit.html", {"form": form, "title": "Edit Resource"})


@login_required(login_url="userschema:signin")
@user_passes_test(_is_staff_or_admin)
def delete_resource(request, pk):
    item = get_object_or_404(StudentResource, pk=pk)
    if request.method == "POST":
        item_id = item.id
        summary = item.title
        item.delete()
        _log_content_action(
            actor=request.user,
            action=ContentAuditLog.ACTION_DELETE,
            content_type=ContentAuditLog.TYPE_RESOURCE,
            object_id=item_id,
            summary=summary,
        )
        messages.success(request, "Resource deleted.")
    return redirect("information:manage_content")


@login_required(login_url="userschema:signin")
@user_passes_test(_is_staff_or_admin)
def edit_faq(request, pk):
    item = get_object_or_404(FAQEntry, pk=pk)
    form = FAQEntryForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        faq = form.save()
        _log_content_action(
            actor=request.user,
            action=ContentAuditLog.ACTION_UPDATE,
            content_type=ContentAuditLog.TYPE_FAQ,
            object_id=faq.id,
            summary=faq.question,
        )
        messages.success(request, "FAQ updated.")
        return redirect("information:manage_content")
    return render(request, "info/content_edit.html", {"form": form, "title": "Edit FAQ"})


@login_required(login_url="userschema:signin")
@user_passes_test(_is_staff_or_admin)
def delete_faq(request, pk):
    item = get_object_or_404(FAQEntry, pk=pk)
    if request.method == "POST":
        item_id = item.id
        summary = item.question
        item.delete()
        _log_content_action(
            actor=request.user,
            action=ContentAuditLog.ACTION_DELETE,
            content_type=ContentAuditLog.TYPE_FAQ,
            object_id=item_id,
            summary=summary,
        )
        messages.success(request, "FAQ deleted.")
    return redirect("information:manage_content")


@login_required(login_url="userschema:signin")
@user_passes_test(_is_student)
def student_results(request):
    records = AssessmentRecord.objects.filter(student=request.user).select_related("course")
    context = _build_results_context(records)
    context.update({"records": records, "for_parent": False})
    return render(request, "info/results_student.html", context)


@login_required(login_url="userschema:signin")
@user_passes_test(_is_parent)
def parent_results(request):
    student = request.user.linked_student
    if not student:
        messages.error(request, "No student account linked to this parent profile yet.")
        return redirect("assistant:dashboard")

    records = AssessmentRecord.objects.filter(student=student).select_related("course")
    context = _build_results_context(records)
    context.update({"records": records, "for_parent": True, "student": student})
    return render(request, "info/results_student.html", context)


def api_announcements(request):
    if not _api_access_granted(request):
        return JsonResponse({"error": "Unauthorized. Provide session auth or X-API-Key."}, status=401)

    data = list(
        Announcement.objects.filter(is_active=True)
        .order_by("-published_at")
        .values("id", "title", "message", "category", "published_at")[:20]
    )
    return JsonResponse({"results": data})


def api_resources(request):
    if not _api_access_granted(request):
        return JsonResponse({"error": "Unauthorized. Provide session auth or X-API-Key."}, status=401)

    qs = StudentResource.objects.select_related("course").all().order_by("-created_at")

    resource_type = request.GET.get("type")
    course_id = request.GET.get("course")
    semester = request.GET.get("semester")

    if resource_type:
        qs = qs.filter(resource_type=resource_type)
    if course_id:
        qs = qs.filter(course_id=course_id)
    if semester:
        qs = qs.filter(semester=semester)

    results = [
        {
            "id": item.id,
            "title": item.title,
            "type": item.resource_type,
            "course": item.course.name if item.course else None,
            "semester": item.semester,
            "external_url": item.external_url,
            "file": item.file.url if item.file else None,
            "description": item.description,
            "created_at": item.created_at,
        }
        for item in qs[:50]
    ]
    return JsonResponse({"results": results})


def api_results(request):
    user = request.user if request.user.is_authenticated else None

    if user:
        if user.role == CustomUser.ROLE_STUDENT:
            target_student = user
        elif user.role == CustomUser.ROLE_PARENT:
            if not user.linked_student:
                return JsonResponse({"error": "No linked student profile for parent."}, status=400)
            target_student = user.linked_student
        elif user.role in {CustomUser.ROLE_STAFF, CustomUser.ROLE_ADMIN}:
            student_id = request.GET.get("student_id")
            if not student_id:
                return JsonResponse({"error": "student_id query param is required for staff/admin."}, status=400)
            target_student = CustomUser.objects.filter(id=student_id, role=CustomUser.ROLE_STUDENT).first()
            if not target_student:
                return JsonResponse({"error": "Student not found."}, status=404)
        else:
            return JsonResponse({"error": "Role not permitted."}, status=403)
    else:
        if not _has_valid_api_key(request):
            return JsonResponse({"error": "Unauthorized. Provide session auth or X-API-Key."}, status=401)

        student_id = request.GET.get("student_id")
        if not student_id:
            return JsonResponse({"error": "student_id query param is required with API key."}, status=400)
        target_student = CustomUser.objects.filter(id=student_id, role=CustomUser.ROLE_STUDENT).first()
        if not target_student:
            return JsonResponse({"error": "Student not found."}, status=404)

    qs = AssessmentRecord.objects.filter(student=target_student).select_related("course").order_by("-created_at")
    summary = (
        qs.values("assessment_type")
        .annotate(avg_score=Avg("score"), avg_max=Avg("max_score"))
        .order_by("assessment_type")
    )

    records = [
        {
            "id": item.id,
            "assessment_type": item.assessment_type,
            "subject": item.subject,
            "score": float(item.score),
            "max_score": float(item.max_score),
            "course": item.course.name if item.course else None,
            "exam_date": item.exam_date,
            "note": item.note,
        }
        for item in qs[:100]
    ]

    return JsonResponse(
        {
            "student": {"id": target_student.id, "email": target_student.email},
            "summary": list(summary),
            "records": records,
        }
    )
