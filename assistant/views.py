from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# import speech_recognition as sr
# import pyttsx3
import json
import uuid
import openai
from openai import OpenAI
from datetime import timedelta, date, datetime



from .models import *
from userschema.models import *

# Create your views here.

# npx tailwindcss -i ./assistant/static/src/input.css -o ./assistant/static/src/output.css --watch
# 01B9B4
client =OpenAI(
    api_key = ""
)

text = f"""
https://medicalasst.pythonanywhere.com/pre-home/appoint/
"""
remind = f"""
    Medication Reminders Functionality: The chatbot system shall be able to provide reminders \
    for medication use including additional information which may include dosages, side effects, \
    and interactions.
    can you remind of my medications?
"""

prompt = f"""
    You are an AI assistant that is an expert in medical health and is part of a hospital system called medicare AI
    You know about symptoms and signs of various types of illnesses.
    You can provide expert advice on self-diagnosis options in the case where an illness can be treated using a home remedy.

    If a query requires serious medical attention with a doctor, recommend them to book an appointment with our doctors.
    email support link is <a href="mailto: mdpeter28@gmail.com">medicare28@gmail.com</a> and phone number link is <a href="tel:08139315800">08139315800</a>
    Check the text delimeted provided to you with triple backticks \
    If it contain url links, you must provide them using anchor tag in HTML format with inline styling of color blue, giving it the name Book Appointment. \
    ```{text}```

    If a query contains booking an appointment with a doctor or how they can book an apointment with a doctor, display the HTML formatted link and educate them on the schedules of the doctor.
    Appointment with our doctor is available from 9am to 12pm and from 1pm to 4pm from Mondays to Fridays and 11am to 3pm on Saturdays.
    No appointment with doctors on Sundays

    If the user greets with "hello", respond with a friendly greeting acknowledging the user's initiation of conversation.

    If you are asked a question that is not related to medical health respond with "I'm sorry but your question is beyond my functionalities".

    If the user's query has anything to do with reminder functionality or the user's query refers to the text delimeted provided to you with triple star, \
    respond with "I'm sorry this functionality is still in process"
    ***{remind}***

    Always give a response or answer to the query that relate to the last response you gave. Before answering any other queries, check if it correspond to the last responses you gave.
    Do not use external URLs or blogs to refer
    Format any lists on individual lines with a dash and a space in front of each line.
"""


def ask_openai(message):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        # max_tokens = 100,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": message},
        ]
    )

    answer = response.choices[0].message.content.strip()
    return answer

@login_required(login_url='userschema:signin')
def initiate_chat(request):
    if request.method == 'POST':
        # chat_is_activated = Chat.objects.filter(user = request.user, conversation__isnull= False)
        message = request.POST.get('message')
        chatId = request.POST.get('chatId')
        # itemId = request.POST.get('itemId')
        print(chatId)
        # chatid = str(uuid.uuid4())
        if Chat.objects.filter(user= request.user, chat_id = chatId).exists():
            cont = Chat.objects.get(user = request.user, chat_id = chatId)
            cont.conversation.append(f"{message}")
            chats = ask_openai(message)
            cont.conversation.append(chats)
            cont = cont.save()
            return JsonResponse({'message':message, 'chats':chats})
        else:
            chats = ask_openai(message)
            chat_is_new = Chat.objects.create(
                user = request.user, title = message, chat_id=chatId,
                conversation=[f"{message}", f"{chats}"]
            )
            return JsonResponse({'message':message, 'chats':chats})

def index(request):
    if request.user.is_authenticated:

        return render(request, 'main/index.html')
    else:

        return redirect('userschema:signin')

@login_required(login_url='userschema:signin')
def continue_chat(request, chat_id):
    url = request.META.get('HTTP_REFERER')
    chat = get_object_or_404(Chat, pk = chat_id, user = request.user)
    datailchat = chat.conversation

    chat_history = datailchat if datailchat else []
    if request.method == 'POST':
        message = request.POST.get('message')
        bot = []
        chat_history.append(f"{message}")
        chats = ask_openai(message)
        chat_history.append(f"{chats}")
        datailchat = chat_history
        chat.save()
        return JsonResponse({"message":message, "chats":chats})

    return render(request, 'main/index.html', {'chat':datailchat})


@login_required(login_url='userschema:signin')
def history_view(request):
    convers = Chat.objects.filter(user= request.user)

    return render(request, 'main/index.html', {'convers':convers})

@login_required(login_url='userschema:signin')
def chatdelete(request):
    # chat = Chat.objects.get
    url = request.META.get('HTTP_REFERER')
    chatId = request.GET.get('deleteitem')
    print(chatId)
    Chat.objects.filter(pk=chatId).delete()

    return redirect ('assistant:index')

@login_required(login_url='userschema:signin')
def alldelete(request):
    url = request.META.get('HTTP_REFERER')
    chatId = request.POST['deleteitem']
    Chat.objects.filter(user_id=chatId).delete()

    return redirect (url)

@login_required(login_url='userschema:signin')
def userdelete(request):
    url = request.META.get('HTTP_REFERER')
    chatId = request.POST['deleteitem']
    CustomUser.objects.filter(id=chatId).delete()

    return redirect ('userschema:register')


