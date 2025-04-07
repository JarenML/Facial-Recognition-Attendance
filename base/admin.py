from django.contrib import admin
from .models import Detectado
from .models import Registrado

# Register your models here.
admin.site.register(Detectado)
admin.site.register(Registrado)