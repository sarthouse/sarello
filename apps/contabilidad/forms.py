from django import forms
from .models import CuentaContable, Ejercicio, Asiento, LineaAsiento

class CuentaForm(forms.ModelForm):
    class Meta:
        model = CuentaContable
        fields = ['codigo', 'nombre', 'tipo', 'padre', 'acepta_movimientos', 'activa']
        widgets = {
            'codigo': forms.TextInput(),
            'nombre': forms.TextInput(),
            'tipo': forms.Select(),
            'padre': forms.Select(),
            'acepta_movimientos': forms.CheckboxInput(),
            'activa': forms.CheckboxInput(),
        }


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'ejercicio_anterior']
        widgets = {
            'nombre': forms.TextInput(),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'estado': forms.Select(attrs={}),
            'ejercicio_anterior': forms.Select(attrs={}),
        }


class AsientoForm(forms.ModelForm):
    class Meta:
        model = Asiento
        fields = ['ejercicio', 'numero', 'fecha', 'descripcion', 'origen', 'estado', 'observaciones']
        widgets = {
            'ejercicio': forms.Select(attrs={}),
            'numero': forms.TextInput(attrs={}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.TextInput(attrs={}),
            'origen': forms.Select(attrs={}),
            'estado': forms.Select(attrs={}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }


class LineaAsientoForm(forms.ModelForm):
    class Meta:
        model = LineaAsiento
        fields = ['cuenta', 'debe', 'haber', 'descripcion']
        widgets = {
            'cuenta': forms.Select(attrs={}),
            'debe': forms.NumberInput(attrs={'step': '0.01'}),
            'haber': forms.NumberInput(attrs={'step': '0.01'}),
            'descripcion': forms.TextInput(attrs={}),
        }