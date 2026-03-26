from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django import forms
from django.db.models import Sum
from .models import CuentaTesoreria, MovimientoTesoreria


class CuentaTesoreriaForm(forms.ModelForm):
    class Meta:
        model = CuentaTesoreria
        fields = ['nombre', 'tipo', 'cuenta_contable', 'moneda', 'saldo_inicial', 'activa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'tipo': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'cuenta_contable': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'moneda': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'saldo_inicial': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2', 'step': '0.01'}),
            'activa': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }


class MovimientoTesoreriaForm(forms.ModelForm):
    class Meta:
        model = MovimientoTesoreria
        fields = ['cuenta', 'tipo', 'importe', 'fecha', 'contacto', 'descripcion', 'observaciones']
        widgets = {
            'cuenta': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'tipo': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'importe': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2', 'step': '0.01'}),
            'fecha': forms.DateInput(attrs={'class': 'w-full border rounded px-3 py-2', 'type': 'date'}),
            'contacto': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'descripcion': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'observaciones': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2', 'rows': 2}),
        }


@login_required
def index(request):
    cuentas = CuentaTesoreria.objects.filter(activa=True)
    total_ars = sum(c.saldo_actual for c in cuentas.filter(moneda='ARS'))
    total_usd = sum(c.saldo_actual for c in cuentas.filter(moneda='USD'))
    
    movimientos_hoy = MovimientoTesoreria.objects.filter(fecha__exact=request.today).order_by('-numero')[:10] if hasattr(request, 'today') else []
    
    return render(request, 'tesoreria/index.html', {
        'cuentas': cuentas,
        'total_ars': total_ars,
        'total_usd': total_usd,
    })


@login_required
def cuentas(request):
    cuentas = CuentaTesoreria.objects.all().order_by('tipo', 'nombre')
    return render(request, 'tesoreria/cuentas.html', {'cuentas': cuentas})


@login_required
def cuenta_create(request):
    if request.method == 'POST':
        form = CuentaTesoreriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta de tesorería creada correctamente')
            return redirect('tesoreria:cuentas')
    else:
        form = CuentaTesoreriaForm()
    return render(request, 'tesoreria/cuenta_form.html', {'form': form, 'action': 'Crear'})


@login_required
def cuenta_edit(request, pk):
    cuenta = get_object_or_404(CuentaTesoreria, pk=pk)
    if request.method == 'POST':
        form = CuentaTesoreriaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta actualizada correctamente')
            return redirect('tesoreria:cuentas')
    else:
        form = CuentaTesoreriaForm(instance=cuenta)
    return render(request, 'tesoreria/cuenta_form.html', {'form': form, 'cuenta': cuenta, 'action': 'Editar'})


@login_required
def cuenta_delete(request, pk):
    cuenta = get_object_or_404(CuentaTesoreria, pk=pk)
    if request.method == 'POST':
        cuenta.delete()
        messages.success(request, 'Cuenta eliminada correctamente')
        return redirect('tesoreria:cuentas')
    return render(request, 'tesoreria/cuenta_confirm_delete.html', {'cuenta': cuenta})


@login_required
def movimientos(request):
    cuenta_id = request.GET.get('cuenta')
    tipo = request.GET.get('tipo')
    fechaDesde = request.GET.get('fechaDesde')
    fechaHasta = request.GET.get('fechaHasta')
    
    movimientos = MovimientoTesoreria.objects.select_related('cuenta', 'contacto').order_by('-fecha', '-numero')
    
    if cuenta_id:
        movimientos = movimientos.filter(cuenta_id=cuenta_id)
    if tipo:
        movimientos = movimientos.filter(tipo=tipo)
    if fechaDesde:
        movimientos = movimientos.filter(fecha__gte=fechaDesde)
    if fechaHasta:
        movimientos = movimientos.filter(fecha__lte=fechaHasta)
    
    cuentas = CuentaTesoreria.objects.filter(activa=True)
    
    paginator = Paginator(movimientos, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'tesoreria/movimientos.html', {
        'page_obj': page_obj,
        'cuentas': cuentas,
        'cuenta_filter': cuenta_id,
        'tipo_filter': tipo,
    })


@login_required
def movimiento_create(request, tipo_movimiento=None):
    if request.method == 'POST':
        form = MovimientoTesoreriaForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.estado = 'confirmado'
            movimiento.save()
            messages.success(request, f"{'Ingreso' if movimiento.tipo == 'cobro' else 'Egreso'} registrado correctamente")
            return redirect('tesoreria:movimientos')
    else:
        form = MovimientoTesoreriaForm()
        if tipo_movimiento:
            form.initial['tipo'] = tipo_movimiento
    
    return render(request, 'tesoreria/movimiento_form.html', {
        'form': form,
        'action': 'Crear',
        'tipo_movimiento': tipo_movimiento
    })


@login_required
def movimiento_edit(request, pk):
    movimiento = get_object_or_404(MovimientoTesoreria, pk=pk)
    if request.method == 'POST':
        form = MovimientoTesoreriaForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento actualizado correctamente')
            return redirect('tesoreria:movimientos')
    else:
        form = MovimientoTesoreriaForm(instance=movimiento)
    return render(request, 'tesoreria/movimiento_form.html', {
        'form': form,
        'movimiento': movimiento,
        'action': 'Editar'
    })


@login_required
def movimiento_delete(request, pk):
    movimiento = get_object_or_404(MovimientoTesoreria, pk=pk)
    if request.method == 'POST':
        movimiento.delete()
        messages.success(request, 'Movimiento eliminado correctamente')
        return redirect('tesoreria:movimientos')
    return render(request, 'tesoreria/movimiento_confirm_delete.html', {'movimiento': movimiento})


@login_required
def ingresos(request):
    cuenta_id = request.GET.get('cuenta')
    
    cuentas = CuentaTesoreria.objects.filter(activa=True)
    
    if request.method == 'POST':
        form = MovimientoTesoreriaForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.tipo = 'cobro'
            movimiento.estado = 'confirmado'
            movimiento.save()
            messages.success(request, 'Ingreso registrado correctamente')
            return redirect('tesoreria:ingresos')
    else:
        form = MovimientoTesoreriaForm()
        if cuenta_id:
            form.initial['cuenta'] = cuenta_id
            form.initial['tipo'] = 'cobro'
    
    return render(request, 'tesoreria/ingresos.html', {
        'form': form,
        'cuentas': cuentas,
    })


@login_required
def egresos(request):
    cuenta_id = request.GET.get('cuenta')
    
    cuentas = CuentaTesoreria.objects.filter(activa=True)
    
    if request.method == 'POST':
        form = MovimientoTesoreriaForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.tipo = 'pago'
            movimiento.estado = 'confirmado'
            movimiento.save()
            messages.success(request, 'Egreso registrado correctamente')
            return redirect('tesoreria:egresos')
    else:
        form = MovimientoTesoreriaForm()
        if cuenta_id:
            form.initial['cuenta'] = cuenta_id
            form.initial['tipo'] = 'pago'
    
    return render(request, 'tesoreria/egresos.html', {
        'form': form,
        'cuentas': cuentas,
    })


@login_required
def caja_diaria(request):
    from datetime import date
    
    fecha = request.GET.get('fecha')
    if fecha:
        fecha = date.fromisoformat(fecha)
    else:
        fecha = date.today()
    
    cuentas = CuentaTesoreria.objects.filter(tipo='caja', activa=True)
    
    datos_caja = []
    total_ingresos = 0
    total_egresos = 0
    
    for cuenta in cuentas:
        ingresos = MovimientoTesoreria.objects.filter(
            cuenta=cuenta,
            fecha=fecha,
            tipo='cobro'
        ).aggregate(total=Sum('importe'))['total'] or 0
        
        egresos = MovimientoTesoreria.objects.filter(
            cuenta=cuenta,
            fecha=fecha,
            tipo='pago'
        ).aggregate(total=Sum('importe'))['total'] or 0
        
        datos_caja.append({
            'cuenta': cuenta,
            'ingresos': ingresos,
            'egresos': egresos,
            'saldo_dia': ingresos - egresos,
            'saldo_acumulado': cuenta.saldo_inicial + (
                MovimientoTesoreria.objects.filter(
                    cuenta=cuenta,
                    fecha__lte=fecha,
                    tipo='cobro'
                ).aggregate(total=Sum('importe'))['total'] or 0
            ) - (
                MovimientoTesoreria.objects.filter(
                    cuenta=cuenta,
                    fecha__lte=fecha,
                    tipo='pago'
                ).aggregate(total=Sum('importe'))['total'] or 0
            )
        })
        
        total_ingresos += ingresos
        total_egresos += egresos
    
    movimientos_dia = MovimientoTesoreria.objects.filter(
        fecha=fecha,
        cuenta__in=cuentas
    ).select_related('cuenta', 'contacto').order_by('-numero')
    
    return render(request, 'tesoreria/caja_diaria.html', {
        'fecha': fecha,
        'datos_caja': datos_caja,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'movimientos_dia': movimientos_dia,
    })


@login_required
def saldo_cuentas(request):
    cuentas = CuentaTesoreria.objects.filter(activa=True).order_by('tipo', 'nombre')
    return render(request, 'tesoreria/saldo_cuentas.html', {'cuentas': cuentas})
