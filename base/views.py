from django.shortcuts import render, redirect
from .models import Detectado

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



