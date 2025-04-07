from django.forms import Form
from .models import Registrado

class RegistradoForm(Form):
    class Meta:
        model = Registrado
        fields = '__all__'