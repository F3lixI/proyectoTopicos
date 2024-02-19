from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests, json
from . models import Flores
from .forms import CustomCreationForm


def index(request):
    
    flores = Flores.objects.all()[:5]
    
    plantas = Flores.objects.all()[5:10]
    
    return render(request, 'index.html', {'flores': flores, 'plantas': plantas})

def signup(request):
    
    data = {
        'form': CustomCreationForm()
    }
    
    if request.method == 'POST':
        user_creation_form = CustomCreationForm(data=request.POST)
        
        if user_creation_form.is_valid():
            user_creation_form.save()
            return redirect('index')
        
    
    
    return render(request, 'signup.html', data)
