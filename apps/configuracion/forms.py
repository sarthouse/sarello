from django import forms
from .models import ParametroSistema, DatosEmpresa


class ParametroForm(forms.ModelForm):
    class Meta:
        model = ParametroSistema
        fields = ['clave', 'valor', 'descripcion', 'grupo', 'editable']


class DatosEmpresaForm(forms.ModelForm):
    class Meta:
        model = DatosEmpresa
        fields = [
            'razon_social', 'nombre_fantasia', 'cuil', 'direccion',
            'telefono', 'email', 'web', 'condicion_iva',
            'numero_ingresos_brutos', 'inicio_actividades', 'logo'
        ]
        widgets = {
            'inicio_actividades': forms.DateInput(attrs={'type': 'date'}),
        }
