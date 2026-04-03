# Convenciones de Código

Guía de estilo y mejores prácticas para desarrollar en Sarello ERP.

> **Nota:** Esta guía refleja el estado actual del proyecto. Lo que está planificado pero aún no implementado se indica explícitamente.

---

## Principios generales

- **Idioma:** Español para nombres del dominio (modelos, campos), inglés para estructura técnica
- **Moneda:** Siempre `DecimalField(max_digits=15, decimal_places=2)`, nunca float
- **Zona horaria:** `django.utils.timezone` con `America/Argentina/Buenos_Aires`
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.base.models import TimeStampedModel
```

---

## Modelos

### Modelos base (`apps/base/models.py`)

**`TimeStampedModel`** (abstracto):
- `creado_en` — `DateTimeField(auto_now_add=True, verbose_name='Creado')`
- `modificado_en` — `DateTimeField(auto_now=True, verbose_name='Modificado')`
- `Meta`: `abstract = True`, `default_permissions = []`

**`DocumentoBase`** (abstracto, hereda TimeStampedModel):
- `ESTADO_CHOICES` — `[('borrador','Borrador'), ('confirmado','Confirmado'), ('cancelado','Cancelado')]`
- `numero` — `CharField(max_length=20, unique=True)`
- `fecha` — `DateField(default=timezone.now)`
- `estado` — `CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')`
- `observaciones` — `TextField(blank=True)`
- `Meta`: `abstract = True`, `ordering = ['-fecha', '-numero']`

### Reglas

- Heredar de `TimeStampedModel` para timestamps automáticos
- Heredar de `DocumentoBase` para facturas y comprobantes con estados
- Usar `verbose_name` en todos los campos (en español)
- `default_permissions = []` en Meta para permisos personalizados
- Método `__str__` en todos los modelos
- Tuplas `CHOICES` en UPPER_SNAKE_CASE
- `related_name` en todas las relaciones ForeignKey/ManyToMany
- Preferir `on_delete=PROTECT` para integridad, `CASCADE` para ownership, `SET_NULL` para opcionales
- Referencias cross-app como string: `'contabilidad.CuentaContable'`
- Usar `related_name='+'` para deshabilitar relación inversa cuando no se necesita

### Ejemplo

```python
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
        'self', null=True, blank=True,
        related_name='hijos', on_delete=models.PROTECT,
        verbose_name='Cuenta padre'
    )
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Cuenta contable'
        verbose_name_plural = 'Cuentas contables'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
```

### Patrones especiales

**Singleton** (`DatosEmpresa`):
```python
def save(self, *args, **kwargs):
    if not self.pk and DatosEmpresa.objects.exists():
        raise ValidationError("Solo puede existir un registro")
    super().save(*args, **kwargs)
```

**Acceso tipo clase** (`ParametroSistema`):
```python
@classmethod
def get(cls, clave, default=None):
    try:
        return cls.objects.get(clave=clave).valor
    except cls.DoesNotExist:
        return default
```

---

## Vistas

### Patrón actual: 100% Function-Based Views

**No se usan Class-Based Views ni ViewSets.** Todas las vistas son funciones decoradas con `@login_required`.

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def plan_cuentas(request):
    busqueda = request.GET.get('q', '')
    tipo = request.GET.get('tipo', '')

    cuentas = CuentaContable.objects.all()
    if busqueda:
        cuentas = cuentas.filter(
            Q(codigo__icontains=busqueda) | Q(nombre__icontains=busqueda)
        )
    if tipo:
        cuentas = cuentas.filter(tipo=tipo)

    paginator = Paginator(cuentas, 25)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'contabilidad/plan_cuentas.html', {
        'page_obj': page_obj,
        'busqueda': busqueda,
    })
```

### Patrones observados

| Patrón | Cómo se usa |
|--------|-------------|
| Permisos | Solo `@login_required` (no hay `@permission_required`) |
| CRUD | Funciones separadas: `lista`, `create`, `edit`, `delete`, `detail` |
| Paginación | `django.core.paginator.Paginator` (20-50 items) |
| Búsqueda | `request.GET.get('q')` con objetos `Q` |
| Filtros | `request.GET.get('tipo', '')` |
| Mensajes | `django.contrib.messages` |
| Redirects | Con URLs namespaced: `redirect('contabilidad:plan_cuentas')` |
| HTMX | Detección: `request.headers.get('HX-Request')` |
| JSON responses | `JsonResponse` para endpoints AJAX |
| CSV export | `HttpResponse(content_type='text/csv')` |
| Formularios | `ModelForm` — algunos en `forms.py`, la mayoría inline en `views.py` |

### Formularios inline en vistas

```python
@login_required
def cuenta_create(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada correctamente')
            return redirect('contabilidad:plan_cuentas')
    else:
        form = CuentaForm()
    return render(request, 'contabilidad/cuenta_form.html', {'form': form})
```

### Formularios con Tailwind en widgets

```python
class CuentaTesoreriaForm(forms.ModelForm):
    class Meta:
        model = CuentaTesoreria
        fields = ['nombre', 'tipo', 'moneda', 'saldo_inicial']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded px-3 py-2'}),
        }
```

### HTMX

```python
@login_required
def cuenta_toggle_active(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    cuenta.activa = not cuenta.activa
    cuenta.save()
    return JsonResponse({'activa': cuenta.activa})
```

---

## URLs

Cada app tiene su `urls.py` con `app_name` para namespacing:

```python
from django.urls import path
from . import views

app_name = 'contabilidad'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plan-cuentas/', views.plan_cuentas, name='plan_cuentas'),
    path('plan-cuentas/nuevo/', views.cuenta_create, name='cuenta_create'),
    path('plan-cuentas/<int:pk>/', views.cuenta_detail, name='cuenta_detail'),
    path('plan-cuentas/<int:pk>/editar/', views.cuenta_edit, name='cuenta_edit'),
    path('plan-cuentas/<int:pk>/eliminar/', views.cuenta_delete, name='cuenta_delete'),
]
```

Core `urls.py` incluye las apps:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', RedirectView.as_view(url='/contabilidad/')),
    path('contabilidad/', include('apps.contabilidad.urls')),
    path('tesoreria/', include('apps.tesoreria.urls')),
    path('impuestos/', include('apps.impuestos.urls')),
    path('contactos/', include('apps.contactos.urls')),
    path('configuracion/', include('apps.configuracion.urls')),
]
```

---

## API / Serializers

**No implementado.** DRF está en `INSTALLED_APPS` y configurado, pero no hay `serializers.py` ni endpoints API. El proyecto usa solo vistas HTML server-rendered.

---

## Admin

**No se usa.** Todos los `admin.py` son stubs vacíos. La gestión de datos se hace a través de vistas custom.

---

## Testing

**Stubs vacíos.** Los archivos `tests.py` usan `django.test.TestCase` pero no hay tests escritos. `pytest` y `pytest-django` están en las dependencias pero no configurados activamente.

---

## Manejo de errores

- `ValidationError` de Django para validación de modelos
- `get_object_or_404` para recursos no encontrados
- Nunca capturar broad `Exception`

```python
def clean(self):
    if self.debe > 0 and self.haber > 0:
        raise ValidationError("Una línea no puede tener debe y haber simultáneamente")
```

---

## Convenciones de nombres

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Campos de modelos | snake_case en español | `creado_en`, `fecha_inicio` |
| Métodos | snake_case | `get_saldo_actual()` |
| Métodos privados | prefijo underscore | `_calcular_saldo()` |
| Constantes | UPPER_SNAKE_CASE | `ESTADO_CHOICES`, `TIPO_CHOICES` |
| Clases | PascalCase | `CuentaContable` |
| URLs | kebab-case | `plan-cuentas/`, `cuenta-create/` |
| Names de URL | snake_case | `plan_cuentas`, `cuenta_create` |

---

## Consultas a base de datos

- `.select_related()` para ForeignKey (usado donde aplica)
- `.prefetch_related()` para relaciones inversas y M2M
- Evitar queries en loops (problema N+1)
- `.exists()` en lugar de `.count()` para verificar existencia
- `.aggregate()` para Sum, Count, Avg

---

## Configuración

| Setting | Valor actual |
|---------|--------------|
| Base de datos | SQLite (desarrollo) |
| Cache | LocMemCache |
| Auth | Django Allauth (email + username) |
| REST Framework | `IsAuthenticated` default, `SessionAuthentication` |
| Language | `es-ar` |
| Timezone | `America/Argentina/Buenos_Aires` |
| Default auto field | `BigAutoField` |

**No configurado:** PostgreSQL, Redis, Celery.

---

## Estado de los módulos

| Módulo | Estado |
|--------|--------|
| `base` | Modelos base implementados |
| `contabilidad` | Completo — CRUD, reportes, HTMX, importación CSV |
| `tesoreria` | Implementado — CRUD cuentas y movimientos |
| `impuestos` | Implementado — tipos, alícuotas |
| `contactos` | Implementado — CRUD con búsqueda |
| `configuracion` | Stub — solo urls con TemplateView |
| `ventas` | Vacío |
| `compras` | Vacío |
| `manufactura` | Vacío |
| `inventario` | Vacío |
| `integraciones` | Vacío |

---

## Ver también

- [Guía de inicio](guia-inicio.md) — Setup del entorno
- [Comandos útiles](comandos.md) — pytest, Ruff, Django
- [Estructura del proyecto](estructura.md) — Mapa de módulos
- `AGENTS.md` (raíz) — Guía completa para agentes de IA
