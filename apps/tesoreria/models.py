from decimal import Decimal
from django.db import models
from apps.base.models import TimeStampedModel, DocumentoBase


class CuentaTesoreria(TimeStampedModel):
    TIPO_CHOICES = [
        ('caja', 'Caja'),
        ('banco', 'Banco'),
        ('digital', 'Billetera digital'),
    ]

    MONEDA_CHOICES = [
        ('ARS', 'Peso Argentino'),
        ('USD', 'Dólar estadounidense'),
        ('EUR', 'Euro'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    cuenta_contable = models.ForeignKey(
        'contabilidad.CuentaContable',
        on_delete=models.PROTECT,
        related_name='cuentas_tesoreria',
        verbose_name='Cuenta contable'
    )
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default='ARS', verbose_name='Moneda')
    saldo_inicial = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name='Saldo inicial')
    activa = models.BooleanField(default=True, verbose_name='Activa')

    class Meta:
        ordering = ['tipo', 'nombre']
        verbose_name = 'Cuenta de tesorería'
        verbose_name_plural = 'Cuentas de tesorería'

    def __str__(self):
        return f"{self.nombre} ({self.moneda})"

    @property
    def saldo_actual(self):
        ingresos = sum(m.importe for m in self.movimientos.filter(tipo='cobro'))
        egresos = sum(m.importe for m in self.movimientos.filter(tipo='pago'))
        return self.saldo_inicial + ingresos - egresos


class MovimientoTesoreria(DocumentoBase):
    TIPO_CHOICES = [
        ('cobro', 'Cobro'),
        ('pago', 'Pago'),
        ('transferencia', 'Transferencia'),
    ]

    cuenta = models.ForeignKey(
        CuentaTesoreria,
        on_delete=models.CASCADE,
        related_name='movimientos',
        verbose_name='Cuenta'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    importe = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Importe')
    contacto = models.ForeignKey(
        'contactos.Contacto',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='movimientos_tesoreria',
        verbose_name='Contacto'
    )
    origen_tipo = models.CharField(max_length=50, blank=True, verbose_name='Tipo de origen')
    origen_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='ID de origen')
    descripcion = models.CharField(max_length=200, blank=True, verbose_name='Descripción')

    class Meta:
        ordering = ['-fecha', '-numero']
        verbose_name = 'Movimiento de tesorería'
        verbose_name_plural = 'Movimientos de tesorería'

    def __str__(self):
        return f"{self.numero} - {self.get_tipo_display()} - {self.importe}"

    @property
    def saldo_cuenta(self):
        return self.cuenta.saldo_actual
