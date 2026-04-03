# Componentes de Template

Componentes reutilizables de Django templates en `templates/components/`.

---

## Estructura

```
templates/
├── base.html                    # Layout principal (DaisyUI dark theme, HTMX, Alpine.js)
├── components/
│   ├── alerts/
│   │   ├── message.html         # Django messages framework (implementado)
│   │   └── alert.html           # (vacío — placeholder)
│   ├── badges/
│   │   └── badge.html
│   ├── breadcrumbs/
│   │   └── breadcrumb.html
│   ├── buttons/
│   │   └── button.html          # (vacío — placeholder)
│   ├── cards/
│   │   └── card.html
│   ├── dividers/
│   │   └── divider.html
│   ├── empty-states/
│   │   └── empty-state.html
│   ├── forms/
│   │   ├── form-field.html      # Input genérico
│   │   ├── form-group.html      # Wrapper para Django BoundField
│   │   ├── select.html          # Dropdown select
│   │   └── textarea.html
│   ├── modals/
│   │   └── modal.html
│   ├── tables/
│   │   └── table.html
│   ├── page-header.html         # (vacío — placeholder)
│   └── pagination.html
└── partials/
    └── drawer.html              # Sidebar de navegación (autenticados)
```

**16 archivos HTML en `components/`** (3 vacíos) + **1 en `partials/`**.

---

## Reglas de uso

1. Las etiquetas `{% include %}` deben estar en **una sola línea**
2. No usar filtros dentro del `with`
3. Preparar variables en las vistas, no en plantillas
4. Los componentes usan clases de Tailwind + DaisyUI directamente

### Preparar variables en la vista

```python
def mi_vista(request):
    return render(request, 'template.html', {
        'card_title': 'Crear Cuenta',
    })
```

```html
{% include "components/cards/card.html" with title=card_title content=content_html %}
```

---

## Componentes implementados

### Alerts — message.html

Renderiza mensajes de Django messages framework.

```html
{% include "components/alerts/message.html" %}
```

Requiere `messages` en el contexto (inyectado por Django automáticamente si `django.contrib.messages` está en `INSTALLED_APPS`).

**Variantes:** `success` (verde), `error` (rojo), default/accent (azul).

### Badge

```html
{% include "components/badges/badge.html" with label="activo" variant="success" size="md" icon="fa-check" %}
```

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `label` | string | — | Texto del badge |
| `variant` | string | `"gray"` | `success`, `danger`, `warning`, `info`, `gray` |
| `size` | string | `"md"` | `sm`, `md`, `lg` |
| `icon` | string | — | Clase Font Awesome (ej: `"fa-check"`) |

### Breadcrumb

```html
{% include "components/breadcrumbs/breadcrumb.html" with items=breadcrumb_items %}
```

`items` es una lista de dicts: `{'url': '/ruta/', 'label': 'Inicio', 'icon': 'fa-home'}`.

- Items con `url` se renderizan como links
- Items sin `url` se renderizan como texto (página actual)
- Separador: chevron-right entre items

### Card

```html
{% include "components/cards/card.html" with title="Sección" subtitle="Descripción" content=content_html footer=footer_html %}
```

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `title` | string | Título del header |
| `subtitle` | string | Subtítulo opcional |
| `content` | HTML | Contenido principal |
| `footer` | HTML | Footer opcional |

### Divider

```html
{% include "components/dividers/divider.html" with text="O continuar con" %}
```

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `text` | string | — | Texto en el medio del divider (opcional) |

### Empty State

```html
{% include "components/empty-states/empty-state.html" with icon="fa-inbox" title="Sin registros" description="No hay datos para mostrar" action_url="/crear/" action_label="Crear" action_icon="fa-plus" %}
```

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `icon` | string | — | Clase Font Awesome |
| `title` | string | — | Título |
| `description` | string | — | Descripción |
| `action_url` | string | — | URL del botón CTA |
| `action_label` | string | `"Crear"` | Texto del botón |
| `action_icon` | string | — | Icono del botón |

### Forms

#### form-field.html (input genérico)

```html
{% include "components/forms/form-field.html" with type="text" name="email" label="Email" value="" placeholder="tu@email.com" required=True help_text="Opcional" error="" %}
```

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `type` | string | `"text"` | Tipo de input |
| `name` | string | — | Nombre del campo |
| `label` | string | — | Etiqueta |
| `value` | string | `""` | Valor actual |
| `placeholder` | string | `""` | Placeholder |
| `required` | bool | `False` | Campo obligatorio |
| `readonly` | bool | `False` | Solo lectura |
| `help_text` | string | — | Texto de ayuda |
| `error` | string | `""` | Mensaje de error |

#### form-group.html (wrapper para Django BoundField)

```html
{% include "components/forms/form-group.html" with label="Email" field=form.email %}
```

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `label` | string | Etiqueta (opcional, si no se usa la del form) |
| `field` | BoundField | Campo de Django form |

Renderiza el campo con su help text y errores de validación.

#### select.html

```html
{% include "components/forms/select.html" with name="tipo" label="Tipo" choices=tipo_choices value="" required=True %}
```

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `name` | string | — | Nombre del select |
| `label` | string | — | Etiqueta |
| `choices` | list | — | Lista de `[value, label]` |
| `value` | string | — | Valor seleccionado |
| `required` | bool | `False` | Campo obligatorio |
| `disabled` | bool | `False` | Deshabilitado |
| `help_text` | string | — | Texto de ayuda |
| `error` | string | — | Mensaje de error |

Agrega opción `"-- Seleccionar --"` cuando `required=False`.

#### textarea.html

```html
{% include "components/forms/textarea.html" with name="descripcion" label="Descripción" value="" rows=4 placeholder="..." %}
```

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `name` | string | — | Nombre |
| `label` | string | — | Etiqueta |
| `value` | string | `""` | Contenido |
| `rows` | int | `4` | Número de filas |
| `placeholder` | string | `""` | Placeholder |
| `required` | bool | `False` | Obligatorio |
| `readonly` | bool | `False` | Solo lectura |
| `help_text` | string | — | Texto de ayuda |
| `error` | string | — | Mensaje de error |

### Modal

```html
{% include "components/modals/modal.html" with modal_id="delete-confirm" title="Confirmar eliminación" content=content_html show_actions=True confirm_label="Eliminar" %}
```

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `modal_id` | string | `"modal"` | ID del elemento |
| `title` | string | — | Título del modal |
| `content` | HTML | — | Contenido |
| `show_actions` | bool | `False` | Mostrar botones Cancelar/Confirmar |
| `confirm_label` | string | `"Confirmar"` | Texto del botón confirmar |

Oculto por defecto (`hidden` class). Se muestra vía JS con `data-modal`. Botones usan `data-close-modal` y `data-confirm-modal`.

### Table

```html
{% include "components/tables/table.html" with columns=columns_config data=items empty_message="Sin resultados" %}
```

`columns` es una lista de dicts:

```python
columns = [
    {'label': 'Código', 'key': 'codigo'},
    {'label': 'Nombre', 'key': 'nombre'},
    {'label': 'Tipo', 'key': 'tipo', 'type': 'badge', 'variant': 'info'},
    {'label': 'Saldo', 'key': 'saldo', 'type': 'currency'},
    {'label': 'Fecha', 'key': 'fecha_creacion', 'type': 'date'},
    {'label': 'Acciones', 'key': 'url', 'type': 'link', 'link_label': 'Ver'},
]
```

| Tipo de celda | Comportamiento |
|---------------|----------------|
| (default) | Texto plano |
| `badge` | Incluye `components/badges/badge.html` con `variant` |
| `currency` | Formatea con 2 decimales (`floatformat:2`) |
| `date` | Formatea como `dd/mm/YYYY` |
| `link` | Renderiza como `<a href="...">` con `link_label` |

**Nota:** Usa el filtro custom `dict_lookup` para acceder a valores por key en el dict de cada row.

### Pagination

```html
{% include "components/pagination.html" with page_obj=page_obj query_params="&tipo=activo" %}
```

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `page_obj` | Page | Objeto Django Paginator |
| `query_params` | string | Parámetros adicionales para las URLs (ej: `"&q=busqueda"`) |

Muestra: primera, anterior, número de página, siguiente, última. Solo se renderiza si hay múltiples páginas.

---

## Componentes vacíos (placeholders)

| Archivo | Estado |
|---------|--------|
| `alerts/alert.html` | Vacío — usar `message.html` para Django messages |
| `buttons/button.html` | Vacío — usar clases DaisyUI `btn btn-primary` directamente |
| `page-header.html` | Vacío — usar estructura inline en templates |

---

## Partial: drawer.html

Sidebar de navegación para usuarios autenticados. Se incluye en `base.html`:

```html
{% include 'partials/drawer.html' %}
```

**Secciones:**
- **Contabilidad:** Dashboard, Plan de Cuentas, Asientos, Libro Diario, Mayor, Balance, Estado Resultados, Impuestos
- **Tesorería:** Dashboard, Cuentas, Movimientos, Ingresos, Egresos, Caja Diaria
- **General:** Contactos, Configuración

Muestra avatar (primera letra del username), nombre, email y botón de logout.

---

## Variantes de colores

### Badges

`success`, `danger`, `warning`, `info`, `gray`

### Alerts (message.html)

`success` (verde), `error` (rojo), default/accent (azul)

---

## Ver también

- [Gestión de assets](assets.md) — CSS y estructura visual
- [Convenciones de código](convenciones.md) — Cómo escribir vistas y plantillas
