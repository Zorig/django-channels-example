from django.contrib import admin
from django.contrib.admin import ModelAdmin

from chat.models import Chat, Message


@admin.register(Chat)
class ChatAdmin(ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("author", "created_at")
