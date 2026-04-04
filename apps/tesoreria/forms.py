from django import forms
from django.forms import inlineformset_factory
from .models import CuentaTesoreria, MovimientoTesoreria, LineaMovimientoTesoreria


class CuentaTesoreriaForm(forms.ModelForm):
    class Meta:
        model = CuentaTesoreria
        fields = ['nombre', 'tipo', 'cuenta_contable', 'moneda', 'saldo_inicial', 'activa']


class MovimientoTesoreriaForm(forms.ModelForm):
    class Meta:
        model = MovimientoTesoreria
        fields = ['tipo', 'fecha', 'contacto', 'estado', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['observaciones'].widget.attrs.update({
            'rows': 3,
            'class': 'w-full border rounded px-3 py-2',
        })


class LineaMovimientoForm(forms.ModelForm):
    class Meta:
        model = LineaMovimientoTesoreria
        fields = ['cuenta', 'debe', 'haber', 'cuenta_contrapartida', 'descripcion']


LineaMovimientoFormSet = inlineformset_factory(
    MovimientoTesoreria,
    LineaMovimientoTesoreria,
    form=LineaMovimientoForm,
    extra=1,
    can_delete=True,
)
