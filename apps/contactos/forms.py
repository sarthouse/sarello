from django import forms
from .models import Contacto


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'tipo', 'codigo', 'cuil', 'condicion_iva', 'direccion', 'telefono', 'email', 'ciudad', 'provincia', 'codigo_postal', 'contacto_principal', 'notas', 'activo', 'limite_credito']
