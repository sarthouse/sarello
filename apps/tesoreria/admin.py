from django.contrib import admin
from .models import CuentaTesoreria, MovimientoTesoreria, LineaMovimientoTesoreria


@admin.register(CuentaTesoreria)
class CuentaTesoreriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'moneda', 'saldo_inicial', 'activa')
    list_filter = ('tipo', 'moneda', 'activa')
    search_fields = ('nombre',)


class LineaMovimientoTesoreriaInline(admin.TabularInline):
    model = LineaMovimientoTesoreria
    extra = 1


@admin.register(MovimientoTesoreria)
class MovimientoTesoreriaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'fecha', 'tipo', 'contacto', 'estado', 'importe_total')
    list_filter = ('tipo', 'estado')
    search_fields = ('numero', 'descripcion')
    inlines = [LineaMovimientoTesoreriaInline]


@admin.register(LineaMovimientoTesoreria)
class LineaMovimientoTesoreriaAdmin(admin.ModelAdmin):
    list_display = ('movimiento', 'cuenta', 'debe', 'haber')
    list_filter = ('cuenta__tipo',)
