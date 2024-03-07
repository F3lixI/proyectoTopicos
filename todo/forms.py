from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.core.validators import MinValueValidator, MaxValueValidator


class CustomCreationForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput, strip=False, required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']
        
class Cliente(forms.Form):
    telefono = forms.CharField(label='Teléfono', max_length=10, required=True)
    edad = forms.IntegerField(label='Edad', required=True, validators=[
            MinValueValidator(0, message="La edad debe ser mayor o igual a 0."),
            MaxValueValidator(100, message="La edad debe ser menor o igual a 100.")
        ])
    sexo = forms.ChoiceField(label='Sexo', choices=[('H', 'Hombre'), ('M', 'Mujer'), ('X', 'Otro')], required=True)
    
        
class PrecioForm(forms.Form):
    precio_min = forms.DecimalField(label='Precio mínimo', required=False)
    precio_max = forms.DecimalField(label='Precio máximo')
    

class DomicilioForm(forms.Form):
    calle = forms.CharField(label='Calle', max_length=100, required=True)
    numero = forms.IntegerField(label='Número', required=True)
    colonia = forms.CharField(label='Colonia', max_length=100, required=True)
    cp = forms.IntegerField(label='Código Postal', required=True)
    ciudad = forms.CharField(label='Ciudad', max_length=100, required=True, initial='Juárez')
    telefono = forms.CharField(label='Teléfono', max_length=12, required=True)
    indicaciones = forms.CharField(label='Indicaciones', max_length=100, required=False)
    nombreInstitucion = forms.CharField(label='Nombre de la institución', max_length=100, required=False)
    mensaje = forms.CharField(label='Añade un mensaje', max_length=100, required=False)
    payment_method = forms.ChoiceField(label='Método de pago', choices=[('tarjeta', 'Tarjeta'), ('paypal', 'PayPal')], required=True)


class PaymentForm(forms.Form):
    cardNumber = forms.CharField(label='Número de tarjeta', max_length=16, required=True)
    expirationDate = forms.CharField(max_length=5, label='Fecha de vencimiento (MM/YY)', help_text='Formato: MM/YY')
    cvv = forms.IntegerField(label='CVV', required=True)
    cardHolder = forms.CharField(label='Nombre del titular', max_length=100, required=True)
    

    