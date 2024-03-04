from django.db import models

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
    dimension = models.CharField(max_length=30)
    large_image = models.URLField()
    extra_large_image = models.URLField()
    service = models.CharField(max_length=1)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
