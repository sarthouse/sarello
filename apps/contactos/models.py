from django.db import models
from apps.base.models import TimeStampedModel


class Contacto(TimeStampedModel):
    TIPO_CHOICES = [
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
        ('cliente_proveedor', 'Cliente y Proveedor'),
    ]

    CONDICION_IVA_CHOICES = [
        ('responsable_inscripto', 'Responsable Inscripto'),
        ('monotributista', 'Monotributista'),
        ('exento', 'Exento'),
        ('consumidor_final', 'Consumidor Final'),
        ('no_responsable', 'No Responsable'),
    ]

    nombre = models.CharField(max_length=200, verbose_name='Nombre o razón social')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='cliente', verbose_name='Tipo')
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    cuil = models.CharField(max_length=13, blank=True, verbose_name='CUIL/CUIT')
    condicion_iva = models.CharField(max_length=30, choices=CONDICION_IVA_CHOICES, default='consumidor_final', verbose_name='Condición IVA')
    direccion = models.CharField(max_length=300, blank=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=50, blank=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Email')
    ciudad = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    provincia = models.CharField(max_length=100, blank=True, verbose_name='Provincia')
    codigo_postal = models.CharField(max_length=20, blank=True, verbose_name='Código postal')
    contacto_principal = models.CharField(max_length=200, blank=True, verbose_name='Contacto principal')
    notas = models.TextField(blank=True, verbose_name='Notas')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    limite_credito = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Límite de crédito')

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
