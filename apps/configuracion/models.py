from django.db import models
from apps.base.models import TimeStampedModel


class ParametroSistema(TimeStampedModel):
    GRUPO_CHOICES = [
        ('empresa', 'Empresa'),
        ('contabilidad', 'Contabilidad'),
        ('ventas', 'Ventas'),
        ('compras', 'Compras'),
        ('tesoreria', 'Tesorería'),
        ('facturacion', 'Facturación'),
        ('integraciones', 'Integraciones'),
    ]

    clave = models.CharField(max_length=50, unique=True, verbose_name='Clave')
    valor = models.TextField(verbose_name='Valor')
    descripcion = models.CharField(max_length=200, blank=True, verbose_name='Descripcion')
    grupo = models.CharField(max_length=20, choices=GRUPO_CHOICES, default='empresa', verbose_name='Grupo')
    editable = models.BooleanField(default=True, verbose_name='Editable')

    class Meta:
        verbose_name = 'Parámetro del sistema'
        verbose_name_plural = 'Parámetros del sistema'
        ordering = ['grupo', 'clave']

    def __str__(self):
        return f"{self.clave} = {self.valor}"

    @classmethod
    def get(cls, clave, default=None):
        try:
            return cls.objects.get(clave=clave).valor
        except cls.DoesNotExist:
            return default


class DatosEmpresa(TimeStampedModel):
    razon_social = models.CharField(max_length=200, verbose_name='Razón social')
    nombre_fantasia = models.CharField(max_length=200, blank=True, verbose_name='Nombre de fantasía')
    cuil = models.CharField(max_length=13, verbose_name='CUIL/CUIT')
    direccion = models.CharField(max_length=300, blank=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=50, blank=True, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Email')
    web = models.URLField(blank=True, verbose_name='Sitio web')
    condicion_iva = models.CharField(
        max_length=50,
        default='Responsable Inscripto',
        verbose_name='Condición frente al IVA'
    )
    numero_ingresos_brutos = models.CharField(max_length=50, blank=True, verbose_name='Número de Ingresos Brutos')
    inicio_actividades = models.DateField(null=True, blank=True, verbose_name='Inicio de actividades')
    logo = models.ImageField(upload_to='empresa/logos', null=True, blank=True, verbose_name='Logo')

    class Meta:
        verbose_name = 'Datos de la empresa'
        verbose_name_plural = 'Datos de la empresa'

    def __str__(self):
        return self.razon_social

    def save(self, *args, **kwargs):
        if not self.pk and DatosEmpresa.objects.exists():
            raise Exception("Solo puede existir un registro de empresa")
        super().save(*args, **kwargs)
