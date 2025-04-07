from django import forms
from .models import Registrado

class RegistradoForm(forms.ModelForm):
    class Meta:
        model = Registrado
        fields = '__all__'