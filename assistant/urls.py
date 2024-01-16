from django.urls import path
from .views import *

app_name ="assistant"

urlpatterns = [
    path('', index, name='index'),
    path('initiate-chat/', initiate_chat),
    path('chat-previous/<str:chat_id>/', continue_chat, name='continuechat'),
    path('chat-previous/<str:chat_id>/initiate-chat/', continue_chat),
    path('history/', history_view, name='history'),
    path('delete-chat/', chatdelete, name='chatdelete'),
]