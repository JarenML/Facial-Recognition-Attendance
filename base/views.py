from django.shortcuts import render, redirect
from .models import Detectado
from .forms import RegistradoForm
from .models import Registrado

# Create your views here.
def listar_detectados(request):
    detectados = Detectado.objects.all()
    context = {
        'detectados': detectados
    }

    return render(request, 'base/detectados_list.html', context)


def eliminar_detectado(request, id):
    detectado = Detectado.objects.get(id=id)
    if request.method == "POST":
        detectado.delete()
        return redirect('detectados')

    context = {
        'detectado': detectado
    }

    return render(request, 'base/detectado_delete.html', context)

def mostrar_registrados(request):
    registrados = Registrado.objects.all()
    return render(request, 'base/registrados.html', {'registrados': registrados})

import os
from django.utils.text import slugify

def agregar_registro(request):
    form = RegistradoForm()
    if request.method == 'POST':
        form = RegistradoForm(request.POST, request.FILES)
        if form.is_valid():
            registro = form.save(commit=False)

            if 'imagen' in request.FILES:
                imagen_original = request.FILES['imagen']
                extension = os.path.splitext(imagen_original.name)[1]
                nuevo_nombre = f"{slugify(registro.nombre)}{extension}"
                imagen_original.name = nuevo_nombre

                registro.imagen = imagen_original

            registro.save()
            return redirect('registrados')
    return render(request, 'base/nuevo_registro.html', {'form': form})

    
    
        



