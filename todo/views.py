from django.shortcuts import render, redirect
from . models import Flores, Clientes, Categoria, DetalleOrden, Orden, Direccion, Reviews
from .forms import CustomCreationForm, PrecioForm, DomicilioForm, PaymentForm, ClienteForm, DomicilioCliente, ReviewForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils import timezone

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
        if 'user_form_submit' in request.POST:
            
            user_form = CustomCreationForm(request.POST)
            
            if user_form.is_valid():
                
                request.session['user_form_data'] = user_form.cleaned_data
                
                user_form.save()
                
                cliente_form = ClienteForm()
                
                return render(request, 'signup.html', {'cliente_form': cliente_form})
            else:
                return render(request, 'signup.html', {'user_form': user_form})
        elif 'cliente_form_submit' in request.POST:
            cliente_form = ClienteForm(request.POST)
            
            if cliente_form.is_valid():
                
                user_form_data = request.session.pop('user_form_data', None)

                username=user_form_data['username'],
                email=user_form_data['email'],
                password=user_form_data['password1'], 
                first_name=user_form_data['first_name'],
                last_name=user_form_data['last_name']
                telefono = cliente_form.cleaned_data['telefono']
                edad = cliente_form.cleaned_data['edad']
                sexo = cliente_form.cleaned_data['sexo']
                # Crear el cliente con el usuario asociado
                cliente = Clientes(
                    username = username,
                    email=email,
                    password=password,
                    nombre=first_name,
                    apellido=last_name,
                    fecha_creacion=timezone.now(),
                    telefono=telefono,
                    edad=edad,
                    sexo=sexo
                )
                cliente.save()
                return redirect('login')  
            else:
                return render(request, 'signup.html', {'cliente_form': cliente_form})
    else:
        user_form = CustomCreationForm()
    
        return render(request, 'signup.html', {'user_form': user_form})
   

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
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            
            review = Reviews()
            
            review.cliente = User.objects.get(pk=request.user.id)
            review.producto = Flores.objects.get(pk=pk)
            review.calificacion = form.cleaned_data['calificacion']
            review.comentario = form.cleaned_data['comentario']
            review.fecha_creacion = timezone.now()
            
            review.save()
           
            return redirect('singleProduct', pk=pk)
        else:
            return render(request, 'flower_detail.html', {'form': form})
    else:
        form = ReviewForm()
        
        flor = Flores.objects.get(pk=pk)
        
        flores = Flores.objects.all()[:4]    
        
        reviews = Reviews.objects.filter(producto_id=pk).order_by('-fecha_creacion')
        
        users = [review.cliente for review in reviews]
        
    return render(request, 'flower_detail.html', {'flor': flor, 'flores': flores, 'form': form, 'reviews': reviews, 'users': users})

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
    quantity = [(flor.id, carrito.get(str(flor.id), 0)) for flor in flores]
    
    detalles_carrito = {}

    for producto_id, cantidad in carrito.items():
        producto = Flores.objects.get(pk=producto_id)
        subtotal = producto.price * cantidad
        detalles_carrito[producto_id] = {
            'nombre': producto.name,
            'cantidad': cantidad,
            'precio_unitario': producto.price,
            'subtotal': subtotal,
        }

    total_carrito = sum(item['subtotal'] for item in detalles_carrito.values())
    
    return render(request, 'cart.html', {'flores': flores, 'total': total, 'quantity': quantity, 'total_carrito': total_carrito})

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
@login_required
def checkout(request):
    if request.method == 'POST':
        if 'direccion-submit' in request.POST:
            form = DomicilioForm(request.POST)
            
            #obtiene el metodo de pago del formulario
            metodo_pago = request.POST.get('payment_method')
            
                
            if form.is_valid():
                
                #obtiene el carrito de la sesion
                carrito = request.session.get('carrito', {})
                
                #calcula el total 
                flores = Flores.objects.filter(id__in=carrito.keys())
                total = sum(flor.price * carrito[str(flor.id)] for flor in flores)
                                
                orden = Orden()
                
                orden.cliente = request.user
                orden.fecha = timezone.now()
                orden.total = total
                orden.estado = 'aceptado'
                    
                orden.save()
                
                detalle_orden = DetalleOrden()
                #detalle_orden.productos = flores
                detalle_orden.id_orden = Orden.objects.latest('id')
                detalle_orden.calle = form.cleaned_data['calle']
                detalle_orden.numero = form.cleaned_data['numero']
                detalle_orden.colonia = form.cleaned_data['colonia']
                detalle_orden.ciudad = form.cleaned_data['ciudad']
                detalle_orden.codigo_postal = form.cleaned_data['cp']
                detalle_orden.metodoPago = metodo_pago
                detalle_orden.indicaciones = form.cleaned_data['indicaciones']
                detalle_orden.mensaje = form.cleaned_data['mensaje']
                detalle_orden.nombreInstitucion = form.cleaned_data['nombreInstitucion']
                detalle_orden.save()
                
                detalle_orden.productos.add(*flores)
                
                if metodo_pago == 'tarjeta':
                    
                    carrito = request.session.get('carrito', {})
                    
                    flores = Flores.objects.filter(id__in=carrito.keys())
                    
                    total = sum(flor.price * carrito[str(flor.id)] for flor in flores)
                    
                    cantidad = [(flor.id, carrito.get(str(flor.id), 0)) for flor in flores]
                    
                    formPayment = PaymentForm()                        
                    return render(request, 'checkout.html', {'formPayment': formPayment, 'flores': flores, 'total': total, 'cantidad': cantidad})
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
                
                #elimina el carrito 
                del request.session['carrito']
                
                return redirect('profile')
                
            else:
                # Si el formulario de pago no es válido, vuelve a mostrarlo con los errores
                return render(request, 'checkout.html', {'formPayment': formPayment})
    else:
        # Cargar el formulario de dirección por defecto
        form = DomicilioForm()
        
        #obtiene los datos del carrito y los manda
        carrito = request.session.get('carrito', {})
        
        flores = Flores.objects.filter(id__in=carrito.keys())
        
        total = sum(flor.price * carrito[str(flor.id)] for flor in flores)
        
        cantidad = [(flor.id, carrito.get(str(flor.id), 0)) for flor in flores]
        
        return render(request, 'checkout.html', {'form': form, 'flores': flores, 'total': total, 'cantidad': cantidad})
        



@login_required
def profile(request):
    
    if request.method == 'POST':
        
        form = DomicilioCliente(request.POST)
        
        if form.is_valid():
            
            user_id = request.user.id
            
            cliente = Clientes.objects.get(id=user_id)
            
            try:
                direccion = Direccion.objects.get(cliente=user_id)
            except Direccion.DoesNotExist:
                direccion = Direccion(cliente_id=user_id)
            
            direccion.calle = form.cleaned_data['calle']
            direccion.numero = form.cleaned_data['numero']
            direccion.colonia = form.cleaned_data['colonia']
            direccion.ciudad = 'Juarez'
            direccion.codigo_postal = form.cleaned_data['cp']
            direccion.save()
            
            return redirect('profile')
        else:
            return render(request, 'profile.html', {'form': form})
    else:
        
        user_id = request.user.id
        cliente = Clientes.objects.get(id=user_id)
        user = request.user
        
        #consulta la direccion del cliente si existe
        if Direccion.objects.filter(cliente_id=user_id).exists():
            direccion = Direccion.objects.get(cliente_id=user_id)
        else:
            direccion = None
        
        #si no existe la direccion solo renderiza el formulario vacio
        if direccion is None:
            domiciliocliente = DomicilioCliente()
        else:
            domiciliocliente = DomicilioCliente(initial={
                'calle': direccion.calle,
                'numero': direccion.numero,
                'colonia': direccion.colonia,
                'cp': direccion.codigo_postal,
            })
        
        #consulta las ordenes del cliente
        ordenes = Orden.objects.filter(cliente_id=user_id)
        
        #guarda los id de las ordenes para consultar los detalles de cada orden
        ids = [orden.id for orden in ordenes]
        
        #consulta los detalles de las ordenes
        detalles = DetalleOrden.objects.filter(id_orden_id__in=ids)
        
        #flores = []
        
        flores = []

        for detalle in detalles:
            for flor in detalle.productos.all():
                flores.append(flor.name)

        cantidadFlores = {}

        for flor in flores:
            cantidadFlores[flor] = cantidadFlores.get(flor, 0) + 1
            
        #print('helllllo',cantidadFlores)

        cantidadFlores = [(flor, cantidad) for flor, cantidad in cantidadFlores.items()]

        context = {
            'user': user,
            'cliente': cliente,
            'domiciliocliente': domiciliocliente,
            'ordenes': ordenes,
            'detalles': detalles,
            #'flores' : flores,
            'cantidadFlores': cantidadFlores,
            
        }
        
        return render(request, 'profile.html', context)


