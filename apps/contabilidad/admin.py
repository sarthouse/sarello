from django.contrib import admin
from .models import CuentaContable, Ejercicio, Asiento, LineaAsiento, MapeoContable, TipoImpuesto, Alicuota, ConfiguracionImpuesto


@admin.register(CuentaContable)
class CuentaContableAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo', 'activa', 'acepta_movimientos')
    list_filter = ('tipo', 'activa', 'acepta_movimientos')
    search_fields = ('codigo', 'nombre')


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado',)


@admin.register(Asiento)
class AsientoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'fecha', 'ejercicio', 'origen', 'estado')
    list_filter = ('estado', 'origen', 'ejercicio')
    search_fields = ('numero', 'descripcion')


@admin.register(LineaAsiento)
class LineaAsientoAdmin(admin.ModelAdmin):
    list_display = ('asiento', 'cuenta', 'debe', 'haber')
    list_filter = ('cuenta__tipo',)


@admin.register(MapeoContable)
class MapeoContableAdmin(admin.ModelAdmin):
    list_display = ('evento', 'cuenta_debe', 'cuenta_haber', 'activo')
    list_filter = ('activo',)


@admin.register(TipoImpuesto)
class TipoImpuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'tipo', 'activo')
    list_filter = ('tipo', 'activo')


@admin.register(Alicuota)
class AlicuotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_impuesto', 'porcentaje', 'jurisdiccion', 'por_defecto')
    list_filter = ('tipo_impuesto', 'por_defecto')


@admin.register(ConfiguracionImpuesto)
class ConfiguracionImpuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_impuesto', 'jurisdiccion', 'aplica_compras', 'aplica_ventas')
    list_filter = ('jurisdiccion', 'aplica_compras', 'aplica_ventas')
