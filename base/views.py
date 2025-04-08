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

def agregar_registro(request):
    form = RegistradoForm()
    if request.method == 'POST':
        form = RegistradoForm(request.POST, request.FILES)
        print("FORM:", form)
        print(form.instance.imagen.url)
        if form.is_valid():
            form.save()
            return redirect('registrados')
    return render(request, 'base/nuevo_registro.html', {'form': form})
    
    
        



