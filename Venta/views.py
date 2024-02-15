from django.shortcuts import render
from django.http import JsonResponse
import requests, json
from . models import Flores


def index(request):
    
    flores = Flores.objects.all()[:5]
    
    return render(request, 'index.html', {'flores': flores})