from decimal import Decimal
from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.base.models import TimeStampedModel, DocumentoBase


class CuentaContable(TimeStampedModel):
    TIPO_CHOICES = [
        ('activo', 'Activo'),
        ('pasivo', 'Pasivo'),
        ('patrimonio', 'Patrimonio Neto'),
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]

    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    padre = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        related_name='hijos', 
        on_delete=models.PROTECT,
        verbose_name='Cuenta padre'
    )
    acepta_movimientos = models.BooleanField(default=True, verbose_name='Acepta movimientos')
    activa = models.BooleanField(default=True, verbose_name='Activa')

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Cuenta contable'
        verbose_name_plural = 'Cuentas contables'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def saldo_actual(self):
        debe = sum(self.movimientos.debe() for _ in [1])
        haber = sum(self.movimientos.haber() for _ in [1])
        return debe - haber if self.tipo in ['activo', 'egreso'] else haber - debe

    @property
    def nivel(self):
        return self.codigo.count('.')

    def es_cuenta_hoja(self):
        return not self.hijos.exists()

    def get_saldo_en_fecha(self, fecha_inicio, fecha_fin):
        from django.db.models import Sum

        agg = LineaAsiento.objects.filter(
            asiento__fecha__gte=fecha_inicio,
            asiento__fecha__lte=fecha_fin,
            cuenta=self
        ).aggregate(debe=Sum('debe'), haber=Sum('haber'))
        
        debe = agg['debe'] or 0
        haber = agg['haber'] or 0
        
        if self.tipo in ['activo', 'egreso']:
            return debe - haber
        else:
            return haber - debe

    def get_saldo_con_hijos(self, fecha_inicio, fecha_fin):
        saldo = self.get_saldo_en_fecha(fecha_inicio, fecha_fin)
        for hijo in self.hijos.all():
            saldo += hijo.get_saldo_con_hijos(fecha_inicio, fecha_fin)
        return saldo

    def get_trimestre_actual(self):
        hoy = date.today()
        mes = hoy.month
        if mes <= 3:
            return 1
        elif mes <= 6:
            return 2
        elif mes <= 9:
            return 3
        else:
            return 4

    def get_fechas_trimestre(self, trimestre, anio=None):
        if anio is None:
            anio = self.fecha_inicio.year
        if trimestre == 1:
            return date(anio, 1, 1), date(anio, 3, 31)
        elif trimestre == 2:
            return date(anio, 4, 1), date(anio, 6, 30)
        elif trimestre == 3:
            return date(anio, 7, 1), date(anio, 9, 30)
        else:
            return date(anio, 10, 1), date(anio, 12, 31)

    def get_trimestre_anterior(self):
        t_actual = self.get_trimestre_actual()
        if t_actual == 1:
            return 4, self.fecha_inicio.year - 1
        return t_actual - 1, self.fecha_inicio.year


class Ejercicio(TimeStampedModel):
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
    ]

    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
    fecha_fin = models.DateField(verbose_name='Fecha de fin')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto', verbose_name='Estado')
    ejercicio_anterior = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        related_name='ejercicios_siguientes',
        on_delete=models.SET_NULL,
        verbose_name='Ejercicio anterior'
    )
    ejercicio_consolidado = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='ejercicios_desconsolidar',
        on_delete=models.SET_NULL,
        verbose_name='Ejercicio consolidado anterior'
    )

    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Ejercicio contable'
        verbose_name_plural = 'Ejercicios contables'

    def __str__(self):
        return f"{self.nombre} ({self.fecha_inicio.year})"

    def esta_abierto(self):
        return self.estado == 'abierto'

    def puede_cerrar(self):
        return self.estado == 'abierto'

    def get_trimestre_actual(self):
        from datetime import date
        hoy = date.today()
        mes = hoy.month
        if self.fecha_inicio <= hoy <= self.fecha_fin:
            if mes <= 3:
                return 1
            elif mes <= 6:
                return 2
            elif mes <= 9:
                return 3
            else:
                return 4
        return None

    def get_fechas_trimestre(self, trimestre, anio=None):
        if anio is None:
            anio = self.fecha_inicio.year
        if trimestre == 1:
            return date(anio, 1, 1), date(anio, 3, 31)
        elif trimestre == 2:
            return date(anio, 4, 1), date(anio, 6, 30)
        elif trimestre == 3:
            return date(anio, 7, 1), date(anio, 9, 30)
        else:
            return date(anio, 10, 1), date(anio, 12, 31)

    def get_trimestre_anterior(self):
        t_actual = self.get_trimestre_actual() or 1
        if t_actual == 1:
            return 4, self.fecha_inicio.year - 1
        return t_actual - 1, self.fecha_inicio.year


class Asiento(DocumentoBase):
    ORIGEN_CHOICES = [
        ('manual', 'Manual'),
        ('venta', 'Venta'),
        ('compra', 'Compra'),
        ('tesoreria', 'Tesorería'),
        ('manufactura', 'Manufactura'),
    ]

    ejercicio = models.ForeignKey(
        Ejercicio, 
        on_delete=models.PROTECT, 
        related_name='asientos',
        verbose_name='Ejercicio'
    )
    descripcion = models.CharField(max_length=200, verbose_name='Descripción')
    origen = models.CharField(max_length=20, choices=ORIGEN_CHOICES, default='manual', verbose_name='Origen')
    origen_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='ID origen')

    class Meta:
        ordering = ['-fecha', '-numero']
        verbose_name = 'Asiento contable'
        verbose_name_plural = 'Asientos contables'

    def __str__(self):
        return f"Asiento {self.numero} - {self.fecha}"

    def total_debe(self):
        return sum(linea.debe for linea in self.lineas.all())

    def total_haber(self):
        return sum(linea.haber for linea in self.lineas.all())

    def balanceado(self):
        return self.total_debe() == self.total_haber()

    def clean(self):
        if self.pk and self.lineas.exists() and not self.balanceado():
            raise ValidationError(f"Asiento desbalanceado: debe={self.total_debe()}, haber={self.total_haber()}")


class LineaAsiento(models.Model):
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE, related_name='lineas', verbose_name='Asiento')
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT, related_name='lineas', verbose_name='Cuenta')
    debe = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name='Debe')
    haber = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name='Haber')
    descripcion = models.CharField(max_length=200, blank=True, verbose_name='Descripción')

    class Meta:
        verbose_name = 'Línea de asiento'
        verbose_name_plural = 'Líneas de asiento'

    def __str__(self):
        return f"{self.cuenta.codigo} - D:{self.debe} H:{self.haber}"

    def clean(self):
        if self.debe > 0 and self.haber > 0:
            raise ValidationError("Una línea no puede tener debe y haber simultáneamente")
    
    @property
    def importe(self):
        return self.debe if self.debe > 0 else self.haber
