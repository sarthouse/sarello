# Componentes de Template

Componentes reutilizables de Django templates en `templates/components/`.

---

## Estructura

```
components/
├── page-header.html       # Encabezado de página
├── pagination.html        # Paginación
├── alerts/
│   └── alert.html
├── badges/
│   └── badge.html
├── breadcrumbs/
│   └── breadcrumb.html
├── buttons/
│   └── button.html
├── cards/
│   └── card.html
├── dividers/
│   └── divider.html
├── empty-states/
│   └── empty-state.html
├── forms/
│   ├── form-field.html
│   ├── form-group.html
│   ├── select.html
│   └── textarea.html
├── modals/
│   └── modal.html
└── tables/
    └── table.html
```

---

## Reglas de uso

1. Las etiquetas `{% include %}` deben estar en **una sola línea**
2. No usar filtros dentro del `with`
3. Preparar variables en las vistas, no en plantillas
4. Los componentes incluyen accesibilidad ARIA

### Preparar variables en la vista

```python
# views.py
def mi_vista(request):
    contexto = {
        'card_title': 'Crear Cuenta',
    }
    return render(request, 'template.html', contexto)
```

```html
<!-- template.html -->
{% include "components/cards/card.html" with title=card_title %}
```

---

## Componentes disponibles

### Buttons

```django
{% include "components/buttons/button.html" with label="Click me" variant="primary" size="md" type="button" icon="fa-save" disabled=False %}
```

### Cards

```django
{% include "components/cards/card.html" with title="Sección" subtitle="Descripción" content=content_html footer=footer_html %}
```

### Badges

```django
{% include "components/badges/badge.html" with label="activo" variant="success" size="md" icon="fa-check" %}
```

### Alerts

```django
{% include "components/alerts/alert.html" with message="Success!" title="Título" variant="success" icon="fa-check-circle" dismissible=True %}
```

### Forms

```django
{% include "components/forms/form-group.html" with label="Email" field=form.email help_text="Opcional" %}
```

### Pagination

```django
{% include "components/pagination.html" with page_obj=page_obj query_params="&tipo=activo" %}
```

### Tables

```django
{% include "components/tables/table.html" with columns=columns_config data=items empty_message="Sin resultados" %}
```

### Page Header

```django
{% include "components/page-header.html" with title="Asientos Contables" subtitle="Listado" action_label="Nuevo" action_url="/ruta/" action_icon="fa-plus" %}
```

### Breadcrumbs

```django
{% include "components/breadcrumbs/breadcrumb.html" with items=breadcrumb_items %}
```

### Modals

```django
{% include "components/modals/modal.html" with modal_id="delete-confirm" title="Confirmar" show_actions=True confirm_label="Eliminar" content=content_html %}
```

---

## Variantes de colores

### Botones

| Variant | Color | Uso |
|---------|-------|-----|
| `primary` | Azul | Acciones principales |
| `success` | Verde | Guardar, confirmar |
| `danger` | Rojo | Eliminar |
| `warning` | Amarillo | Cambios importantes |
| `info` | Azul claro | Información |
| `ghost` | Transparente | Secundarias |

### Badges

`success`, `danger`, `warning`, `info`, `gray`

### Alerts

`success`, `danger`, `warning`, `info`

---

## Tamaños

- Botones: `sm`, `md`, `lg`
- Badges: `sm`, `md`, `lg`

---

## Ver también

- [Gestión de assets](assets.md) — CSS y estructura visual
- [Convenciones de código](convenciones.md) — Cómo escribir vistas y plantillas
