from django.contrib import admin
from .models import *

# Register your models here.



@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "title",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "user__username",
        "title",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "session",
        "role",
        "created_at",
    )

    search_fields = (
        "content",
        "session__user__username",
    )

@admin.register(UploadedPDF)
class UploadedPDFAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "title",
        "uploaded_at",
    )

    search_fields = (
        "user__username",
        "title",
    )