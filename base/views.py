from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DeleteView
from .models import Asistencia
from django.urls import reverse_lazy


# Create your views here.
class ListaRegistrados(ListView):
    model = Asistencia
    context_object_name = 'registrados'
    template_name = 'base/registro_asistencia.html'


class EliminarRegistro(DeleteView):
    model = Asistencia
    context_object_name = 'registro'
    template_name = 'base/confirmar_eliminacion_reg.html'
    success_url = reverse_lazy('registrados')
