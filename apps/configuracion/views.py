from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ParametroSistema, DatosEmpresa
from .forms import ParametroForm, DatosEmpresaForm


@login_required
def index(request):
    return render(request, 'configuracion/index.html')


@login_required
def parametros(request):
    parametros = ParametroSistema.objects.all().order_by('grupo', 'clave')
    return render(request, 'configuracion/parametros.html', {'parametros': parametros})


@login_required
def parametro_edit(request, pk):
    parametro = get_object_or_404(ParametroSistema, pk=pk)
    if not parametro.editable:
        messages.error(request, 'Este parámetro no es editable')
        return redirect('configuracion:parametros')

    if request.method == 'POST':
        form = ParametroForm(request.POST, instance=parametro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Parámetro actualizado')
            return redirect('configuracion:parametros')
    else:
        form = ParametroForm(instance=parametro)
    return render(request, 'configuracion/parametro_form.html', {'form': form, 'parametro': parametro})


@login_required
def datos_empresa(request):
    datos = DatosEmpresa.objects.first()
    if request.method == 'POST':
        form = DatosEmpresaForm(request.POST, request.FILES, instance=datos)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos de la empresa actualizados')
            return redirect('configuracion:datos_empresa')
    else:
        form = DatosEmpresaForm(instance=datos)
    return render(request, 'configuracion/datos_empresa.html', {'form': form})
