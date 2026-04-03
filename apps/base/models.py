from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    modificado_en = models.DateTimeField(auto_now=True, verbose_name='Modificado')

    class Meta:
        abstract = True
        default_permissions = []


class DocumentoBase(TimeStampedModel):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('anulado', 'Anulado'),
    ]

    numero = models.CharField(max_length=20, unique=True, verbose_name='Número')
    fecha = models.DateField(default=timezone.now, verbose_name='Fecha')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador', verbose_name='Estado')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')

    class Meta:
        abstract = True
        ordering = ['-fecha', '-numero']
