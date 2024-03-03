from django.contrib import admin
from .models import ToDo


@admin.register(ToDo)
class ToDoModelAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at", "modified_at")