import csv
import io
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.http import JsonResponse
from django import forms
from .models import CuentaContable, Ejercicio, Asiento, LineaAsiento


class CuentaForm(forms.ModelForm):
    class Meta:
        model = CuentaContable
        fields = ['codigo', 'nombre', 'tipo', 'padre', 'acepta_movimientos', 'activa']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'tipo': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'padre': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'acepta_movimientos': forms.CheckboxInput(attrs={'class': 'rounded'}),
            'activa': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }


class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'estado', 'ejercicio_anterior']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'w-full border rounded px-3 py-2', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'w-full border rounded px-3 py-2', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'ejercicio_anterior': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }


class AsientoForm(forms.ModelForm):
    class Meta:
        model = Asiento
        fields = ['ejercicio', 'numero', 'fecha', 'descripcion', 'origen', 'estado', 'observaciones']
        widgets = {
            'ejercicio': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'numero': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'fecha': forms.DateInput(attrs={'class': 'w-full border rounded px-3 py-2', 'type': 'date'}),
            'descripcion': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'origen': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'estado': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'observaciones': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2', 'rows': 2}),
        }


class LineaAsientoForm(forms.ModelForm):
    class Meta:
        model = LineaAsiento
        fields = ['cuenta', 'debe', 'haber', 'descripcion']
        widgets = {
            'cuenta': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'debe': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2', 'step': '0.01'}),
            'haber': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2', 'step': '0.01'}),
            'descripcion': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
        }


@login_required
def cuenta_create(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada correctamente')
            return redirect('contabilidad:plan_cuentas')
    else:
        form = CuentaForm()
    
    cuentas = CuentaContable.objects.filter(padre__isnull=True, activa=True)
    return render(request, 'contabilidad/cuenta_form.html', {
        'form': form,
        'cuentas': cuentas,
        'action': 'Crear'
    })


@login_required
def cuenta_edit(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    
    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta actualizada correctamente')
            return redirect('contabilidad:plan_cuentas')
    else:
        form = CuentaForm(instance=cuenta)
    
    cuentas = CuentaContable.objects.filter(padre__isnull=True, activa=True).exclude(pk=pk)
    return render(request, 'contabilidad/cuenta_form.html', {
        'form': form,
        'cuentas': cuentas,
        'cuenta': cuenta,
        'action': 'Editar'
    })


@login_required
def cuenta_delete(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    
    if request.method == 'POST':
        if cuenta.lineas.exists():
            messages.error(request, 'No se puede eliminar una cuenta con movimientos')
            return redirect('contabilidad:plan_cuentas')
        cuenta.delete()
        messages.success(request, 'Cuenta eliminada correctamente')
        return redirect('contabilidad:plan_cuentas')
    
    return render(request, 'contabilidad/cuenta_confirm_delete.html', {
        'cuenta': cuenta
    })


@login_required
def ejercicio_create(request):
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ejercicio creado correctamente')
            return redirect('contabilidad:dashboard')
    else:
        form = EjercicioForm()
    
    return render(request, 'contabilidad/ejercicio_form.html', {
        'form': form,
        'action': 'Crear'
    })


@login_required
def ejercicio_edit(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    
    if request.method == 'POST':
        form = EjercicioForm(request.POST, instance=ejercicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ejercicio actualizado correctamente')
            return redirect('contabilidad:dashboard')
    else:
        form = EjercicioForm(instance=ejercicio)
    
    return render(request, 'contabilidad/ejercicio_form.html', {
        'form': form,
        'ejercicio': ejercicio,
        'action': 'Editar'
    })


@login_required
def dashboard(request):
    ejercicios = Ejercicio.objects.filter(estado='abierto')[:1]
    ejercicio_actual = ejercicios.first()
    
    cuentas_total = CuentaContable.objects.filter(activa=True).count()
    cuentas_raiz = CuentaContable.objects.filter(padre__isnull=True, activa=True)
    
    ultimos_asientos = Asiento.objects.select_related('ejercicio').order_by('-fecha', '-numero')[:10]
    
    contexto = {
        'ejercicio_actual': ejercicio_actual,
        'cuentas_total': cuentas_total,
        'cuentas_raiz': cuentas_raiz,
        'ultimos_asientos': ultimos_asientos,
    }
    return render(request, 'contabilidad/dashboard.html', contexto)


@login_required
def plan_cuentas(request):
    cuentas = CuentaContable.objects.all().order_by('codigo')
    
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '')
    acepta_movimientos = request.GET.get('acepta_movimientos', '')
    show_inactive = request.GET.get('show_inactive', '') == '1'
    
    if not show_inactive:
        cuentas = cuentas.filter(activa=True)
    
    if q:
        cuentas = cuentas.filter(
            Q(codigo__icontains=q) |
            Q(nombre__icontains=q)
        )
    
    if tipo:
        cuentas = cuentas.filter(tipo=tipo)
    
    if acepta_movimientos == '1':
        cuentas = cuentas.filter(acepta_movimientos=True)
    elif acepta_movimientos == '0':
        cuentas = cuentas.filter(acepta_movimientos=False)
    
    paginator = Paginator(cuentas, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'contabilidad/plan_cuentas.html', {
        'page_obj': page_obj,
        'q': q,
        'tipo_filter': tipo,
        'acepta_filter': acepta_movimientos,
        'show_inactive': show_inactive,
    })


@login_required
def cuenta_detail(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    lineas = LineaAsiento.objects.filter(cuenta=cuenta).select_related('asiento').order_by('-asiento__fecha')[:50]
    
    saldo_debe = lineas.aggregate(total=Sum('debe'))['total'] or 0
    saldo_haber = lineas.aggregate(total=Sum('haber'))['total'] or 0
    
    if cuenta.tipo in ['activo', 'egreso']:
        saldo = saldo_debe - saldo_haber
    else:
        saldo = saldo_haber - saldo_debe
    
    context = {
        'cuenta': cuenta,
        'lineas': lineas,
        'saldo': saldo,
    }
    
    if request.headers.get('HX-Request'):
        return render(request, 'contabilidad/cuenta_detail_modal.html', context)
    
    return render(request, 'contabilidad/cuenta_detail.html', context)


@login_required
def lista_asientos(request):
    ejercicio_id = request.GET.get('ejercicio')
    
    ejercicios = Ejercicio.objects.filter(estado='abierto')
    asientos = Asiento.objects.select_related('ejercicio').order_by('-fecha', '-numero')
    
    if ejercicio_id:
        asientos = asientos.filter(ejercicio_id=ejercicio_id)
    else:
        asientos = asientos.filter(ejercicio__estado='abierto')
    
    paginator = Paginator(asientos, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'contabilidad/asientos.html', {
        'page_obj': page_obj,
        'ejercicios': ejercicios,
        'ejercicio_seleccionado': ejercicio_id,
    })


def asiento_detail(request, pk):
    asiento = get_object_or_404(Asiento, pk=pk)
    return render(request, 'contabilidad/asiento_detail.html', {
        'asiento': asiento,
    })


@login_required
def libro_diario(request):
    ejercicio_id = request.GET.get('ejercicio')
    
    ejercicios = Ejercicio.objects.all()
    
    if ejercicio_id:
        ejercicios_filter = ejercicios.filter(pk=ejercicio_id)
    else:
        ejercicios_filter = ejercicios.filter(estado='abierto')
    
    asientos = Asiento.objects.filter(ejercicio__in=ejercicios_filter).select_related('ejercicio').order_by('-fecha', '-numero')
    
    total_debe = sum(a.total_debe() for a in asientos)
    total_haber = sum(a.total_haber() for a in asientos)
    
    return render(request, 'contabilidad/libro_diario.html', {
        'asientos': asientos,
        'ejercicios': ejercicios,
        'ejercicio_seleccionado': ejercicio_id,
        'total_debe': total_debe,
        'total_haber': total_haber,
    })


@login_required
def mayor(request):
    ejercicio_id = request.GET.get('ejercicio')
    cuenta_id = request.GET.get('cuenta')
    
    ejercicios = Ejercicio.objects.all()
    cuentas = CuentaContable.objects.filter(activa=True, acepta_movimientos=True).order_by('codigo')
    
    lineas = None
    saldo = 0
    cuenta = None
    page_obj = None
    
    if ejercicio_id and cuenta_id:
        lineas_qs = LineaAsiento.objects.filter(
            asiento__ejercicio_id=ejercicio_id,
            cuenta_id=cuenta_id
        ).select_related('asiento').order_by('asiento__fecha', 'asiento__numero')
        
        cuenta = get_object_or_404(CuentaContable, pk=cuenta_id)
        
        saldo_acumulado = 0
        saldos_por_linea = {}
        
        for linea in lineas_qs:
            if cuenta.tipo in ['activo', 'egreso']:
                saldo_acumulado += linea.debe - linea.haber
            else:
                saldo_acumulado += linea.haber - linea.debe
            saldos_por_linea[linea.pk] = saldo_acumulado
        
        paginator = Paginator(lineas_qs, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        for linea in page_obj:
            linea.saldo_acumulado = saldos_por_linea.get(linea.pk, 0)
        
        saldo = saldo_acumulado
    
    return render(request, 'contabilidad/mayor.html', {
        'lineas': page_obj if page_obj else lineas,
        'ejercicios': ejercicios,
        'cuentas': cuentas,
        'ejercicio_seleccionado': ejercicio_id,
        'cuenta_seleccionada': cuenta_id,
        'cuenta_obj': cuenta,
        'saldo': saldo,
    })


@login_required
def balance(request):
    ejercicio_id = request.GET.get('ejercicio')
    
    if ejercicio_id:
        ejercicio = get_object_or_404(Ejercicio, pk=ejercicio_id)
    else:
        ejercicio = Ejercicio.objects.filter(estado='abierto').first()
    
    datos = []
    resultado_ejercicio = 0
    resultado_ejercicio_anterior = 0
    resultado_consolidado = 0
    
    totales = {
        'activo_t_actual': 0,
        'activo_t_anterior': 0,
        'activo_consolidado': 0,
        'pasivo_t_actual': 0,
        'pasivo_t_anterior': 0,
        'pasivo_consolidado': 0,
        'patrimonio_t_actual': 0,
        'patrimonio_t_anterior': 0,
        'patrimonio_consolidado': 0,
    }
    
    if ejercicio:
        todas_cuentas = CuentaContable.objects.filter(activa=True).order_by('codigo')
        
        t_actual = ejercicio.get_trimestre_actual() or 1
        t_anterior, anio_anterior = ejercicio.get_trimestre_anterior()
        
        fecha_t_actual_inicio, fecha_t_actual_fin = ejercicio.get_fechas_trimestre(t_actual)
        fecha_t_anterior_inicio, fecha_t_anterior_fin = ejercicio.get_fechas_trimestre(t_anterior, anio_anterior)
        
        ejercicio_consolidado = ejercicio.ejercicio_consolidado
        fecha_consolidado_inicio = None
        fecha_consolidado_fin = None
        
        if ejercicio_consolidado:
            fecha_consolidado_inicio = ejercicio_consolidado.fecha_inicio
            fecha_consolidado_fin = ejercicio_consolidado.fecha_fin
        
        def get_saldo_cuenta(cuenta, fecha_inicio, fecha_fin):
            agg = LineaAsiento.objects.filter(
                asiento__fecha__gte=fecha_inicio,
                asiento__fecha__lte=fecha_fin,
                cuenta=cuenta
            ).aggregate(debe=Sum('debe'), haber=Sum('haber'))
            
            debe = agg['debe'] or 0
            haber = agg['haber'] or 0
            
            if cuenta.tipo in ['activo', 'egreso']:
                saldo = debe - haber
            else:
                saldo = haber - debe
            
            for hijo in cuenta.hijos.all():
                saldo += get_saldo_cuenta(hijo, fecha_inicio, fecha_fin)
            
            return saldo
        
        cuentas_ingreso = CuentaContable.objects.filter(activa=True, tipo='ingreso', padre__isnull=True)
        cuentas_egreso = CuentaContable.objects.filter(activa=True, tipo='egreso', padre__isnull=True)
        
        ingreso_t_actual = sum(get_saldo_cuenta(c, fecha_t_actual_inicio, fecha_t_actual_fin) for c in cuentas_ingreso)
        ingreso_t_anterior = sum(get_saldo_cuenta(c, fecha_t_anterior_inicio, fecha_t_anterior_fin) for c in cuentas_ingreso)
        
        egreso_t_actual = sum(get_saldo_cuenta(c, fecha_t_actual_inicio, fecha_t_actual_fin) for c in cuentas_egreso)
        egreso_t_anterior = sum(get_saldo_cuenta(c, fecha_t_anterior_inicio, fecha_t_anterior_fin) for c in cuentas_egreso)
        
        resultado_t_actual = ingreso_t_actual - egreso_t_actual
        resultado_t_anterior = ingreso_t_anterior - egreso_t_anterior
        
        if ejercicio_consolidado:
            ingreso_consolidado = sum(get_saldo_cuenta(c, ejercicio_consolidado.fecha_inicio, ejercicio_consolidado.fecha_fin) for c in cuentas_ingreso)
            egreso_consolidado = sum(get_saldo_cuenta(c, ejercicio_consolidado.fecha_inicio, ejercicio_consolidado.fecha_fin) for c in cuentas_egreso)
            resultado_consolidado = ingreso_consolidado - egreso_consolidado
        
        for cuenta in todas_cuentas:
            if not (cuenta.codigo.startswith('1') or cuenta.codigo.startswith('2') or cuenta.codigo.startswith('3')):
                continue
            
            saldo_t_actual = get_saldo_cuenta(cuenta, fecha_t_actual_inicio, fecha_t_actual_fin)
            saldo_t_anterior = get_saldo_cuenta(cuenta, fecha_t_anterior_inicio, fecha_t_anterior_fin)
            
            if ejercicio_consolidado:
                saldo_consolidado = get_saldo_cuenta(cuenta, fecha_consolidado_inicio, fecha_consolidado_fin)
            else:
                saldo_consolidado = 0
            
            nivel = cuenta.codigo.count('.')
            
            seccion = ''
            if cuenta.codigo.startswith('1'):
                seccion = 'activo'
                if nivel == 0:
                    totales['activo_t_actual'] += saldo_t_actual
                    totales['activo_t_anterior'] += saldo_t_anterior
                    totales['activo_consolidado'] += saldo_consolidado
            elif cuenta.codigo.startswith('2'):
                seccion = 'pasivo'
                if nivel == 0:
                    totales['pasivo_t_actual'] += saldo_t_actual
                    totales['pasivo_t_anterior'] += saldo_t_anterior
                    totales['pasivo_consolidado'] += saldo_consolidado
            elif cuenta.codigo.startswith('3'):
                seccion = 'patrimonio'
                if nivel == 0:
                    totales['patrimonio_t_actual'] += saldo_t_actual
                    totales['patrimonio_t_anterior'] += saldo_t_anterior
                    totales['patrimonio_consolidado'] += saldo_consolidado
            
            datos.append({
                'cuenta': cuenta,
                'seccion': seccion,
                'nivel': nivel,
                'saldo_t_actual': saldo_t_actual,
                'saldo_t_anterior': saldo_t_anterior,
                'saldo_consolidado': saldo_consolidado,
            })
        
        datos.append({
            'cuenta': None,
            'seccion': 'resultado',
            'nivel': 0,
            'saldo_t_actual': resultado_t_actual,
            'saldo_t_anterior': resultado_t_anterior,
            'saldo_consolidado': resultado_consolidado,
        })
        
        resultado_ejercicio = resultado_t_actual
        resultado_ejercicio_anterior = resultado_t_anterior
        
        diferencia = totales['activo_t_actual'] - (totales['pasivo_t_actual'] + totales['patrimonio_t_actual'] + resultado_ejercicio)
        diferencia_abs = abs(diferencia)
    else:
        diferencia = 0
        diferencia_abs = 0
    
    ejercicios = Ejercicio.objects.all()
    
    ejercicio_display = ejercicio
    if ejercicio:
        t_actual = ejercicio.get_trimestre_actual() or 1
        t_anterior, anio_anterior = ejercicio.get_trimestre_anterior()
        ejercicio_display = {
            'ejercicio': ejercicio,
            't_actual': t_actual,
            't_anterior': t_anterior,
            'anio_anterior': anio_anterior,
            'ejercicio_consolidado': ejercicio.ejercicio_consolidado,
        }
    
    return render(request, 'contabilidad/balance.html', {
        'datos': datos,
        'resultado_ejercicio': resultado_ejercicio,
        'resultado_ejercicio_anterior': resultado_ejercicio_anterior,
        'resultado_consolidado': resultado_consolidado,
        'totales': totales,
        'diferencia': diferencia,
        'diferencia_abs': diferencia_abs,
        'ejercicio': ejercicio,
        'ejercicio_display': ejercicio_display,
        'ejercicios': ejercicios,
    })


@login_required
def estado_resultados(request):
    ejercicio_id = request.GET.get('ejercicio')
    
    if ejercicio_id:
        ejercicio = get_object_or_404(Ejercicio, pk=ejercicio_id)
    else:
        ejercicio = Ejercicio.objects.filter(estado='abierto').first()
    
    datos = []
    totales = {
        'ingreso_t_actual': 0,
        'ingreso_t_anterior': 0,
        'ingreso_consolidado': 0,
        'egreso_t_actual': 0,
        'egreso_t_anterior': 0,
        'egreso_consolidado': 0,
    }
    
    if ejercicio:
        cuentas_ingreso = CuentaContable.objects.filter(activa=True, tipo='ingreso').order_by('codigo')
        cuentas_egreso = CuentaContable.objects.filter(activa=True, tipo='egreso').order_by('codigo')
        
        t_actual = ejercicio.get_trimestre_actual() or 1
        t_anterior, anio_anterior = ejercicio.get_trimestre_anterior()
        
        fecha_t_actual_inicio, fecha_t_actual_fin = ejercicio.get_fechas_trimestre(t_actual)
        fecha_t_anterior_inicio, fecha_t_anterior_fin = ejercicio.get_fechas_trimestre(t_anterior, anio_anterior)
        
        ejercicio_consolidado = ejercicio.ejercicio_consolidado
        
        def get_saldo_cuenta(cuenta, fecha_inicio, fecha_fin):
            agg = LineaAsiento.objects.filter(
                asiento__fecha__gte=fecha_inicio,
                asiento__fecha__lte=fecha_fin,
                cuenta=cuenta
            ).aggregate(debe=Sum('debe'), haber=Sum('haber'))
            
            debe = agg['debe'] or 0
            haber = agg['haber'] or 0
            saldo = haber - debe
            
            for hijo in cuenta.hijos.all():
                saldo += get_saldo_cuenta(hijo, fecha_inicio, fecha_fin)
            
            return saldo
        
        for cuenta in cuentas_ingreso:
            saldo_t_actual = get_saldo_cuenta(cuenta, fecha_t_actual_inicio, fecha_t_actual_fin)
            saldo_t_anterior = get_saldo_cuenta(cuenta, fecha_t_anterior_inicio, fecha_t_anterior_fin)
            
            if ejercicio_consolidado:
                saldo_consolidado = get_saldo_cuenta(cuenta, ejercicio_consolidado.fecha_inicio, ejercicio_consolidado.fecha_fin)
            else:
                saldo_consolidado = 0
            
            nivel = cuenta.codigo.count('.')
            
            datos.append({
                'cuenta': cuenta,
                'seccion': 'ingreso',
                'nivel': nivel,
                't_actual': saldo_t_actual,
                't_anterior': saldo_t_anterior,
                'consolidado': saldo_consolidado,
            })
            
            if nivel == 0:
                totales['ingreso_t_actual'] += saldo_t_actual
                totales['ingreso_t_anterior'] += saldo_t_anterior
                totales['ingreso_consolidado'] += saldo_consolidado
        
        for cuenta in cuentas_egreso:
            saldo_t_actual = get_saldo_cuenta(cuenta, fecha_t_actual_inicio, fecha_t_actual_fin)
            saldo_t_anterior = get_saldo_cuenta(cuenta, fecha_t_anterior_inicio, fecha_t_anterior_fin)
            
            if ejercicio_consolidado:
                saldo_consolidado = get_saldo_cuenta(cuenta, ejercicio_consolidado.fecha_inicio, ejercicio_consolidado.fecha_fin)
            else:
                saldo_consolidado = 0
            
            nivel = cuenta.codigo.count('.')
            
            datos.append({
                'cuenta': cuenta,
                'seccion': 'egreso',
                'nivel': nivel,
                't_actual': saldo_t_actual,
                't_anterior': saldo_t_anterior,
                'consolidado': saldo_consolidado,
            })
            
            if nivel == 0:
                totales['egreso_t_actual'] += saldo_t_actual
                totales['egreso_t_anterior'] += saldo_t_anterior
                totales['egreso_consolidado'] += saldo_consolidado
        
        totales['resultado_t_actual'] = totales['ingreso_t_actual'] - totales['egreso_t_actual']
        totales['resultado_t_anterior'] = totales['ingreso_t_anterior'] - totales['egreso_t_anterior']
        totales['resultado_consolidado'] = totales['ingreso_consolidado'] - totales['egreso_consolidado']
    
    ejercicios = Ejercicio.objects.all()
    
    ejercicio_display = ejercicio
    if ejercicio:
        t_actual = ejercicio.get_trimestre_actual() or 1
        t_anterior, anio_anterior = ejercicio.get_trimestre_anterior()
        ejercicio_display = {
            'ejercicio': ejercicio,
            't_actual': t_actual,
            't_anterior': t_anterior,
            'anio_anterior': anio_anterior,
            'ejercicio_consolidado': ejercicio.ejercicio_consolidado,
        }
    
    return render(request, 'contabilidad/estado_resultados.html', {
        'datos': datos,
        'totales': totales,
        'ejercicio': ejercicio,
        'ejercicio_display': ejercicio_display,
        'ejercicios': ejercicios,
    })


def balance_sumas_saldos(request):
    return balance(request)


@login_required
def asiento_create(request):
    ejercicio = Ejercicio.objects.filter(estado='abierto').first()
    cuentas = CuentaContable.objects.filter(activa=True, acepta_movimientos=True)
    
    if request.method == 'POST':
        form = AsientoForm(request.POST)
        
        cuenta_ids = request.POST.getlist('cuenta_id')
        debe_vals = request.POST.getlist('debe')
        haber_vals = request.POST.getlist('haber')
        descripcion_vals = request.POST.getlist('linea_descripcion')
        
        lineas_data = []
        for i, cuenta_id in enumerate(cuenta_ids):
            if cuenta_id:
                debe = debe_vals[i] if i < len(debe_vals) else '0'
                haber = haber_vals[i] if i < len(haber_vals) else '0'
                desc = descripcion_vals[i] if i < len(descripcion_vals) else ''
                lineas_data.append({
                    'cuenta_id': int(cuenta_id),
                    'debe': Decimal(debe.replace(',', '.')) if debe else Decimal('0'),
                    'haber': Decimal(haber.replace(',', '.')) if haber else Decimal('0'),
                    'descripcion': desc
                })
        
        if form.is_valid():
            asiento = form.save(commit=False)
            if not asiento.numero:
                ultimo = Asiento.objects.filter(ejercicio=asiento.ejercicio).order_by('-numero').first()
                if ultimo:
                    try:
                        ultimo_num = int(ultimo.numero)
                        asiento.numero = str(ultimo_num + 1).zfill(4)
                    except:
                        asiento.numero = str(Asiento.objects.count() + 1).zfill(4)
                else:
                    asiento.numero = '0001'
            asiento.estado = 'confirmado'
            asiento.save()
            
            total_debe = Decimal('0')
            total_haber = Decimal('0')
            for ld in lineas_data:
                cuenta = CuentaContable.objects.get(pk=ld['cuenta_id'])
                LineaAsiento.objects.create(
                    asiento=asiento,
                    cuenta=cuenta,
                    debe=ld['debe'],
                    haber=ld['haber'],
                    descripcion=ld['descripcion']
                )
                total_debe += ld['debe']
                total_haber += ld['haber']
            
            if total_debe != total_haber:
                messages.error(request, f'Asiento desbalanceado: Debe={total_debe}, Haber={total_haber}')
                return redirect('contabilidad:asiento_edit', pk=asiento.pk)
            
            messages.success(request, 'Asiento creado correctamente')
            return redirect('contabilidad:asiento_detail', pk=asiento.pk)
    else:
        initial = {}
        if ejercicio:
            initial['ejercicio'] = ejercicio
            initial['fecha'] = ejercicio.fecha_inicio
        form = AsientoForm(initial=initial)
    
    return render(request, 'contabilidad/asiento_form.html', {
        'form': form,
        'cuentas': cuentas,
        'action': 'Crear',
        'asiento': None,
        'lineas_data': [{'cuenta_id': '', 'debe': '', 'haber': '', 'descripcion': ''}]
    })


@login_required
def asiento_edit(request, pk):
    asiento = get_object_or_404(Asiento, pk=pk)
    cuentas = CuentaContable.objects.filter(activa=True, acepta_movimientos=True)
    
    if request.method == 'POST':
        form = AsientoForm(request.POST, instance=asiento)
        
        cuenta_ids = request.POST.getlist('cuenta_id')
        debe_vals = request.POST.getlist('debe')
        haber_vals = request.POST.getlist('haber')
        descripcion_vals = request.POST.getlist('linea_descripcion')
        linea_pks = request.POST.getlist('linea_pk')
        
        if form.is_valid():
            form.save()
            
            asiento.lineas.all().delete()
            
            total_debe = Decimal('0')
            total_haber = Decimal('0')
            for i, cuenta_id in enumerate(cuenta_ids):
                if cuenta_id:
                    debe = debe_vals[i] if i < len(debe_vals) else '0'
                    haber = haber_vals[i] if i < len(haber_vals) else '0'
                    desc = descripcion_vals[i] if i < len(descripcion_vals) else ''
                    cuenta = CuentaContable.objects.get(pk=cuenta_id)
                    LineaAsiento.objects.create(
                        asiento=asiento,
                        cuenta=cuenta,
                        debe=Decimal(debe.replace(',', '.')) if debe else Decimal('0'),
                        haber=Decimal(haber.replace(',', '.')) if haber else Decimal('0'),
                        descripcion=desc
                    )
                    total_debe += Decimal(debe.replace(',', '.')) if debe else Decimal('0')
                    total_haber += Decimal(haber.replace(',', '.')) if haber else Decimal('0')
            
            if total_debe != total_haber:
                messages.error(request, f'Asiento desbalanceado: Debe={total_debe}, Haber={total_haber}')
            else:
                messages.success(request, 'Asiento actualizado correctamente')
            
            return redirect('contabilidad:asiento_detail', pk=asiento.pk)
    else:
        form = AsientoForm(instance=asiento)
    
    lineas_data = [{'pk': l.pk, 'cuenta_id': l.cuenta_id, 'debe': str(l.debe), 'haber': str(l.haber), 'descripcion': l.descripcion} for l in asiento.lineas.all()]
    if not lineas_data:
        lineas_data = [{'cuenta_id': '', 'debe': '', 'haber': '', 'descripcion': ''}]
    
    return render(request, 'contabilidad/asiento_form.html', {
        'form': form,
        'cuentas': cuentas,
        'asiento': asiento,
        'action': 'Editar',
        'lineas_data': lineas_data
    })


@login_required
def asiento_delete(request, pk):
    asiento = get_object_or_404(Asiento, pk=pk)
    if request.method == 'POST':
        asiento.delete()
        messages.success(request, 'Asiento eliminado correctamente')
        return redirect('contabilidad:asientos')
    return render(request, 'contabilidad/asiento_confirm_delete.html', {'asiento': asiento})


@login_required
def asiento_agregar_linea(request, pk):
    from django.http import JsonResponse
    
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        asiento = get_object_or_404(Asiento, pk=pk)
        cuenta = get_object_or_404(CuentaContable, pk=data.get('cuenta_id'))
        
        linea = LineaAsiento.objects.create(
            asiento=asiento,
            cuenta=cuenta,
            debe=data.get('debe', 0),
            haber=data.get('haber', 0),
            descripcion=data.get('descripcion', '')
        )
        
        return JsonResponse({'success': True, 'linea_id': linea.pk})
    
    return JsonResponse({'success': False})


@login_required
def asiento_eliminar_linea(request, pk, linea_id):
    from django.http import JsonResponse
    
    linea = get_object_or_404(LineaAsiento, pk=linea_id, asiento_id=pk)
    linea.delete()
    
    return JsonResponse({'success': True})


@login_required
def cuentas_bulk_delete(request):
    if request.method == 'POST':
        cuentas_ids = request.POST.getlist('cuentas')
        action = request.POST.get('action')
        
        if action == 'delete' and cuentas_ids:
            cuentas = CuentaContable.objects.filter(pk__in=cuentas_ids)
            eliminadas = 0
            errores = []
            for cuenta in cuentas:
                if cuenta.lineas.exists():
                    errores.append(f"{cuenta.codigo}: tiene movimientos")
                else:
                    cuenta.delete()
                    eliminadas += 1
            
            if errores:
                messages.warning(request, f"Eliminadas: {eliminadas}. Errores: {', '.join(errores)}")
            else:
                messages.success(request, f"{eliminadas} cuentas eliminadas")
        
        elif action == 'activate' and cuentas_ids:
            CuentaContable.objects.filter(pk__in=cuentas_ids).update(activa=True)
            messages.success(request, f"{len(cuentas_ids)} cuentas activadas")
        
        elif action == 'deactivate' and cuentas_ids:
            CuentaContable.objects.filter(pk__in=cuentas_ids).update(activa=False)
            messages.success(request, f"{len(cuentas_ids)} cuentas desactivadas")
    
    return redirect('contabilidad:plan_cuentas')


@login_required
def cuenta_toggle_active(request, pk):
    if request.headers.get('HX-Request'):
        cuenta = get_object_or_404(CuentaContable, pk=pk)
        cuenta.activa = not cuenta.activa
        cuenta.save()
        return JsonResponse({'activa': cuenta.activa})
    return redirect('contabilidad:plan_cuentas')


@login_required
def importar_cuentas(request):
    if request.method == 'POST' and request.FILES.get('archivo_csv'):
        import json
        
        archivo = request.FILES['archivo_csv']
        contenido = archivo.read().decode('utf-8')
        
        lector = csv.DictReader(io.StringIO(contenido))
        columnas = lector.fieldnames or []
        
        if request.headers.get('HX-Request') and not request.headers.get('HX-Mapping'):
            return JsonResponse({
                'columnas': columnas,
                'campos': ['codigo', 'nombre', 'tipo', 'cuenta_padre', 'acepta_movimientos'],
            })
        
        mapping_header = request.headers.get('HX-Mapping')
        if mapping_header:
            try:
                mapping = json.loads(mapping_header)
            except:
                mapping = {}
        else:
            mapping = {
                'codigo': 'codigo',
                'nombre': 'nombre',
                'tipo': 'tipo',
                'cuenta_padre': 'cuenta_padre',
                'acepta_movimientos': 'acepta_movimientos',
            }
        
        cuentas_nuevas = []
        errores = []
        
        for num_fila, fila in enumerate(lector, start=2):
            try:
                codigo = fila.get(mapping.get('codigo', 'codigo'), '').strip()
                nombre = fila.get(mapping.get('nombre', 'nombre'), '').strip()
                tipo = fila.get(mapping.get('tipo', 'tipo'), '').strip().lower()
                acepta_mov_str = fila.get(mapping.get('acepta_movimientos', 'acepta_movimientos'), '1').strip()
                acepta_movimientos = acepta_mov_str in ['1', 'True', 'true', 'YES', 'yes', 'S', 's']
                
                if not codigo or not nombre:
                    errores.append(f"Fila {num_fila}: Código y nombre son obligatorios")
                    continue
                
                if tipo not in ['activo', 'pasivo', 'patrimonio', 'ingreso', 'egreso']:
                    errores.append(f"Fila {num_fila}: Tipo '{tipo}' inválido")
                    continue
                
                cuenta_existente = CuentaContable.objects.filter(codigo=codigo).first()
                
                if cuenta_existente:
                    errores.append(f"Fila {num_fila}: Ya existe cuenta con código {codigo}")
                    continue
                
                padre = None
                cuenta_padre_codigo = fila.get(mapping.get('cuenta_padre', 'cuenta_padre'), '').strip()
                if cuenta_padre_codigo:
                    padre = CuentaContable.objects.filter(codigo=cuenta_padre_codigo).first()
                else:
                    codigo_parts = codigo.rsplit('.', 1)
                    if len(codigo_parts) > 1:
                        codigo_padre = '.'.join(codigo_parts[:-1])
                        padre = CuentaContable.objects.filter(codigo=codigo_padre).first()
                
                cuentas_nuevas.append({
                    'codigo': codigo,
                    'nombre': nombre,
                    'tipo': tipo,
                    'padre': padre,
                    'acepta_movimientos': acepta_movimientos,
                })
            except Exception as e:
                errores.append(f"Fila {num_fila}: Error - {str(e)}")
        
        if request.headers.get('HX-Request'):
            return JsonResponse({
                'cuentas': cuentas_nuevas,
                'errores': errores,
                'total': len(cuentas_nuevas)
            })
        
        if errores and not cuentas_nuevas:
            for error in errores:
                messages.error(request, error)
            return redirect('contabilidad:plan_cuentas')
        
        if cuentas_nuevas:
            cuentas_creadas = []
            for c in cuentas_nuevas:
                cuenta = CuentaContable.objects.create(
                    codigo=c['codigo'],
                    nombre=c['nombre'],
                    tipo=c['tipo'],
                    padre=c['padre'],
                    acepta_movimientos=c['acepta_movimientos'],
                    activa=True
                )
                cuentas_creadas.append(cuenta)
            
            messages.success(request, f'Se importaron {len(cuentas_creadas)} cuentas correctamente')
            return redirect('contabilidad:plan_cuentas')
    
    return render(request, 'contabilidad/importar_cuentas.html')


@login_required
def importar_cuentas_confirmar(request):
    if request.method == 'POST':
        import json
        datos = json.loads(request.body)
        
        mapping = datos.get('mapping', {})
        archivo_nombre = datos.get('filename', '')
        
        if archivo_nombre:
            from django.core.files.storage import default_storage
            from django.conf import settings
            
            try:
                with default_storage.open(archivo_nombre, 'rb') as f:
                    contenido = f.read().decode('utf-8')
                f = io.StringIO(contenido)
                lector = csv.DictReader(f)
            except Exception:
                return JsonResponse({'success': False, 'errores': ['No se pudo leer el archivo']})
        else:
            return JsonResponse({'success': False, 'errores': ['Archivo no proporcionado']})
        
        cuentas_creadas = []
        errores = []
        cuentas_data = []
        
        for num_fila, fila in enumerate(lector, start=2):
            try:
                codigo = fila.get(mapping.get('codigo', 'codigo'), '').strip()
                nombre = fila.get(mapping.get('nombre', 'nombre'), '').strip()
                tipo = fila.get(mapping.get('tipo', 'tipo'), '').strip().lower()
                acepta_mov_str = fila.get(mapping.get('acepta_movimientos', 'acepta_movimientos'), '1').strip()
                acepta_movimientos = acepta_mov_str in ['1', 'True', 'true', 'YES', 'yes', 'S', 's']
                
                if not codigo or not nombre:
                    errores.append(f"Fila {num_fila}: Código y nombre obligatorios")
                    continue
                
                if tipo not in ['activo', 'pasivo', 'patrimonio', 'ingreso', 'egreso']:
                    errores.append(f"Fila {num_fila}: Tipo '{tipo}' inválido")
                    continue
                
                if CuentaContable.objects.filter(codigo=codigo).exists():
                    errores.append(f"Fila {num_fila}: Ya existe {codigo}")
                    continue
                
                cuenta_padre_codigo = fila.get(mapping.get('cuenta_padre', 'cuenta_padre'), '').strip()
                
                cuentas_data.append({
                    'codigo': codigo,
                    'nombre': nombre,
                    'tipo': tipo,
                    'acepta_movimientos': acepta_movimientos,
                    'cuenta_padre_codigo': cuenta_padre_codigo,
                })
            except Exception as e:
                errores.append(f"Fila {num_fila}: Error - {str(e)}")
        
        if errores and not cuentas_data:
            return JsonResponse({'success': False, 'errores': errores})
        
        for cd in cuentas_data:
            CuentaContable.objects.create(
                codigo=cd['codigo'],
                nombre=cd['nombre'],
                tipo=cd['tipo'],
                padre=None,
                acepta_movimientos=cd['acepta_movimientos'],
                activa=True
            )
            cuentas_creadas.append(cd['codigo'])
        
        for cd in cuentas_data:
            if cd['cuenta_padre_codigo']:
                padre = CuentaContable.objects.filter(codigo=cd['cuenta_padre_codigo']).first()
            else:
                codigo_parts = cd['codigo'].rsplit('.', 1)
                if len(codigo_parts) > 1:
                    codigo_padre = '.'.join(codigo_parts[:-1])
                    padre = CuentaContable.objects.filter(codigo=codigo_padre).first()
                else:
                    padre = None
            
            if padre:
                cuenta = CuentaContable.objects.get(codigo=cd['codigo'])
                cuenta.padre = padre
                cuenta.save()
        
        return JsonResponse({'success': True, 'total': len(cuentas_creadas)})
    
    return JsonResponse({'success': False})


@login_required
def descargar_guia_csv(request):
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guia_plan_cuentas.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['codigo', 'nombre', 'tipo', 'cuenta_padre', 'acepta_movimientos'])
    writer.writerow(['1', 'Activo', 'activo', '', '1'])
    writer.writerow(['1.1', 'Caja y Bancos', 'activo', '1', '0'])
    writer.writerow(['1.1.01', 'Caja pesos', 'activo', '1.1', '1'])
    writer.writerow(['1.1.02', 'Banco Galicia', 'activo', '1.1', '1'])
    writer.writerow(['1.2', 'Clientes', 'activo', '1', '0'])
    writer.writerow(['1.2.01', 'Clientes locales', 'activo', '1.2', '1'])
    writer.writerow(['2', 'Pasivo', 'pasivo', '', '1'])
    writer.writerow(['2.1', 'Proveedores', 'pasivo', '2', '0'])
    writer.writerow(['2.1.01', 'Proveedores locales', 'pasivo', '2.1', '1'])
    writer.writerow(['3', 'Patrimonio Neto', 'patrimonio', '', '1'])
    writer.writerow(['3.1', 'Capital', 'patrimonio', '3', '1'])
    writer.writerow(['4', 'Ingresos', 'ingreso', '', '1'])
    writer.writerow(['4.1', 'Venta de mercadería', 'ingreso', '4', '1'])
    writer.writerow(['5', 'Egresos', 'egreso', '', '1'])
    writer.writerow(['5.1', 'Costo de mercadería', 'egreso', '5', '1'])
    
    return response


@login_required
def preview_cierre(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    
    if ejercicio.estado != 'abierto':
        messages.error(request, 'El ejercicio ya está cerrado')
        return redirect('contabilidad:dashboard')
    
    cuentas_ingreso = CuentaContable.objects.filter(activa=True, tipo='ingreso').order_by('codigo')
    cuentas_egreso = CuentaContable.objects.filter(activa=True, tipo='egreso').order_by('codigo')
    
    total_ingresos = Decimal('0')
    total_egresos = Decimal('0')
    
    lineas_preview = []
    
    def get_saldo(cuenta, ejercicio):
        from django.db.models import Sum
        agg = LineaAsiento.objects.filter(
            asiento__ejercicio=ejercicio,
            cuenta=cuenta
        ).aggregate(debe=Sum('debe'), haber=Sum('haber'))
        debe = agg['debe'] or 0
        haber = agg['haber'] or 0
        return haber - debe
    
    for cuenta in cuentas_ingreso:
        saldo = get_saldo(cuenta, ejercicio)
        if saldo > 0:
            lineas_preview.append({
                'cuenta': cuenta,
                'debe': saldo,
                'haber': 0,
                'tipo': 'cierre_ingreso'
            })
            total_ingresos += saldo
    
    for cuenta in cuentas_egreso:
        saldo = get_saldo(cuenta, ejercicio)
        if saldo > 0:
            lineas_preview.append({
                'cuenta': cuenta,
                'debe': saldo,
                'haber': 0,
                'tipo': 'cierre_egreso'
            })
            total_egresos += saldo
    
    resultado = total_ingresos - total_egresos
    
    cuenta_resultados = CuentaContable.objects.filter(
        Q(codigo='3.3.02') | Q(nombre__icontains='Resultados acumulados')
    ).first()
    
    if not cuenta_resultados:
        messages.error(request, 'No se encontró la cuenta de Resultados Acumulados (3.3.02)')
        return redirect('contabilidad:dashboard')
    
    if resultado > 0:
        lineas_preview.append({
            'cuenta': cuenta_resultados,
            'debe': 0,
            'haber': resultado,
            'tipo': 'resultado'
        })
    elif resultado < 0:
        lineas_preview.append({
            'cuenta': cuenta_resultados,
            'debe': abs(resultado),
            'haber': 0,
            'tipo': 'resultado'
        })
    
    return render(request, 'contabilidad/cierre_preview.html', {
        'ejercicio': ejercicio,
        'lineas': lineas_preview,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'resultado': resultado,
    })


@login_required
def cerrar_ejercicio(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    
    if ejercicio.estado != 'abierto':
        messages.error(request, 'El ejercicio ya está cerrado')
        return redirect('contabilidad:dashboard')
    
    if request.method != 'POST':
        return redirect('contabilidad:preview_cierre', pk=pk)
    
    cuentas_ingreso = CuentaContable.objects.filter(activa=True, tipo='ingreso').order_by('codigo')
    cuentas_egreso = CuentaContable.objects.filter(activa=True, tipo='egreso').order_by('codigo')
    
    cuenta_resultados = CuentaContable.objects.filter(
        Q(codigo='3.3.02') | Q(nombre__icontains='Resultados acumulados')
    ).first()
    
    if not cuenta_resultados:
        messages.error(request, 'No se encontró la cuenta de Resultados Acumulados')
        return redirect('contabilidad:dashboard')
    
    total_ingresos = Decimal('0')
    total_egresos = Decimal('0')
    
    def get_saldo(cuenta, ejercicio):
        from django.db.models import Sum
        agg = LineaAsiento.objects.filter(
            asiento__ejercicio=ejercicio,
            cuenta=cuenta
        ).aggregate(debe=Sum('debe'), haber=Sum('haber'))
        debe = agg['debe'] or 0
        haber = agg['haber'] or 0
        return haber - debe
    
    ultimo_asiento = Asiento.objects.order_by('-numero').first()
    if ultimo_asiento:
        try:
            numero = int(ultimo_asiento.numero) + 1
        except ValueError:
            numero = 1
    else:
        numero = 1
    
    asiento_cierre = Asiento.objects.create(
        ejercicio=ejercicio,
        numero=str(numero).zfill(4),
        fecha=ejercicio.fecha_fin,
        descripcion=f'Asiento de cierre - Ejercicio {ejercicio.nombre}',
        origen='cierre',
        estado='confirmado'
    )
    
    for cuenta in cuentas_ingreso:
        saldo = get_saldo(cuenta, ejercicio)
        if saldo > 0:
            LineaAsiento.objects.create(
                asiento=asiento_cierre,
                cuenta=cuenta,
                debe=saldo,
                haber=0,
                descripcion=f'Cierre cuenta {cuenta.codigo}'
            )
            total_ingresos += saldo
    
    for cuenta in cuentas_egreso:
        saldo = get_saldo(cuenta, ejercicio)
        if saldo > 0:
            LineaAsiento.objects.create(
                asiento=asiento_cierre,
                cuenta=cuenta,
                debe=saldo,
                haber=0,
                descripcion=f'Cierre cuenta {cuenta.codigo}'
            )
            total_egresos += saldo
    
    resultado = total_ingresos - total_egresos
    
    if resultado > 0:
        LineaAsiento.objects.create(
            asiento=asiento_cierre,
            cuenta=cuenta_resultados,
            debe=0,
            haber=resultado,
            descripcion=f'Ganancia del ejercicio'
        )
    elif resultado < 0:
        LineaAsiento.objects.create(
            asiento=asiento_cierre,
            cuenta=cuenta_resultados,
            debe=abs(resultado),
            haber=0,
            descripcion=f'Pérdida del ejercicio'
        )
    
    ejercicio.estado = 'cerrado'
    ejercicio.save()
    
    messages.success(request, f'Ejercicio {ejercicio.nombre} cerrado correctamente. Asiento de cierre: {asiento_cierre.numero}')
    return redirect('contabilidad:dashboard')


@login_required
def generar_apertura(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    
    if ejercicio.estado != 'abierto':
        messages.error(request, 'El ejercicio debe estar abierto')
        return redirect('contabilidad:dashboard')
    
    if not ejercicio.ejercicio_anterior:
        messages.error(request, 'El ejercicio no tiene un ejercicio anterior configurado')
        return redirect('contabilidad:dashboard')
    
    ejercicio_anterior = ejercicio.ejercicio_anterior
    
    cuentas_activo = CuentaContable.objects.filter(activa=True, tipo='activo').order_by('codigo')
    cuentas_pasivo = CuentaContable.objects.filter(activa=True, tipo='pasivo').order_by('codigo')
    
    def get_saldo(cuenta, ejercicio):
        from django.db.models import Sum
        agg = LineaAsiento.objects.filter(
            asiento__ejercicio=ejercicio,
            cuenta=cuenta
        ).aggregate(debe=Sum('debe'), haber=Sum('haber'))
        debe = agg['debe'] or 0
        haber = agg['haber'] or 0
        return debe - haber
    
    lineas_preview = []
    
    for cuenta in cuentas_activo:
        saldo = get_saldo(cuenta, ejercicio_anterior)
        if saldo != 0:
            lineas_preview.append({
                'cuenta': cuenta,
                'debe': saldo if saldo > 0 else 0,
                'haber': abs(saldo) if saldo < 0 else 0
            })
    
    for cuenta in cuentas_pasivo:
        saldo = get_saldo(cuenta, ejercicio_anterior)
        if saldo != 0:
            lineas_preview.append({
                'cuenta': cuenta,
                'debe': abs(saldo) if saldo < 0 else 0,
                'haber': saldo if saldo > 0 else 0
            })
    
    if request.method == 'POST':
        ultimo_asiento = Asiento.objects.order_by('-numero').first()
        if ultimo_asiento:
            try:
                numero = int(ultimo_asiento.numero) + 1
            except ValueError:
                numero = 1
        else:
            numero = 1
        
        apertura = Asiento.objects.create(
            ejercicio=ejercicio,
            numero=str(numero).zfill(4),
            fecha=ejercicio.fecha_inicio,
            descripcion=f'Asiento de apertura - Ejercicio {ejercicio.nombre}',
            origen='apertura',
            estado='confirmado'
        )
        
        for linea in lineas_preview:
            LineaAsiento.objects.create(
                asiento=apertura,
                cuenta=linea['cuenta'],
                debe=linea['debe'],
                haber=linea['haber'],
                descripcion=f'Apertura desde ejercicio anterior'
            )
        
        messages.success(request, f'Asiento de apertura generado: {apertura.numero}')
        return redirect('contabilidad:dashboard')
    
    return render(request, 'contabilidad/apertura.html', {
        'ejercicio': ejercicio,
        'ejercicio_anterior': ejercicio_anterior,
        'lineas': lineas_preview,
    })
