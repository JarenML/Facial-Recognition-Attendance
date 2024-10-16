from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DeleteView
from .models import Asistencia
from django.urls import reverse_lazy


# Create your views here.
def lista_pendientes(pedido):
    return HttpResponse("Lista de pendientes")


def mostrar_registrados(request):
    with open('base/asistencia.csv', 'r') as archivo:
        registros = archivo.readlines()

    contexto = {'registros': registros}

    return render(request, 'base/registro_asistencia.html', contexto)


class ListaRegistrados(ListView):
    model = Asistencia
    context_object_name = 'registrados'
    template_name = 'base/registro_asistencia.html'


class EliminarRegistro(DeleteView):
    model = Asistencia
    context_object_name = 'registro'
    template_name = 'base/confirmar_eliminacion_reg.html'
    success_url = reverse_lazy('registrados')
