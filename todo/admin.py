from django.contrib import admin
from .models import ToDo, Flores


@admin.register(ToDo)
class ToDoModelAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at", "modified_at")
    
@admin.register(Flores)
class FloresModelAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")