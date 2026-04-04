from django.contrib import admin
from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'codigo', 'cuil', 'condicion_iva', 'activo')
    list_filter = ('tipo', 'condicion_iva', 'activo')
    search_fields = ('nombre', 'codigo', 'cuil')
