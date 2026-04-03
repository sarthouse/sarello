# Componentes de Plantilla - Sarello ERP

Esta carpeta contiene componentes reutilizables organizados por categorías.

## Estructura

```
components/
├── README.md
├── page-header.html    # Encabezado de página
├── pagination.html   # Paginación
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

## Uso Correcto

**Importante**: Las etiquetas `{% include %}` deben estar en una sola línea. No se pueden partir en múltiples líneas ni usar filtros dentro del `with`.

### Variables en el contexto

Las variables deben prepararse en las vistas (views.py), no en la plantilla.

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

## Componentes Disponibles

### 1. Buttons
```django
{% include "components/buttons/button.html" with label="Click me" variant="primary" size="md" type="button" icon="fa-save" disabled=False %}
```

### 2. Cards
```django
{% include "components/cards/card.html" with title="Sección" subtitle="Descripción" content=content_html footer=footer_html %}
```

### 3. Badges
```django
{% include "components/badges/badge.html" with label="activo" variant="success" size="md" icon="fa-check" %}
```

### 4. Alerts
```django
{% include "components/alerts/alert.html" with message="Success!" title="Título" variant="success" icon="fa-check-circle" dismissible=True %}
```

### 5. Forms
```django
{% include "components/forms/form-group.html" with label="Email" field=form.email help_text="Opcional" %}
```

### 6. Pagination
```django
{% include "components/pagination.html" with page_obj=page_obj query_params="&tipo=activo" %}
```

### 7. Tables
```django
{% include "components/tables/table.html" with columns=columns_config data=items empty_message="Sin resultados" %}
```

### 8. Page Header
```django
{% include "components/page-header.html" with title="Asientos Contables" subtitle="Listado" action_label="Nuevo" action_url="/ruta/" action_icon="fa-plus" %}
```

### 9. Breadcrumbs
```django
{% include "components/breadcrumbs/breadcrumb.html" with items=breadcrumb_items %}
```

### 10. Modals
```django
{% include "components/modals/modal.html" with modal_id="delete-confirm" title="Confirmar" show_actions=True confirm_label="Eliminar" content=content_html %}
```

## Variantes de Colores

### Botones (variant)
- `primary` (azul) - Acciones principales
- `success` (verde) - Guardar, confirmar
- `danger` (rojo) - Eliminar
- `warning` (amarillo) - Cambios importantes
- `info` (azul claro) - Información
- `ghost` (transparente) - Secundarias

### Badges (variant)
- `success`, `danger`, `warning`, `info`, `gray`

### Alerts (variant)
- `success`, `danger`, `warning`, `info`

## Tamaños

- Botones: `sm`, `md`, `lg`
- Badges: `sm`, `md`, `lg`

## Notas Importantes

1. Las etiquetas `{% include %}` deben estar en una sola línea
2. No usar filtros dentro del `with`
3. Preparar variables en las vistas, no en plantillas
4. Usar componentes asegurar coherencia visual
5. Los componentes incluyen accesibilidad ARIA