# Componentes de Plantilla - Sarello ERP

Esta carpeta contiene componentes reutilizables organizados por categorías.

## Estructura

```
components/
├── README.md
├── page-header.html    # Encabezado de página
├── pagination.html # Paginación
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

## Componentes Disponibles

### 1. Buttons - buttons/button.html
```django
{% include "components/buttons/button.html" with 
    label="Click me" 
    variant="primary"  # primary, success, danger, warning, info, ghost
    size="md"         # sm, md, lg
    type="button"     # button, submit, reset
    icon="fa-save"
    disabled=False
%}
```

### 2. Cards - cards/card.html
```django
{% include "components/cards/card.html" with 
    title="Sección"
    subtitle="Descripción"
    content=content_html
    footer=footer_html
%}
```

### 3. Badges - badges/badge.html
```django
{% include "components/badges/badge.html" with 
    label="activo"
    variant="success"  # success, danger, warning, info, gray
    size="md"         # sm, md, lg
    icon="fa-check"
%}
```

### 4. Alerts - alerts/alert.html
```django
{% include "components/alerts/alert.html" with 
    message="Success!"
    title="Título"
    variant="success"  # success, danger, warning, info
    icon="fa-check-circle"
    dismissible=True
%}
```

### 5. Forms - forms/form-group.html
```django
{% include "components/forms/form-group.html" with 
    label="Email"
    field=form.email
    help_text="Opcional: tu email"
%}
```

### 6. Pagination - pagination.html
```django
{% include "components/pagination.html" with 
    page_obj=page_obj
    query_params="&tipo=activo&search=test"
%}
```

### 7. Tables - tables/table.html
```django
{% include "components/tables/table.html" with 
    columns=columns_config
    data=items
    empty_message="Sin resultados"
%}
```

### 8. Page Header - page-header.html
```django
{% include "components/page-header.html" with 
    title="Asientos Contables"
    subtitle="Listado del libro diario"
    action_label="Nuevo Asiento"
    action_url="{% url 'contabilidad:asiento_create' %}"
    action_icon="fa-plus"
%}
```

### 9. Breadcrumbs - breadcrumbs/breadcrumb.html
```django
{% include "components/breadcrumbs/breadcrumb.html" with items=breadcrumb_items %}
```

### 10. Modals - modals/modal.html
```django
{% include "components/modals/modal.html" with 
    modal_id="delete-confirm"
    title="Confirmar eliminación"
    show_actions=True
    confirm_label="Eliminar"
    content=content_html
%}
```

## Variantes de Colores

### Botones (variant)
- `primary` (azul) - Acciones principales
- `success` (verde) - Guardar, confirmar
- `danger` (rojo) - Eliminar, advertencia
- `warning` (amarillo) - Cambios importantes
- `info` (azul claro) - Información
- `ghost` (transparente) - Acciones secundarias

### Badges (variant)
- `success` - Estado activo/completado
- `danger` - Estado crítico/error
- `warning` - Atención requerida
- `info` - Información general
- `gray` - Estado neutral

### Alerts (variant)
- `success` - Operación exitosa
- `danger` - Error crítico
- `warning` - Advertencia
- `info` - Información general

## Tamaños

### Botones (size)
- `sm` - Pequeño (px-2 py-1)
- `md` - Mediano (px-4 py-2)
- `lg` - Grande (px-6 py-3)

### Badges (size)
- `sm` - Pequeña
- `md` - Mediana
- `lg` - Grande

## Ejemplos Completos

### Ejemplo 1: Lista con Paginación
```django
{% include "components/page-header.html" with 
    title="Asientos Contables"
    subtitle="Listado del libro diario"
    action_label="Nuevo Asiento"
    action_url="..." %}

{% include "components/tables/table.html" with 
    columns=columns
    data=asientos
    empty_message="No hay asientos registrados" %}

{% include "components/pagination.html" with page_obj=page_obj %}
```

### Ejemplo 2: Formulario
```django
{% include "components/cards/card.html" with title="Crear Cuenta" %}
    <form method="post">
        {% csrf_token %}
        {% include "components/forms/form-group.html" with label="Código" field=form.codigo %}
        {% include "components/forms/form-group.html" with label="Nombre" field=form.nombre %}
        {% include "components/forms/form-group.html" with label="Tipo" field=form.tipo %}
        
        <div class="mt-6 flex gap-2">
            {% include "components/buttons/button.html" with label="Guardar" variant="success" type="submit" icon="fa-save" %}
            {% include "components/buttons/button.html" with label="Cancelar" variant="ghost" %}
        </div>
    </form>
```

### Ejemplo 3: Confirmación
```django
{% include "components/modals/modal.html" with 
    modal_id="delete-modal"
    title="Eliminar Registro"
    show_actions=True
    confirm_label="Eliminar"
    content="¿Está seguro de que desea eliminar este registro?" %}
```

## Notas Importantes

1. **Componentes anidables**: Puedes usar componentes dentro de otros
2. **Flexibilidad**: Todos los parámetros con valores por defecto son opcionales
3. **Consistencia**: Usar componentes asegura coherencia visual
4. **Mantenibilidad**: Los cambios de estilos se aplican globalmente
5. **Accesibilidad**: Los componentes incluyen atributos ARIA

## Clases CSS Disponibles

Los componentes utilizan clases CSS de Tailwind + DaisyUI:
- `.btn` - Clase base para botones
- `.btn-{variant}` - Variante de color
- `.badge` - Clase base para badges
- `.alert` - Clase base para alertas
- `.form-group` - Grupo de formulario