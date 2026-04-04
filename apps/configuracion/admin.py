from django.contrib import admin
from .models import ParametroSistema, DatosEmpresa


@admin.register(ParametroSistema)
class ParametroSistemaAdmin(admin.ModelAdmin):
    list_display = ('clave', 'valor', 'grupo', 'editable')
    list_filter = ('grupo', 'editable')
    search_fields = ('clave', 'descripcion')


@admin.register(DatosEmpresa)
class DatosEmpresaAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'cuil', 'condicion_iva')
