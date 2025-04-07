from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path('detectados/', views.listar_detectados, name='detectados'),
               path('eliminar-detectado/<int:id>', views.eliminar_detectado, name='eliminar'),
               path('registrados/', views.mostrar_registrados, name='registrados'),
               path('nuevo_registro/', views.agregar_registro, name='agregar_registro')]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
