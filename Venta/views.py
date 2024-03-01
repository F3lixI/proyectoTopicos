from django.shortcuts import render, redirect
from . models import Flores
from .forms import CustomCreationForm, PrecioForm, DomicilioForm, PaymentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q

#Paypal
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse


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
    
    if request.method == 'POST':
        form = PrecioForm(request.POST)
        if form.is_valid():
            precio_min = form.cleaned_data['precio_min']
            precio_max = form.cleaned_data['precio_max']
            
            orden = request.GET.get('orden')
        
            if orden == '1':  
                flores = Flores.objects.filter(category=category).order_by('price')[:20]
            elif orden == '2':  
                flores = Flores.objects.filter(category=category).order_by('-price')[:20]
            elif orden == '3': 
                flores = Flores.objects.filter(category=category).order_by('name')[:20]
            else:
                flores = Flores.objects.filter(category=category)[:20]
            
            if precio_min == None:
                precio_min = 0
                
            flores = Flores.objects.filter(category=category, price__gte=precio_min, price__lte=precio_max)[:20]
            
            
            return render(request, 'listProducts.html', {'flores': flores, 'form': form, 'orden': orden})
    else:
        form = PrecioForm()
        
        orden = request.GET.get('orden')
        
        if orden == '1':  
            flores = Flores.objects.filter(category=category).order_by('price')[:20]
        elif orden == '2':  
            flores = Flores.objects.filter(category=category).order_by('-price')[:20]
        elif orden == '3': 
            flores = Flores.objects.filter(category=category).order_by('name')[:20]
        else:
            flores = Flores.objects.filter(category=category)[:20]
        
        
        return render(request, 'listProducts.html', {'form': form, 'flores': flores, 'orden': orden})
    

def seeShoppingCart(request):
    carrito = request.session.get('carrito', {})
    
    flores = Flores.objects.filter(id__in=carrito.keys())
    
    total = sum(flor.price * carrito[str(flor.id)] for flor in flores)
    
    #cantidad = {flor.id: carrito[str(flor.id)] for flor in flores}
    cantidad = [(flor.id, carrito.get(str(flor.id), 0)) for flor in flores]
    
    return render(request, 'cart.html', {'flores': flores, 'total': total, 'cantidad': cantidad})

def addShoppingCart(request, pk):
    
    carrito = request.session.get('carrito', {})
    
    carrito[pk] = carrito.get(pk, 0) + 1
    request.session['carrito'] = carrito
    
    return redirect('shoppingCart')

def removeShoppingCart(request, pk):
    carrito = request.session.get('carrito', {})
    
    del carrito[str(pk)]

    request.session['carrito'] = carrito
    
    return redirect('shoppingCart')

def updateShoppingCart(request, pk):
    carrito = request.session.get('carrito', {})
    
    carrito[str(pk)] += 1
    
    request.session['carrito'] = carrito

    return redirect('shoppingCart')

def disminuirCantidad(request, pk):
    carrito = request.session.get('carrito', {})
    
    if carrito[str(pk)] > 1:
        carrito[str(pk)] -= 1
    else:
        del carrito[str(pk)]
    
    request.session['carrito'] = carrito
    
    return redirect('shoppingCart')


def checkout(request):
    if request.method == 'POST':
        if 'direccion-submit' in request.POST:
            form = DomicilioForm(request.POST)
            
            #obtiene el metodo de pago del formulario
            metodo_pago = request.POST.get('payment_method')
            
                
            if form.is_valid():
                
                
                if metodo_pago == 'tarjeta':
                    formPayment = PaymentForm()
                    return render(request, 'checkout.html', {'formPayment': formPayment})
                else:
                    host = request.get_host()
            
                    #obtiene el carrito de la sesion
                    carrito = request.session.get('carrito', {})
                    
                    #consulta las flores que estan en el carrito
                    flores = Flores.objects.filter(id__in=carrito.keys())

                    #calcula el total de la compra
                    total = sum(flor.price * carrito[str(flor.id)] for flor in flores)
                    
                    paypal_checkout = {
                        'business': settings.PAYPAL_RECEIVER_EMAIL,
                        'amount': total,
                        'item_name': 'Flores',
                        'invoice': str(uuid.uuid4()),
                        'currency_code': 'USD',
                        #'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
                        #'return_url': 'http://{}{}'.format(host, reverse('profile')),
                        #'cancel_return': 'http://{}{}'.format(host, reverse('checkout')),
                    }
                        
                    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
                
                    formPayment = PaymentForm()
                    
                    context = {
                        'paypal': paypal_payment,
                    }
                    
                    return render(request, 'checkout.html', context)
            else:
                # Si el formulario de dirección no es válido, vuelve a mostrarlo con los errores
                return render(request, 'checkout.html', {'form': form})
        elif 'payment-submit' in request.POST:
            
            formPayment = PaymentForm(request.POST)
            
            if formPayment.is_valid():
                print(formPayment.cleaned_data)
                # Procesar el formulario de pago si es válido
                # Aquí puedes realizar las acciones necesarias, como guardar la información y completar la compra
                # Después de procesar el pago, podrías redirigir al usuario a una página de confirmación o a donde desees
                return redirect('index')
            else:
                # Si el formulario de pago no es válido, vuelve a mostrarlo con los errores
                return render(request, 'checkout.html', {'formPayment': formPayment})
    else:
        # Cargar el formulario de dirección por defecto
        form = DomicilioForm()
        return render(request, 'checkout.html', {'form': form})
    
def profile(request):
    return render(request, 'profile.html')

    


    

    

    