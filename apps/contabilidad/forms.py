from django import forms
from .models import CuentaContable, Ejercicio, Asiento, LineaAsiento


class CuentaForm(forms.ModelForm):
    class Meta:
        model = CuentaContable
        fields = ['codigo', 'nombre', 'tipo', 'padre', 'acepta_movimientos', 'activa']


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'ejercicio_anterior']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }


class AsientoForm(forms.ModelForm):
    class Meta:
        model = Asiento
        fields = ['ejercicio', 'numero', 'fecha', 'descripcion', 'origen', 'estado', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }


class LineaAsientoForm(forms.ModelForm):
    class Meta:
        model = LineaAsiento
        fields = ['cuenta', 'debe', 'haber', 'descripcion']
        widgets = {
            'debe': forms.NumberInput(attrs={'step': '0.01'}),
            'haber': forms.NumberInput(attrs={'step': '0.01'}),
        }
