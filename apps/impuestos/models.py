from decimal import Decimal
from django.db import models
from apps.base.models import TimeStampedModel


class TipoImpuesto(TimeStampedModel):
    TIPO_CHOICES = [
        ('iva', 'IVA'),
        ('iibb', 'IIBB'),
        ('retencion', 'Retención'),
        ('percepcion', 'Percepción'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    cuenta_contable = models.ForeignKey(
        'contabilidad.CuentaContable',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='tipos_impuesto',
        verbose_name='Cuenta contable'
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Tipo de impuesto'
        verbose_name_plural = 'Tipos de impuesto'

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Alicuota(TimeStampedModel):
    tipo_impuesto = models.ForeignKey(
        TipoImpuesto,
        on_delete=models.CASCADE,
        related_name='alicuotas',
        verbose_name='Tipo de impuesto'
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Porcentaje')
    jurisdiccion = models.CharField(
        max_length=100, 
        blank=True, 
        default='Nacional',
        verbose_name='Jurisdicción'
    )
    fecha_desde = models.DateField(verbose_name='Vigente desde')
    fecha_hasta = models.DateField(null=True, blank=True, verbose_name='Vigente hasta')
    por_defecto = models.BooleanField(default=False, verbose_name='Por defecto')

    class Meta:
        ordering = ['-fecha_desde']
        verbose_name = 'Alícuota'
        verbose_name_plural = 'Alícuotas'

    def __str__(self):
        return f"{self.tipo_impuesto.nombre} - {self.nombre} ({self.porcentaje}%)"

    def esta_vigente(self):
        from django.utils import timezone
        hoy = timezone.now().date()
        return self.fecha_desde <= hoy and (self.fecha_hasta is None or self.fecha_hasta >= hoy)


class ConfiguracionImpuesto(TimeStampedModel):
    JURISDICCION_CHOICES = [
        ('nacional', 'Nacional'),
        ('provincial', 'Provincial'),
        ('municipal', 'Municipal'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    tipo_impuesto = models.ForeignKey(
        TipoImpuesto,
        on_delete=models.CASCADE,
        related_name='configuraciones',
        verbose_name='Tipo de impuesto'
    )
    jurisdiccion = models.CharField(max_length=20, choices=JURISDICCION_CHOICES, default='nacional', verbose_name='Jurisdicción')
    provincia = models.CharField(max_length=100, blank=True, verbose_name='Provincia')
    municipio = models.CharField(max_length=100, blank=True, verbose_name='Municipio')
    alicuota_por_defecto = models.ForeignKey(
        Alicuota,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Alícuota por defecto'
    )
    aplica_compras = models.BooleanField(default=True, verbose_name='Aplica a compras')
    aplica_ventas = models.BooleanField(default=True, verbose_name='Aplica a ventas')
    requiere_constancia = models.BooleanField(default=False, verbose_name='Requiere constancia')
    cuenta_contable_debe = models.ForeignKey(
        'contabilidad.CuentaContable',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Cuenta debe'
    )
    cuenta_contable_haber = models.ForeignKey(
        'contabilidad.CuentaContable',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Cuenta haber'
    )

    class Meta:
        verbose_name = 'Configuración de impuesto'
        verbose_name_plural = 'Configuraciones de impuesto'

    def __str__(self):
        return f"{self.nombre} - {self.get_jurisdiccion_display()}"
