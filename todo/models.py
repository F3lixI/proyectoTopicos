from django.db import models
from django.contrib.auth.models import User

#Clase mostrada en el ejemplo
class ToDo(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self) -> str:
        return f"{self.text}"
    
class Flores(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50)
    small_image = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    dimension = models.CharField(max_length=30, null=True, blank=True)
    large_image = models.URLField()
    extra_large_image = models.URLField(null=True, blank=True)
    service = models.CharField(max_length=1, null=True, blank=True)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    producto_id = models.IntegerField()
    display = models.CharField(max_length=50)
    categoria = models.CharField(max_length=10)
    
    def __str__(self):
        return self.display
    
class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()
    fecha_creacion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    edad = models.IntegerField()
    sexo = models.CharField(max_length=1, null=True, blank=True)
    
    def __str__(self):
        return self.nombre

#Direccion de un cliente    
class Direccion(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    calle = models.CharField(max_length=50)
    numero = models.IntegerField()
    colonia = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=6)
    
    def __str__(self):
        return self.calle

    
class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.id) + " " + str(self.cliente) + " " + str(self.fecha) + " " + str(self.total) + " " + str(self.estado)
    
class DetalleOrden(models.Model):
    id = models.AutoField(primary_key=True)
    productos = models.ManyToManyField(Flores)
    id_orden  = models.ForeignKey(Orden, on_delete=models.CASCADE, null=True, blank=True)
    calle = models.CharField(max_length=50, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    colonia = models.CharField(max_length=50, null=True, blank=True)
    ciudad = models.CharField(max_length=50, null=True, blank=True)
    codigo_postal = models.CharField(max_length=6, null=True, blank=True)
    metodoPago = models.CharField(max_length=50)
    indicaciones = models.CharField(max_length=255, null=True, blank=True)
    mensaje = models.CharField(max_length=255, null=True, blank=True)
    nombreInstitucion = models.CharField(max_length=255, null=True, blank=True)
    
    
    def __str__(self):
        return str(self.id)
    



    
    
    