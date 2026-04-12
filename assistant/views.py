import json
import os
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from extrainfo.models import Announcement, AssessmentRecord, Course, FAQEntry, StudentResource
from userschema.models import CustomUser

from .models import Chat


def _role_display(user):
    if not getattr(user, "role", None):
        return "student"
    return user.get_role_display().lower()


def _local_knowledge_answer(message):
    query = (message or "").strip().lower()
    if not query:
        return "Please type your question so I can help."

    faq_entries = FAQEntry.objects.filter(is_active=True)
    for item in faq_entries:
        keywords = [k.strip().lower() for k in (item.keywords or "").split(",") if k.strip()]
        text_blob = f"{item.question} {item.answer}".lower()
        if any(k in query for k in keywords) or query in text_blob:
            return item.answer

    if any(token in query for token in ["deadline", "date", "event", "notice", "announcement"]):
        latest = Announcement.objects.filter(is_active=True).order_by("-published_at")[:3]
        if latest:
            lines = [f"- {item.title}: {item.message}" for item in latest]
            return "Latest announcements:\n" + "\n".join(lines)

    if any(token in query for token in ["course", "program", "major", "department"]):
        courses = Course.objects.select_related("department").all()[:8]
        if courses:
            lines = [f"- {c.name} ({c.department.name})" for c in courses]
            return "Available programs include:\n" + "\n".join(lines)

    if any(token in query for token in ["timetable", "booklet", "resource", "schedule", "test solution"]):
        resources = StudentResource.objects.select_related("course").all()[:5]
        if resources:
            lines = []
            for r in resources:
                scope = f" - {r.course.name}" if r.course else ""
                link = r.external_url or (r.file.url if r.file else "")
                suffix = f" [{link}]" if link else ""
                lines.append(f"- {r.title} ({r.get_resource_type_display()}{scope}){suffix}")
            return "Here are student resources:\n" + "\n".join(lines)

    return None


def ask_helpdesk(question, user):
    local = _local_knowledge_answer(question)
    if local:
        return local

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return (
            "I could not find this in the local helpdesk data yet. "
            "Please ask admin to add this FAQ in Django admin under FAQ entries, "
            "or set OPENAI_API_KEY for AI responses."
        )

    system_prompt = (
        "You are a college student help desk assistant. "
        "Scope: admissions, courses, scholarships, fees, timetable, exam schedule, campus facilities, "
        "events, and student resources. "
        f"Current user role: {_role_display(user)}. "
        "Provide concise, practical answers. "
        "When unsure, say what information is missing and what the user should do next."
    )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )
        return (response.choices[0].message.content or "").strip()
    except Exception:
        return (
            "AI responses are temporarily unavailable in this environment. "
            "The local helpdesk data is still available, or you can switch to a supported Python version "
            "such as 3.12 or 3.13 and reinstall dependencies."
        )


def _shared_context(user):
    announcements = Announcement.objects.filter(is_active=True)[:5]
    resources = StudentResource.objects.select_related("course")[:5]
    context = {
        "announcements": announcements,
        "resources": resources,
    }

    if user.role == CustomUser.ROLE_STUDENT:
        records = AssessmentRecord.objects.filter(student=user)
        context["student_record_count"] = records.count()
        breakdown = records.values("assessment_type").annotate(total=Count("id")).order_by("assessment_type")
        context["dashboard_chart_labels"] = json.dumps([item["assessment_type"].upper() for item in breakdown])
        context["dashboard_chart_values"] = json.dumps([item["total"] for item in breakdown])
    elif user.role == CustomUser.ROLE_PARENT and user.linked_student_id:
        records = AssessmentRecord.objects.filter(student=user.linked_student)
        context["student_record_count"] = records.count()
        breakdown = records.values("assessment_type").annotate(total=Count("id")).order_by("assessment_type")
        context["dashboard_chart_labels"] = json.dumps([item["assessment_type"].upper() for item in breakdown])
        context["dashboard_chart_values"] = json.dumps([item["total"] for item in breakdown])
    elif user.role in {CustomUser.ROLE_STAFF, CustomUser.ROLE_ADMIN}:
        context["managed_record_count"] = AssessmentRecord.objects.count()
        context["student_count"] = CustomUser.objects.filter(role=CustomUser.ROLE_STUDENT).count()

    return context


@login_required(login_url="userschema:signin")
def dashboard(request):
    context = _shared_context(request.user)
    return render(request, "main/dashboard.html", context)


@login_required(login_url="userschema:signin")
def initiate_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    message = request.POST.get("message", "").strip()
    chat_id = request.POST.get("chatId", "").strip() or str(uuid.uuid4())

    if not message:
        return JsonResponse({"error": "Message cannot be empty"}, status=400)

    chat = Chat.objects.filter(user=request.user, chat_id=chat_id).first()
    answer = ask_helpdesk(message, request.user)

    if chat:
        history = chat.conversation or []
        history.extend([message, answer])
        chat.conversation = history
        chat.save(update_fields=["conversation"])
    else:
        Chat.objects.create(
            user=request.user,
            title=message[:100],
            chat_id=chat_id,
            conversation=[message, answer],
        )

    return JsonResponse({"message": message, "chats": answer})


def index(request):
    if not request.user.is_authenticated:
        return redirect("userschema:signin")

    context = _shared_context(request.user)
    return render(request, "main/index.html", context)


@login_required(login_url="userschema:signin")
def continue_chat(request, chat_id):
    chat = get_object_or_404(Chat, pk=chat_id, user=request.user)
    chat_history = list(chat.conversation or [])

    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if not message:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        answer = ask_helpdesk(message, request.user)
        chat_history.extend([message, answer])
        chat.conversation = chat_history
        chat.save(update_fields=["conversation"])
        return JsonResponse({"message": message, "chats": answer})

    context = _shared_context(request.user)
    context["chat"] = chat_history
    return render(request, "main/index.html", context)


@login_required(login_url="userschema:signin")
def history_view(request):
    convers = Chat.objects.filter(user=request.user)
    return render(request, "main/index.html", {"convers": convers, **_shared_context(request.user)})


@login_required(login_url="userschema:signin")
def chatdelete(request):
    chat_id = request.GET.get("deleteitem")
    Chat.objects.filter(pk=chat_id, user=request.user).delete()
    return redirect("assistant:index")


@login_required(login_url="userschema:signin")
def alldelete(request):
    chat_id = request.POST.get("deleteitem")
    if str(request.user.id) != str(chat_id) and request.user.role not in {CustomUser.ROLE_ADMIN, CustomUser.ROLE_STAFF}:
        return HttpResponseForbidden("You are not allowed to delete other users' chats.")

    if request.user.role in {CustomUser.ROLE_ADMIN, CustomUser.ROLE_STAFF}:
        Chat.objects.filter(user_id=chat_id).delete()
    else:
        Chat.objects.filter(user=request.user).delete()

    return redirect(request.META.get("HTTP_REFERER") or "assistant:index")


@login_required(login_url="userschema:signin")
def userdelete(request):
    target_id = request.POST.get("deleteitem")
    is_admin = request.user.role in {CustomUser.ROLE_ADMIN, CustomUser.ROLE_STAFF}

    if not is_admin and str(request.user.id) != str(target_id):
        return HttpResponseForbidden("You are not allowed to delete this account.")

    CustomUser.objects.filter(id=target_id).delete()
    return redirect("userschema:signin")
