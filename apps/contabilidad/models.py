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
        from django.db.models import Sum
        agg = self.lineas.aggregate(debe=Sum('debe'), haber=Sum('haber'))
        debe = agg['debe'] or Decimal('0.00')
        haber = agg['haber'] or Decimal('0.00')
        
        if self.tipo in ['activo', 'egreso']:
            return debe - haber
        else:
            return haber - debe

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
        ('apertura', 'Apertura'),
        ('cierre', 'Cierre'),
        ('ajuste', 'Ajuste'),
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


class MapeoContable(TimeStampedModel):
    EVENTO_CHOICES = [
        ('venta_gravada', 'Venta gravada'),
        ('venta_exenta', 'Venta exenta'),
        ('venta_iva', 'Venta IVA'),
        ('compra_gravada', 'Compra gravada'),
        ('compra_exenta', 'Compra exenta'),
        ('compra_iva', 'Compra IVA'),
        ('cobro_efectivo', 'Cobro en efectivo'),
        ('cobro_banco', 'Cobro por banco'),
        ('pago_efectivo', 'Pago en efectivo'),
        ('pago_banco', 'Pago por banco'),
        ('ajuste_stock_entrada', 'Ajuste stock entrada'),
        ('ajuste_stock_salida', 'Ajuste stock salida'),
        ('devolucion_venta', 'Devolución de venta'),
        ('devolucion_compra', 'Devolución de compra'),
    ]

    evento = models.CharField(max_length=50, unique=True, choices=EVENTO_CHOICES, verbose_name='Evento')
    cuenta_debe = models.ForeignKey(
        'contabilidad.CuentaContable',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Cuenta debe'
    )
    cuenta_haber = models.ForeignKey(
        'contabilidad.CuentaContable',
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Cuenta haber'
    )
    descripcion = models.CharField(max_length=200, blank=True, verbose_name='Descripcion')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Mapeo contable'
        verbose_name_plural = 'Mapeos contables'

    def __str__(self):
        return f"{self.get_evento_display()} -> D:{self.cuenta_debe.codigo} / H:{self.cuenta_haber.codigo}"

    @classmethod
    def obtener_contrapartida(cls, evento, direccion='debe'):
        """Devuelve la cuenta contable para la dirección especificada del evento."""
        try:
            mapeo = cls.objects.get(evento=evento, activo=True)
            return getattr(mapeo, f'cuenta_{direccion}')
        except cls.DoesNotExist:
            return None


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
        CuentaContable,
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
        CuentaContable,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Cuenta debe'
    )
    cuenta_contable_haber = models.ForeignKey(
        CuentaContable,
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
