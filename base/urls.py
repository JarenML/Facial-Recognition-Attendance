from django.urls import path
from .views import ListaRegistrados, EliminarRegistro


urlpatterns = [path('registrados/', ListaRegistrados.as_view(), name='registrados'),
               path('eliminar-registro/<int:pk>', EliminarRegistro.as_view(), name='eliminar')]
