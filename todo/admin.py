from django.contrib import admin
from .models import ToDo, Flores, Reviews
from import_export.admin import ImportExportModelAdmin


@admin.register(ToDo)
class ToDoModelAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at", "modified_at")
    
@admin.register(Flores)
class FloresModelAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category")
    
@admin.register(Reviews)
class ReviewsAdmin(ImportExportModelAdmin):
    list_display = ("id", "producto", "cliente", "calificacion", "comentario")





