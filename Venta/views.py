from django.shortcuts import render, redirect
from . models import Flores
from .forms import CustomCreationForm, PrecioForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q


def index(request):
    
    flores = Flores.objects.all()[:5]
    
    plantas = Flores.objects.all()[5:10]
    
    return render(request, 'index.html', {'flores': flores, 'plantas': plantas})

def signup(request):
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomCreationForm()
    
    return render(request, 'signup.html', {'form': form})

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
    
def listProducts(request):
    
    flores = Flores.objects.all()[:20]
    
    return render(request, 'listProducts.html', {'flores': flores})

def singleProduct(request, pk):
    
    flor = Flores.objects.get(pk=pk)
    
    flores = Flores.objects.all()[:4]
    
    return render(request, 'flower_detail.html', {'flor': flor, 'flores': flores})

def cerrarSesion(request):
    logout(request)
    return redirect('index')

def filtrar_productos(request):
    if request.method == 'POST':
        form = PrecioForm(request.POST)
        if form.is_valid():
            precio_min = form.cleaned_data['precio_min']
            precio_max = form.cleaned_data['precio_max']
            
            if precio_min == None:
                precio_min = 0
                
            flores = Flores.objects.filter(price__gte=precio_min, price__lte=precio_max)[:20]
            return render(request, 'listProducts.html', {'flores': flores, 'form': form})
    else:
        form = PrecioForm()
        
        flores = Flores.objects.all()[:20]
        
        return render(request, 'listProducts.html', {'form': form, 'flores': flores})
    
def search(request):
    query = request.GET.get('q')
    
    flores = Flores.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if flores.exists():
        return render(request, 'listProducts.html', {'flores': flores})
    else:
        return redirect('listProducts')
    
def listProductsCategory(request, category):
    
    flores = Flores.objects.filter(category=category)
    
    form = PrecioForm()
    
    return render(request, 'listProducts.html', {'flores': flores, 'form': form})
    