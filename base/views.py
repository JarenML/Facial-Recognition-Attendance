from django.shortcuts import render, redirect
from .models import Asistencia

# Create your views here.
def listar_detectados(request):
    detectados = Asistencia.objects.all()
    context = {
        'detectados': detectados
    }

    return render(request, 'base/detectados_list.html', context)


def eliminar_detectado(request, id):
    detectado = Asistencia.objects.get(id=id)
    if request.method == "POST":
        detectado.delete()
        return redirect('detectados')

    context = {
        'detectado': detectado
    }

    return render(request, 'base/detectado_delete.html', context)



