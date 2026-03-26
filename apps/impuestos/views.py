from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from .models import TipoImpuesto, Alicuota, ConfiguracionImpuesto


class TipoImpuestoForm(forms.ModelForm):
    class Meta:
        model = TipoImpuesto
        fields = ['nombre', 'codigo', 'tipo', 'cuenta_contable', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'codigo': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'tipo': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'cuenta_contable': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'activo': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }


class AlicuotaForm(forms.ModelForm):
    class Meta:
        model = Alicuota
        fields = ['tipo_impuesto', 'nombre', 'porcentaje', 'jurisdiccion', 'fecha_desde', 'fecha_hasta', 'por_defecto']
        widgets = {
            'tipo_impuesto': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'porcentaje': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2', 'step': '0.01'}),
            'jurisdiccion': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'fecha_desde': forms.DateInput(attrs={'class': 'w-full border rounded px-3 py-2', 'type': 'date'}),
            'fecha_hasta': forms.DateInput(attrs={'class': 'w-full border rounded px-3 py-2', 'type': 'date'}),
            'por_defecto': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }


@login_required
def index(request):
    return render(request, 'impuestos/index.html')


@login_required
def tipos(request):
    tipos = TipoImpuesto.objects.all().order_by('nombre')
    return render(request, 'impuestos/tipos.html', {'tipos': tipos})


@login_required
def tipo_create(request):
    if request.method == 'POST':
        form = TipoImpuestoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de impuesto creado correctamente')
            return redirect('impuestos:tipos')
    else:
        form = TipoImpuestoForm()
    return render(request, 'impuestos/tipo_form.html', {'form': form, 'action': 'Crear'})


@login_required
def tipo_edit(request, pk):
    tipo = get_object_or_404(TipoImpuesto, pk=pk)
    if request.method == 'POST':
        form = TipoImpuestoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de impuesto actualizado correctamente')
            return redirect('impuestos:tipos')
    else:
        form = TipoImpuestoForm(instance=tipo)
    return render(request, 'impuestos/tipo_form.html', {'form': form, 'tipo': tipo, 'action': 'Editar'})


@login_required
def tipo_delete(request, pk):
    tipo = get_object_or_404(TipoImpuesto, pk=pk)
    if request.method == 'POST':
        tipo.delete()
        messages.success(request, 'Tipo de impuesto eliminado correctamente')
        return redirect('impuestos:tipos')
    return render(request, 'impuestos/tipo_confirm_delete.html', {'tipo': tipo})


@login_required
def alicuotas(request):
    alicuotas = Alicuota.objects.select_related('tipo_impuesto').order_by('-fecha_desde')
    return render(request, 'impuestos/alicuotas.html', {'alicuotas': alicuotas})


@login_required
def alicuota_create(request):
    if request.method == 'POST':
        form = AlicuotaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alícuota creada correctamente')
            return redirect('impuestos:alicuotas')
    else:
        form = AlicuotaForm()
    return render(request, 'impuestos/alicuota_form.html', {'form': form, 'action': 'Crear'})


@login_required
def alicuota_edit(request, pk):
    alicuota = get_object_or_404(Alicuota, pk=pk)
    if request.method == 'POST':
        form = AlicuotaForm(request.POST, instance=alicuota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alícuota actualizada correctamente')
            return redirect('impuestos:alicuotas')
    else:
        form = AlicuotaForm(instance=alicuota)
    return render(request, 'impuestos/alicuota_form.html', {'form': form, 'alicuota': alicuota, 'action': 'Editar'})


@login_required
def alicuota_delete(request, pk):
    alicuota = get_object_or_404(Alicuota, pk=pk)
    if request.method == 'POST':
        alicuota.delete()
        messages.success(request, 'Alícuota eliminada correctamente')
        return redirect('impuestos:alicuotas')
    return render(request, 'impuestos/alicuota_confirm_delete.html', {'alicuota': alicuota})
