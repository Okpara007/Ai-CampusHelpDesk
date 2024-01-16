from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
import speech_recognition as sr
import pyttsx3
import json
import uuid
import openai
from openai import OpenAI
from datetime import timedelta, date, datetime



from .models import *

# Create your views here.

# npx tailwindcss -i ./assistant/static/src/input.css -o ./assistant/static/src/output.css --watch
# 01B9B4
client =OpenAI(
    api_key = "pk-yuLcYPQMmUsyHvhHvuHwgHiPLWYKoaiFnmfycNsbnFGRLvaE",
    base_url= 'https://api.pawan.krd/pai-001-light-beta/v1'
)

prompt = """
    You are an AI assistant that is an expert in medical health and is part of a hospital system called medicare AI
    You know about symptoms and signs of various types of illnesses.
    You can provide expert advice on self-diagnosis options in the case where an illness can be treated using a home remedy.
    If a query requires serious medical attention with a doctor, recommend them to book an appointment with our doctors
    If you are asked a question that is not related to medical health respond with "I'm sorry but your question is beyond my functionalities".
    Always give a response or answer the query that relate to the last response you gave. Before answering any other queries, check if it correspond to the last responses you gave. 
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


def history_view(request):
    convers = Chat.objects.filter(user= request.user)

    return render(request, 'main/index.html', {'convers':convers})

def chatdelete(request):
    # chat = Chat.objects.get
    url = request.META.get('HTTP_REFERER')
    chatId = request.GET.get('deleteitem')
    print(chatId)
    Chat.objects.filter(pk=chatId).delete()

    return redirect ('assistant:index')

