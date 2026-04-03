# Convenciones de Código

Guía de estilo y mejores prácticas para desarrollar en Sarello ERP.

> **Nota para agentes de IA:** La versión completa y optimizada para agentes está en `AGENTS.md` en la raíz del proyecto.

---

## Principios generales

- **Idioma:** Español para nombres del dominio (modelos, campos), inglés para estructura técnica
- **Moneda:** Siempre `DecimalField`, nunca float
- **Zona horaria:** `django.utils.timezone` con America/Argentina/Buenos_Aires
- **Formato:** PEP 8 (aplicado por Ruff)

---

## Importaciones

Orden:
1. Librería estándar
2. Terceros (Django, DRF)
3. Importaciones locales

Una línea en blanco entre grupos. Sin wildcard imports.

```python
from decimal import Decimal
from datetime import date

from django.db import models
from django.utils import timezone

from apps.base.models import TimeStampedModel
```

---

## Modelos

- Heredar de `TimeStampedModel` para `creado_en` y `modificado_en`
- Usar `verbose_name` en todos los campos (en español)
- `default_permissions = []` en Meta para permisos personalizados
- Método `__str__` en todos los modelos
- Tuplas `CHOICES` en snake_case para BD
- `related_name` en todas las relaciones ForeignKey/ManyToMany
- Preferir `on_delete=PROTECT` para integridad
- `DecimalField(max_digits=15, decimal_places=2)` para dinero

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

---

## Vistas y ViewSets

- Usar class-based views
- DRF `ViewSet` para APIs
- Verificar permisos con `@permission_required` o `check_object_permissions`
- Retornar códigos HTTP significativos

---

## Serializadores (DRF)

- Serializadores separados para vistas list/detail si es necesario
- `SerializerMethodField` para propiedades computadas
- Validar precisión decimal para campos monetarios

---

## Manejo de errores

- `ValidationError` de Django para validación de modelos
- `Http404` o DRF `NotFound` para recursos no encontrados
- `PermissionDenied` para acceso no autorizado
- Nunca capturar broad `Exception`

```python
from django.core.exceptions import ValidationError

def clean(self):
    if self.debe > 0 and self.haber > 0:
        raise ValidationError("Una línea no puede tener debe y haber simultáneamente")
```

---

## Type hints

Usar type hints para argumentos y retorno de funciones.

```python
from typing import Optional
from decimal import Decimal

def get_saldo_en_fecha(self, fecha_inicio: date, fecha_fin: date) -> Decimal:
    """Calcula el saldo en un período."""
    pass
```

---

## Convenciones de nombres

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Campos de modelos | snake_case en español | `creado_en`, `fecha_inicio` |
| Métodos | snake_case | `get_saldo_actual()` |
| Métodos privados | prefijo underscore | `_calcular_saldo()` |
| Constantes | UPPER_SNAKE_CASE | `ESTADO_CHOICES` |
| Clases | PascalCase | `CuentaContable` |

---

## Testing

- Usar `pytest` con `pytest-django`
- Fixtures para objetos de BD
- Mockear dependencias externas
- Nombrar tests: `test_<funcion>_<escenario>_<resultado>`

```python
@pytest.mark.django_db
class TestCuentaContable:
    def test_str_returns_codigo_and_nombre(self):
        cuenta = CuentaContable.objects.create(
            codigo='1', nombre='Activos'
        )
        assert str(cuenta) == '1 - Activos'
```

---

## Consultas a base de datos

- `.select_related()` para ForeignKey
- `.prefetch_related()` para relaciones inversas y M2M
- Evitar queries en loops (problema N+1)
- `.exists()` en lugar de `.count()` para verificar existencia
- `.aggregate()` para Sum, Count, Avg

---

## Interfaz de administración

- Registrar modelos en `apps/<app>/admin.py`
- Usar `list_display`, `list_filter`, `search_fields`
- `readonly_fields` para campos computados

---

## Dependencias clave

| Paquete | Versión | Uso |
|---------|---------|-----|
| Django | 5.2 | Framework web |
| DRF | 3.15 | APIs REST |
| pytest | 8.3 | Testing |
| Ruff | 0.9 | Linting |
| Celery | 5.4 | Tareas asincrónicas |
| Allauth | 65.15 | Autenticación |

---

## Ver también

- [Guía de inicio](guia-inicio.md) — Setup del entorno
- [Comandos útiles](comandos.md) — pytest, Ruff, Django
- [Estructura del proyecto](estructura.md) — Mapa de módulos
- `AGENTS.md` (raíz) — Guía completa para agentes de IA
