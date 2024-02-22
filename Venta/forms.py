
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


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
        

class PrecioForm(forms.Form):
    precio_min = forms.DecimalField(label='Precio mínimo', required=False)
    precio_max = forms.DecimalField(label='Precio máximo')
    