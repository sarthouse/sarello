from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.core.exceptions import ValidationError
from .models import CuentaTesoreria, MovimientoTesoreria
from .forms import CuentaTesoreriaForm, MovimientoTesoreriaForm, LineaMovimientoFormSet


@login_required
def index(request):
    cuentas = CuentaTesoreria.objects.filter(activa=True).select_related('cuenta_contable')
    total_ars = sum(c.saldo_contable for c in cuentas.filter(moneda='ARS'))
    total_usd = sum(c.saldo_contable for c in cuentas.filter(moneda='USD'))

    conciliaciones = {}
    for cuenta in cuentas:
        conc = cuenta.conciliar()
        conciliaciones[cuenta.pk] = conc['conciliado']

    return render(request, 'tesoreria/index.html', {
        'cuentas': cuentas,
        'total_ars': total_ars,
        'total_usd': total_usd,
        'conciliaciones': conciliaciones,
    })


@login_required
def cuentas(request):
    cuentas = CuentaTesoreria.objects.select_related('cuenta_contable').all().order_by('tipo', 'nombre')
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
        if cuenta.lineas.exists():
            messages.error(request, 'No se puede eliminar una cuenta con movimientos')
            return redirect('tesoreria:cuentas')
        cuenta.delete()
        messages.success(request, 'Cuenta eliminada correctamente')
        return redirect('tesoreria:cuentas')
    return render(request, 'tesoreria/cuenta_confirm_delete.html', {'cuenta': cuenta})


@login_required
def movimientos(request):
    cuenta_id = request.GET.get('cuenta')
    tipo = request.GET.get('tipo')
    estado = request.GET.get('estado')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    qs = MovimientoTesoreria.objects.select_related('contacto').prefetch_related('lineas__cuenta').order_by('-fecha', '-numero')

    if cuenta_id:
        qs = qs.filter(lineas__cuenta_id=cuenta_id).distinct()
    if tipo:
        qs = qs.filter(tipo=tipo)
    if estado:
        qs = qs.filter(estado=estado)
    if fecha_desde:
        qs = qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        qs = qs.filter(fecha__lte=fecha_hasta)

    cuentas = CuentaTesoreria.objects.filter(activa=True)

    paginator = Paginator(qs, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'tesoreria/movimientos.html', {
        'page_obj': page_obj,
        'cuentas': cuentas,
        'cuenta_filter': cuenta_id,
        'tipo_filter': tipo,
        'estado_filter': estado,
    })


@login_required
def movimiento_create(request):
    if request.method == 'POST':
        form = MovimientoTesoreriaForm(request.POST)
        formset = LineaMovimientoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            movimiento = form.save(commit=False)
            movimiento.estado = 'confirmado'
            movimiento.save()

            lineas = formset.save(commit=False)
            for linea in lineas:
                linea.movimiento = movimiento
                linea.save()

            formset.save_m2m()

            messages.success(request, f"{'Cobro' if movimiento.tipo == 'cobro' else 'Pago' if movimiento.tipo == 'pago' else 'Transferencia'} registrado correctamente")
            return redirect('tesoreria:movimientos')
    else:
        form = MovimientoTesoreriaForm()
        formset = LineaMovimientoFormSet()

    return render(request, 'tesoreria/movimiento_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Crear',
    })


@login_required
def movimiento_edit(request, pk):
    movimiento = get_object_or_404(MovimientoTesoreria, pk=pk)

    if movimiento.estado not in ('borrador',):
        messages.error(request, 'Solo se pueden editar movimientos en borrador')
        return redirect('tesoreria:movimientos')

    if request.method == 'POST':
        form = MovimientoTesoreriaForm(request.POST, instance=movimiento)
        formset = LineaMovimientoFormSet(request.POST, instance=movimiento)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Movimiento actualizado correctamente')
            return redirect('tesoreria:movimientos')
    else:
        form = MovimientoTesoreriaForm(instance=movimiento)
        formset = LineaMovimientoFormSet(instance=movimiento)

    return render(request, 'tesoreria/movimiento_form.html', {
        'form': form,
        'formset': formset,
        'movimiento': movimiento,
        'action': 'Editar',
    })


@login_required
def movimiento_anular(request, pk):
    movimiento = get_object_or_404(MovimientoTesoreria, pk=pk)

    if movimiento.estado != 'confirmado':
        messages.error(request, 'Solo se pueden anular movimientos confirmados')
        return redirect('tesoreria:movimientos')

    if request.method == 'POST':
        try:
            movimiento.estado = 'anulado'
            movimiento.save()
            messages.success(request, 'Movimiento anulado correctamente')
        except ValidationError as e:
            messages.error(request, str(e))
        return redirect('tesoreria:movimientos')

    return render(request, 'tesoreria/movimiento_confirm_anular.html', {
        'movimiento': movimiento,
    })


@login_required
def movimiento_delete(request, pk):
    movimiento = get_object_or_404(MovimientoTesoreria, pk=pk)

    if movimiento.estado == 'confirmado':
        messages.error(request, 'No se puede eliminar un movimiento confirmado. Anulelo primero.')
        return redirect('tesoreria:movimientos')

    if request.method == 'POST':
        movimiento.delete()
        messages.success(request, 'Movimiento eliminado correctamente')
        return redirect('tesoreria:movimientos')

    return render(request, 'tesoreria/movimiento_confirm_delete.html', {'movimiento': movimiento})


@login_required
def movimiento_detail(request, pk):
    movimiento = get_object_or_404(
        MovimientoTesoreria.objects.prefetch_related('lineas__cuenta', 'lineas__cuenta_contrapartida'),
        pk=pk
    )
    return render(request, 'tesoreria/movimiento_detail.html', {
        'movimiento': movimiento,
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
    total_ingresos = Decimal('0')
    total_egresos = Decimal('0')

    for cuenta in cuentas:
        lineas_dia = cuenta.lineas.filter(movimiento__fecha=fecha)

        ingresos = lineas_dia.aggregate(total=Sum('debe'))['total'] or Decimal('0')
        egresos = lineas_dia.aggregate(total=Sum('haber'))['total'] or Decimal('0')

        datos_caja.append({
            'cuenta': cuenta,
            'ingresos': ingresos,
            'egresos': egresos,
            'saldo_dia': ingresos - egresos,
            'saldo_acumulado': cuenta.saldo_tesoreria,
        })

        total_ingresos += ingresos
        total_egresos += egresos

    movimientos_dia = MovimientoTesoreria.objects.filter(
        fecha=fecha,
        lineas__cuenta__in=cuentas
    ).select_related('contacto').prefetch_related('lineas__cuenta').distinct().order_by('-numero')

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
    conciliaciones = []
    for cuenta in cuentas:
        conc = cuenta.conciliar()
        conciliaciones.append({
            'cuenta': cuenta,
            **conc,
        })
    return render(request, 'tesoreria/saldo_cuentas.html', {'conciliaciones': conciliaciones})


@login_required
def conciliar_cuentas(request):
    cuentas = CuentaTesoreria.objects.filter(activa=True).order_by('tipo', 'nombre')
    resultados = []
    for cuenta in cuentas:
        conc = cuenta.conciliar()
        resultados.append({
            'cuenta': cuenta,
            'saldo_tesoreria': conc['saldo_tesoreria'],
            'saldo_contable': conc['saldo_contable'],
            'diferencia': conc['diferencia'],
            'conciliado': conc['conciliado'],
        })
    return render(request, 'tesoreria/conciliar.html', {
        'resultados': resultados,
    })


@login_required
def crear_ajuste_desde_conciliacion(request, cuenta_pk):
    cuenta = get_object_or_404(CuentaTesoreria, pk=cuenta_pk)
    conc = cuenta.conciliar()

    if request.method == 'POST':
        form = MovimientoTesoreriaForm(request.POST)
        formset = LineaMovimientoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            movimiento = form.save(commit=False)
            movimiento.estado = 'confirmado'
            movimiento.save()

            lineas = formset.save(commit=False)
            for linea in lineas:
                linea.movimiento = movimiento
                linea.save()

            formset.save_m2m()

            messages.success(request, 'Ajuste de saldo registrado correctamente')
            return redirect('tesoreria:conciliar')
    else:
        form = MovimientoTesoreriaForm(initial={
            'tipo': 'ajuste',
            'observaciones': f'Ajuste por conciliación - Diferencia: {conc["diferencia"]}',
        })
        formset = LineaMovimientoFormSet()

    return render(request, 'tesoreria/movimiento_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Crear Ajuste',
        'ajuste_cuenta': cuenta,
        'ajuste_diferencia': conc['diferencia'],
    })
