from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
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
    saldo_inicial = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name='Saldo inicial'
    )
    activa = models.BooleanField(default=True, verbose_name='Activa')

    class Meta:
        ordering = ['tipo', 'nombre']
        verbose_name = 'Cuenta de tesorería'
        verbose_name_plural = 'Cuentas de tesorería'

    def __str__(self):
        return f"{self.nombre} ({self.moneda})"

    @property
    def saldo_contable(self):
        """Fuente de verdad: viene de la contabilidad (LineaAsiento)."""
        return self.cuenta_contable.saldo_actual

    @property
    def saldo_tesoreria(self):
        """Cálculo propio: saldo_inicial + debe - haber desde líneas."""
        entradas = self.lineas.aggregate(total=Sum('debe'))['total'] or Decimal('0')
        salidas = self.lineas.aggregate(total=Sum('haber'))['total'] or Decimal('0')
        return self.saldo_inicial + entradas - salidas

    def conciliar(self):
        """Verifica que el saldo de tesorería coincida con el contable."""
        diff = self.saldo_tesoreria - self.saldo_contable
        return {
            'saldo_tesoreria': self.saldo_tesoreria,
            'saldo_contable': self.saldo_contable,
            'diferencia': diff,
            'conciliado': diff == Decimal('0'),
        }


class MovimientoTesoreria(DocumentoBase):
    TIPO_CHOICES = [
        ('cobro', 'Cobro'),
        ('pago', 'Pago'),
        ('transferencia', 'Transferencia'),
        ('ajuste', 'Ajuste de saldo'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    contacto = models.ForeignKey(
        'contactos.Contacto',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='movimientos_tesoreria',
        verbose_name='Contacto'
    )
    asiento_contable = models.ForeignKey(
        'contabilidad.Asiento',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='movimientos_tesoreria',
        verbose_name='Asiento contable'
    )

    class Meta:
        ordering = ['-fecha', '-numero']
        verbose_name = 'Movimiento de tesorería'
        verbose_name_plural = 'Movimientos de tesorería'

    def __str__(self):
        return f"{self.numero} - {self.get_tipo_display()} - {self.importe_total}"

    def clean(self):
        super().clean()
        if self.tipo == 'ajuste' and not self.observaciones:
            raise ValidationError({
                'observaciones': 'El motivo es obligatorio para ajustes de saldo'
            })

    @property
    def importe_total(self):
        """Suma de debe + haber de todas las líneas."""
        total = self.lineas.aggregate(d=Sum('debe'), h=Sum('haber'))
        return (total['d'] or Decimal('0')) + (total['h'] or Decimal('0'))

    def _detectar_contrapartida(self, linea):
        """Auto-detecta la cuenta contrapartida desde MapeoContable."""
        if linea.cuenta_contrapartida:
            return linea.cuenta_contrapartida

        from apps.contabilidad.models import MapeoContable

        tipo_cuenta = linea.cuenta.tipo
        eventos = {
            ('cobro', 'caja'): 'cobro_efectivo',
            ('cobro', 'banco'): 'cobro_banco',
            ('cobro', 'digital'): 'cobro_efectivo',
            ('pago', 'caja'): 'pago_efectivo',
            ('pago', 'banco'): 'pago_banco',
            ('pago', 'digital'): 'pago_efectivo',
            ('ajuste', 'caja'): 'ajuste_caja',
            ('ajuste', 'banco'): 'ajuste_banco',
            ('ajuste', 'digital'): 'ajuste_caja',
        }
        evento = eventos.get((self.tipo, tipo_cuenta))
        if not evento:
            return None

        if linea.debe > 0:
            return MapeoContable.obtener_contrapartida(evento, 'haber')
        else:
            return MapeoContable.obtener_contrapartida(evento, 'debe')

    def _construir_asiento(self, invertido=False):
        """Construye las líneas del asiento contable."""
        from apps.contabilidad.models import Asiento, LineaAsiento

        lineas_contables = []
        for linea in self.lineas.all():
            contrapartida = self._detectar_contrapartida(linea)
            if not contrapartida:
                raise ValidationError(
                    f"No se pudo determinar la contrapartida para la línea "
                    f"con cuenta {linea.cuenta}. Especificá una cuenta contrapartida."
                )

            if linea.debe > 0:
                if invertido:
                    lineas_contables.append({
                        'cuenta': contrapartida,
                        'debe': linea.debe,
                        'haber': Decimal('0'),
                        'descripcion': f'Anulación {self.numero} - {linea.cuenta.nombre}',
                    })
                    lineas_contables.append({
                        'cuenta': linea.cuenta.cuenta_contable,
                        'debe': Decimal('0'),
                        'haber': linea.debe,
                        'descripcion': f'Anulación {self.numero} - {linea.cuenta.nombre}',
                    })
                else:
                    lineas_contables.append({
                        'cuenta': linea.cuenta.cuenta_contable,
                        'debe': linea.debe,
                        'haber': Decimal('0'),
                        'descripcion': linea.descripcion or f'{self.get_tipo_display()} - {linea.cuenta.nombre}',
                    })
                    lineas_contables.append({
                        'cuenta': contrapartida,
                        'debe': Decimal('0'),
                        'haber': linea.debe,
                        'descripcion': linea.descripcion or f'{self.get_tipo_display()} - {linea.cuenta.nombre}',
                    })

            elif linea.haber > 0:
                if invertido:
                    lineas_contables.append({
                        'cuenta': linea.cuenta.cuenta_contable,
                        'debe': linea.haber,
                        'haber': Decimal('0'),
                        'descripcion': f'Anulación {self.numero} - {linea.cuenta.nombre}',
                    })
                    lineas_contables.append({
                        'cuenta': contrapartida,
                        'debe': Decimal('0'),
                        'haber': linea.haber,
                        'descripcion': f'Anulación {self.numero} - {linea.cuenta.nombre}',
                    })
                else:
                    lineas_contables.append({
                        'cuenta': contrapartida,
                        'debe': linea.haber,
                        'haber': Decimal('0'),
                        'descripcion': linea.descripcion or f'{self.get_tipo_display()} - {linea.cuenta.nombre}',
                    })
                    lineas_contables.append({
                        'cuenta': linea.cuenta.cuenta_contable,
                        'debe': Decimal('0'),
                        'haber': linea.haber,
                        'descripcion': linea.descripcion or f'{self.get_tipo_display()} - {linea.cuenta.nombre}',
                    })

        return lineas_contables

    def generar_asiento(self):
        """Genera el asiento contable para este movimiento confirmado."""
        from apps.contabilidad.models import Asiento, LineaAsiento

        if self.asiento_contable:
            return self.asiento_contable

        lineas_contables = self._construir_asiento(invertido=False)

        asiento = Asiento.objects.create(
            ejercicio=self._obtener_ejercicio(),
            numero=self._generar_numero_asiento(),
            fecha=self.fecha,
            descripcion=f'Movimiento {self.numero} - {self.get_tipo_display()}',
            origen='tesoreria',
            origen_id=self.pk,
            estado='confirmado',
        )

        for lc in lineas_contables:
            LineaAsiento.objects.create(asiento=asiento, **lc)

        self.asiento_contable = asiento
        self.save(update_fields=['asiento_contable'])
        return asiento

    def generar_asiento_inverso(self):
        """Genera un asiento de anulación (líneas invertidas)."""
        from apps.contabilidad.models import Asiento, LineaAsiento

        lineas_contables = self._construir_asiento(invertido=True)

        asiento = Asiento.objects.create(
            ejercicio=self._obtener_ejercicio(),
            numero=self._generar_numero_asiento(),
            fecha=self.fecha,
            descripcion=f'Anulación movimiento {self.numero} - {self.get_tipo_display()}',
            origen='tesoreria',
            origen_id=self.pk,
            estado='confirmado',
        )

        for lc in lineas_contables:
            LineaAsiento.objects.create(asiento=asiento, **lc)

        return asiento

    def _obtener_ejercicio(self):
        """Obtiene el ejercicio contable abierto para la fecha del movimiento."""
        from apps.contabilidad.models import Ejercicio

        ejercicio = Ejercicio.objects.filter(
            fecha_inicio__lte=self.fecha,
            fecha_fin__gte=self.fecha,
            estado='abierto',
        ).first()

        if not ejercicio:
            raise ValidationError(
                f'No hay ejercicio contable abierto para la fecha {self.fecha}'
            )
        return ejercicio

    def _generar_numero_asiento(self):
        """Genera un número único para el asiento."""
        from apps.contabilidad.models import Asiento

        ultimo = Asiento.objects.order_by('-pk').first()
        if ultimo:
            try:
                return str(int(ultimo.numero) + 1).zfill(4)
            except ValueError:
                return str(Asiento.objects.count() + 1).zfill(4)
        return '0001'

    def save(self, *args, **kwargs):
        estado_anterior = None
        if self.pk:
            try:
                estado_anterior = MovimientoTesoreria.objects.values_list('estado', flat=True).get(pk=self.pk)
            except MovimientoTesoreria.DoesNotExist:
                pass

        transicion_valida = True
        if estado_anterior == 'confirmado' and self.estado == 'cancelado':
            transicion_valida = False
            raise ValidationError('Un movimiento confirmado debe anularse antes de cancelarse')

        super().save(*args, **kwargs)

        if not transicion_valida:
            return

        if estado_anterior == 'borrador' and self.estado == 'confirmado':
            self.generar_asiento()
        elif estado_anterior == 'confirmado' and self.estado == 'anulado':
            self.generar_asiento_inverso()


class LineaMovimientoTesoreria(models.Model):
    movimiento = models.ForeignKey(
        MovimientoTesoreria,
        on_delete=models.CASCADE,
        related_name='lineas',
        verbose_name='Movimiento'
    )
    cuenta = models.ForeignKey(
        CuentaTesoreria,
        on_delete=models.PROTECT,
        related_name='lineas',
        verbose_name='Cuenta de tesorería'
    )
    debe = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name='Debe'
    )
    haber = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'), verbose_name='Haber'
    )
    cuenta_contrapartida = models.ForeignKey(
        'contabilidad.CuentaContable',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='+',
        verbose_name='Cuenta contrapartida'
    )
    descripcion = models.CharField(max_length=200, blank=True, verbose_name='Descripción')

    class Meta:
        verbose_name = 'Línea de movimiento'
        verbose_name_plural = 'Líneas de movimiento'

    def __str__(self):
        return f"{self.cuenta} - D:{self.debe} H:{self.haber}"

    def clean(self):
        if self.debe > 0 and self.haber > 0:
            raise ValidationError('Una línea no puede tener debe y haber simultáneamente')
        if self.debe == 0 and self.haber == 0:
            raise ValidationError('Una línea debe tener debe o haber')

    @property
    def importe(self):
        return self.debe if self.debe > 0 else self.haber
