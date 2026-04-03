# AGENTS.md - Guía de Código para Sarello ERP

Este documento proporciona instrucciones para agentes de código y desarrolladores que trabajan en el proyecto Django de Sarello ERP.

> **Documentación completa:** [docs/index.md](docs/index.md) — Guías de inicio, assets, Docker, troubleshooting y más.

---

## Comandos de Build, Lint y Testing

> Referencia completa: [docs/comandos.md](docs/comandos.md)

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas de una aplicación específica
pytest apps/contabilidad/

# Ejecutar un archivo de pruebas específico
pytest apps/contabilidad/tests.py

# Ejecutar una clase de pruebas específica
pytest apps/contabilidad/tests.py::MiClaseTest

# Ejecutar un método de prueba específico
pytest apps/contabilidad/tests.py::MiClaseTest::test_metodo_nombre

# Ejecutar con salida detallada
pytest -v

# Ejecutar con reporte de cobertura
pytest --cov=apps
```

### Comandos de Django

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# Crear migraciones después de cambios en modelos
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate

# Consola interactiva de Django
python manage.py shell

# Crear usuario administrador
python manage.py createsuperuser

# Recopilar archivos estáticos (producción)
python manage.py collectstatic --noinput
```

### Calidad de Código y Linting

```bash
# Verificar código con Ruff (linter/formateador)
ruff check .

# Corregir automáticamente con Ruff
ruff check . --fix

# Formatear código
ruff format .
```

---

## Guía de Estilo de Código

> Referencia completa: [docs/convenciones.md](docs/convenciones.md)

### Principios Generales

- **Idioma**: Español para nombres específicos del dominio (modelos, vistas), English para estructura
- **Formato**: Seguir PEP 8 (aplicado por Ruff)
- **Moneda**: Usar siempre `DecimalField` para dinero, NUNCA float
- **Zona horaria**: Usar `django.utils.timezone` para datetimes con zona horaria
- **Localización**: Español (España) para locale, zona horaria Argentina (America/Argentina/Buenos_Aires)

### Importaciones

- Importaciones de librería estándar primero
- Importaciones de terceros (Django, DRF) segundo
- Importaciones locales de la aplicación último
- Una línea en blanco entre grupos
- Evitar importaciones con wildcard (`from module import *`)

**Ejemplo:**

```python
from decimal import Decimal
from datetime import date, datetime
from django.db import models
from django.utils import timezone
from apps.base.models import TimeStampedModel, DocumentoBase
```

### Modelos

- Heredar de `TimeStampedModel` para campos automáticos `creado_en` y `modificado_en`
- Usar `verbose_name` para todas las etiquetas de campos (en español)
- Establecer `default_permissions = []` en Meta para permisos personalizados
- Definir método `__str__` en todos los modelos
- Usar tuplas `CHOICES` (snake_case en BD, strings legibles para display)
- Usar `related_name` en todas las relaciones ForeignKey/ManyToMany
- Siempre usar `on_delete` (preferir `PROTECT` para integridad)
- Usar `DecimalField(max_digits=15, decimal_places=2)` para dinero

**Ejemplo:**

```python
class CuentaContable(TimeStampedModel):
    TIPO_CHOICES = [
        ('activo', 'Activo'),
        ('pasivo', 'Pasivo'),
    ]

    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Cuenta contable'
        verbose_name_plural = 'Cuentas contables'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
```

### Vistas y ViewSets

- Usar class-based views para consistencia
- Usar DRF `ViewSet` para APIs
- Siempre verificar permisos con `@permission_required` o `check_object_permissions`
- Retornar códigos HTTP significativos

### Serializadores (DRF)

- Crear serializadores separados para vistas list/detail si es necesario
- Usar `SerializerMethodField` para propiedades computadas
- Validar precisión decimal para campos monetarios

### Manejo de Errores

- Usar `ValidationError` de Django para validación de modelos
- Lanzar `Http404` o DRF `NotFound` para recursos no encontrados
- Lanzar `PermissionDenied` para acceso no autorizado
- Nunca capturar broad `Exception` - ser específico
- Usar niveles de log apropiados (ERROR para fallos, WARNING para issues)

**Ejemplo:**

```python
from django.core.exceptions import ValidationError
from django.http import Http404

def clean(self):
    if self.debe > 0 and self.haber > 0:
        raise ValidationError("Una línea no puede tener debe y haber simultáneamente")
```

### Anotaciones de Tipo (Python 3.12)

- Usar type hints para argumentos y retorno de funciones
- Usar `Optional[Type]` para valores nulables
- Importar tipos del módulo `typing`

**Ejemplo:**

```python
from typing import Optional, List
from decimal import Decimal

def get_saldo_en_fecha(self, fecha_inicio: date, fecha_fin: date) -> Decimal:
    pass
```

### Convenciones de Nombres

- **Campos de modelos**: snake_case en español (ej. `creado_en`, `modificado_en`, `fecha_inicio`)
- **Columnas de BD**: Auto-generadas desde nombres de campos
- **Métodos**: snake_case (ej. `get_saldo_actual()`, `es_cuenta_hoja()`)
- **Constantes**: UPPER_SNAKE_CASE (ej. `ESTADO_CHOICES`, `TIPO_CHOICES`)
- **Clases**: PascalCase (ej. `CuentaContable`, `LineaAsiento`)
- **Métodos privados**: prefijo underscore (ej. `_calcular_saldo()`)

### Comentarios y Docstrings

- Usar docstrings para clases y funciones
- Mantener comentarios mínimos - el código debe ser auto-explicativo
- Para lógica compleja, explicar el "por qué" no el "qué"
- Usar español para explicaciones del dominio, inglés para comentarios técnicos

**Ejemplo:**

```python
def get_trimestre_actual(self) -> Optional[int]:
    """Calcula el trimestre del año fiscal actual."""
    today = date.today()
    if self.fecha_inicio <= today <= self.fecha_fin:
        mes = today.month
        return (mes - 1) // 3 + 1
    return None
```

### Testing

- Usar `pytest` con `pytest-django`
- Usar fixtures para objetos de BD
- Mockear dependencias externas
- Probar casos de éxito y error
- Nombrar tests descriptivamente: `test_<funcion>_<escenario>_<resultado_esperado>`

**Ejemplo:**

```python
import pytest
from django.test import TestCase
from apps.contabilidad.models import CuentaContable

@pytest.mark.django_db
class TestCuentaContable:
    def test_str_returns_codigo_and_nombre(self):
        cuenta = CuentaContable.objects.create(
            codigo='1', nombre='Activos'
        )
        assert str(cuenta) == '1 - Activos'
```

### Consultas a Base de Datos

- Usar `.select_related()` para optimizar ForeignKey
- Usar `.prefetch_related()` para relaciones inversas y M2M
- Evitar queries en loops (problema N+1)
- Usar `.exists()` en lugar de `.count()` para verificar existencia
- Usar `.aggregate()` para cálculos como Sum, Count, Avg

### Interfaz de Administración

- Registrar modelos en `apps/<app>/admin.py`
- Usar `list_display`, `list_filter`, `search_fields`
- Usar `readonly_fields` para campos computados/auto
- Implementar `__str__` para mejor visualización

---

## Estructura del Proyecto

> Referencia completa: [docs/estructura.md](docs/estructura.md)

```text
sarello/
├── apps/                          # Aplicaciones Django
│   ├── base/                      # Modelos base (TimeStampedModel, DocumentoBase)
│   ├── contabilidad/              # Módulo de contabilidad
│   ├── tesoreria/                 # Módulo de tesorería/cajas
│   ├── impuestos/                 # Módulo de impuestos
│   ├── contactos/                 # Módulo de contactos (clientes/proveedores)
│   ├── inventario/                # Módulo de inventario/productos
│   ├── ventas/                    # Módulo de ventas
│   ├── compras/                   # Módulo de compras
│   ├── manufactura/               # Módulo de manufactura
│   ├── configuracion/             # Módulo de configuración
│   └── integraciones/             # Integraciones (AFIP, etc)
├── core/                          # Configuración de Django
├── templates/                     # Plantillas HTML
├── staticfiles/                   # Assets en desarrollo (fuente)
├── static/                        # Assets compilados para producción
├── docs/                          # Documentación del proyecto
├── requirements/                  # Dependencias
│   ├── base.txt                   # Dependencias core
│   ├── local.txt                  # Extras de desarrollo
│   └── production.txt             # Dependencias de producción
├── manage.py                      # CLI de Django
├── AGENTS.md                      # Este archivo
└── README.md                      # Entrada principal del proyecto
```

---

## Dependencias Clave

- **Django 5.2**: Framework web
- **Django REST Framework 3.15**: Framework para APIs REST
- **pytest 8.3 + pytest-django 4.9**: Testing
- **Ruff 0.9**: Linting y formateador
- **PostgreSQL** (producción) / SQLite (desarrollo)
- **Celery 5.4**: Tareas asincrónicas
- **Django Allauth 65.15**: Autenticación

---

## Configuración del Entorno

- Crear `.env` desde `.env.example`
- Establecer `SECRET_KEY` (cambiar en producción!)
- Establecer `DEBUG=True` en desarrollo, `False` en producción
- Configurar `ALLOWED_HOSTS` para deployment
- Producción usa PostgreSQL, desarrollo usa SQLite

---

## Notas Importantes

- **Precisión decimal**: Todas las operaciones financieras usan Decimal con 2 decimales
- **Auditoría**: Todos los modelos heredan de TimeStampedModel para timestamps automáticos
- **Estados de documentos**: Usar DocumentoBase para facturas, comprobantes (borrador → confirmado → cancelado)
- **Especificidades argentinas**: Soporta integración AFIP, impuestos IVA/IIBB, facturación electrónica (Fase 7)
- **Zona horaria**: Todos los dates usan zona horaria America/Argentina/Buenos_Aires

---

## Consideraciones de Rendimiento

- Siempre usar `select_related()` y `prefetch_related()` para foreign keys
- Crear índices de BD para campos consultados frecuentemente
- Cachear cálculos costosos con Redis (configurado en settings)
- Usar Celery para operaciones de larga duración
- Perfilar con Django Debug Toolbar en desarrollo
