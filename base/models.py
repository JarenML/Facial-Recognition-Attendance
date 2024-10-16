from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Asistencia(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)

    def __str__(self):
        return f'{self.nombre} - {self.fecha} {self.hora}'
