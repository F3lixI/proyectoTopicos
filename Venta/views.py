from django.shortcuts import render, redirect
from . models import Flores
from .forms import CustomCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate


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

def iniciarSesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')
        
        return render(request, 'login.html', {'form': form})
                
    else:
        # Si no es una solicitud POST, simplemente renderiza el formulario vacío
        return render(request, 'login.html', {'form': AuthenticationForm()})