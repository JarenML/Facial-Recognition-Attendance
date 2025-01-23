from django.shortcuts import render, redirect
from .models import Asistencia

# Create your views here.
def listar_detectados(request):
    detectados = Asistencia.objects.all()
    context = {
        'detectados': detectados
    }

    return render(request, 'base/registro_asistencia.html', context)


def eliminar_detectado(request, id):
    detectado = Asistencia.objects.get(id=id)
    if request.method == "POST":
        detectado.delete()
        return redirect('detectados')

    context = {
        'detectado': detectado
    }

    return render(request, 'base/confirmar_eliminacion_reg.html', context)



