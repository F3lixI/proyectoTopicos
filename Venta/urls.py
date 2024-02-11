from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("flower_detail", views.flower_detail, name="flower_detail"),
]

