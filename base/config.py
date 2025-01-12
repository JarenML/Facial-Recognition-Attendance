import os
import sys
import django

# Se determina el directorio base del proyecto
current_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(current_path)

# agregando el proyecto al PYTHONPATH
sys.path.append(project_path)

# Inicializando DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()