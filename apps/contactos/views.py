from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django import forms
from .models import Contacto


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'tipo', 'codigo', 'cuil', 'condicion_iva', 'direccion', 'telefono', 'email', 'ciudad', 'provincia', 'codigo_postal', 'contacto_principal', 'notas', 'activo', 'limite_credito']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'tipo': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'codigo': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'cuil': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'condicion_iva': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'direccion': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'ciudad': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'provincia': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'contacto_principal': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'notas': forms.Textarea(attrs={'class': 'w-full border rounded px-3 py-2', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'rounded'}),
            'limite_credito': forms.NumberInput(attrs={'class': 'w-full border rounded px-3 py-2', 'step': '0.01'}),
        }


@login_required
def index(request):
    return render(request, 'contactos/index.html')


@login_required
def lista(request):
    tipo_filter = request.GET.get('tipo')
    estado_filter = request.GET.get('estado')
    busqueda = request.GET.get('q')
    
    contactos = Contacto.objects.all().order_by('nombre')
    
    if tipo_filter:
        contactos = contactos.filter(tipo=tipo_filter)
    
    if estado_filter == 'activo':
        contactos = contactos.filter(activo=True)
    elif estado_filter == 'inactivo':
        contactos = contactos.filter(activo=False)
    
    if busqueda:
        contactos = contactos.filter(
            models.Q(nombre__icontains=busqueda) | 
            models.Q(codigo__icontains=busqueda) |
            models.Q(cuil__icontains=busqueda)
        )
    
    paginator = Paginator(contactos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'contactos/lista.html', {
        'page_obj': page_obj,
        'tipo_filter': tipo_filter,
        'estado_filter': estado_filter,
        'busqueda': busqueda,
    })


@login_required
def contacto_create(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contacto creado correctamente')
            return redirect('contactos:lista')
    else:
        form = ContactoForm()
    return render(request, 'contactos/form.html', {'form': form, 'action': 'Crear'})


@login_required
def contacto_edit(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contacto actualizado correctamente')
            return redirect('contactos:lista')
    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'contactos/form.html', {'form': form, 'contacto': contacto, 'action': 'Editar'})


@login_required
def contacto_delete(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        contacto.delete()
        messages.success(request, 'Contacto eliminado correctamente')
        return redirect('contactos:lista')
    return render(request, 'contactos/confirm_delete.html', {'contacto': contacto})


@login_required
def contacto_detail(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    return render(request, 'contactos/detail.html', {'contacto': contacto})
