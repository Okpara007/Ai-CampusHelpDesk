from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display_links = ('title',)
    search_fields = ('user','title')
    list_display = ("user","title","chat_id","created_at")
