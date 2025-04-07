from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Detectado(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)

    def __str__(self):
        return f'{self.nombre} - {self.fecha} {self.hora}'
    
class Registrado(models.Model):
    nombre = models.CharField(max_length=100)
    informacion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='registrados/', null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateField(auto_created=True)

    def __str__(self):
        return self.nombre



