from django.urls import path
from . import views


urlpatterns = [path('detectados/', views.listar_detectados, name='detectados'),
               path('eliminar-detectado/<int:id>', views.eliminar_detectado, name='eliminar')]
