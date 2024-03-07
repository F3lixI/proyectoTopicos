from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import re

from crispy_forms.helper import FormHelper

from django.utils import timezone




class CustomCreationForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True, max_length=40, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), required=True, max_length=20)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), strip=False, required=True, max_length=20)
        
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']
        
    
        
def validate_phone_number(value):
    if not re.match(r'^\d{10}$', value):
        raise ValidationError('El número de teléfono debe tener exactamente 10 dígitos.')
    
class ClienteForm(forms.Form):
    telefono = forms.CharField(label='Teléfono', max_length=10, validators=[validate_phone_number],required=True)
    edad = forms.IntegerField(label='Edad', required=True, validators=[
            MinValueValidator(0, message="La edad debe ser mayor o igual a 0."),
            MaxValueValidator(100, message="La edad debe ser menor o igual a 100.")
        ])
    sexo = forms.ChoiceField(label='Sexo', choices=[('H', 'Hombre'), ('M', 'Mujer'), ('X', 'Otro')], required=True)
    
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


    
        
class PrecioForm(forms.Form):
    precio_min = forms.DecimalField(label='Precio mínimo', required=False)
    precio_max = forms.DecimalField(label='Precio máximo')
    

class DomicilioForm(forms.Form):
    calle = forms.CharField(label='Calle', max_length=30, required=True)
    numero = forms.IntegerField(label='Número', required=True)
    colonia = forms.CharField(label='Colonia', max_length=30, required=True)
    cp = forms.CharField(label='Código Postal', max_length=5, min_length=5, required=True)
    ciudad = forms.CharField(label='Ciudad', max_length=30, required=True, initial='Juárez')
    telefono = forms.CharField(label='Teléfono', max_length=10, required=True, validators=[validate_phone_number])
    indicaciones = forms.CharField(label='Indicaciones', max_length=80, required=False)
    nombreInstitucion = forms.CharField(label='Nombre de la institución', max_length=30, required=False)
    mensaje = forms.CharField(label='Añade un mensaje', max_length=100, required=False)
    payment_method = forms.ChoiceField(label='Método de pago', choices=[('tarjeta', 'Tarjeta'), ('paypal', 'PayPal')], required=True)
    fecha_entrega = forms.DateField(label='Programar envio', help_text='Dejar en blanco para envio inmediato',widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    
    def clean_fecha_entrega(self):
        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        if fecha_entrega:
            if fecha_entrega <= timezone.now().date():
                raise forms.ValidationError("La fecha de entrega debe ser mayor a la fecha actual.")
        else:
            # Si no se proporciona fecha de entrega, se considera envío inmediato
            fecha_entrega = timezone.now().date()
        return fecha_entrega
    
    def clean_cp(self):
        cp = self.cleaned_data.get('cp')
        if not cp.isdigit() or len(cp) != 5:
            raise forms.ValidationError("El código postal debe contener exactamente 5 dígitos.")
        return cp
    
    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero and len(str(numero)) > 6:
            raise forms.ValidationError("El número no puede tener más de 6 dígitos.")
        return numero


class PaymentForm(forms.Form):
    cardNumber = forms.CharField(label='Número de tarjeta', max_length=16, required=True)
    expirationDate = forms.CharField(max_length=5, label='Fecha de vencimiento (MM/YY)', help_text='Formato: MM/YY')
    cvv = forms.IntegerField(label='CVV', required=True)
    cardHolder = forms.CharField(label='Nombre del titular', max_length=60, required=True)
    

    