# Componentes de Plantilla - Sarello ERP

Esta carpeta contiene componentes reutilizables que simplifican la creación de plantillas manteniendo consistencia visual.

## Componentes Disponibles

### 1. **button.html** - Botón
```django
{% include "components/button.html" with 
    label="Click me" 
    variant="primary"  # primary, success, danger, warning, info, ghost
    size="md"          # sm, md, lg
    type="button"      # button, submit, reset
    icon="fa-save"
    disabled=False
    data_action="submit"
%}
```

### 2. **card.html** - Tarjeta
```django
{% include "components/card.html" with 
    title="Sección"
    subtitle="Descripción"
    content=content_html
    footer=footer_html
%}
```

### 3. **badge.html** - Insignia/Etiqueta
```django
{% include "components/badge.html" with 
    label="activo"
    variant="success"  # success, danger, warning, info, gray
    size="md"          # sm, md, lg
    icon="fa-check"
%}
```

### 4. **alert.html** - Alerta
```django
{% include "components/alert.html" with 
    message="Success!"
    title="Título"
    variant="success"  # success, danger, warning, info
    icon="fa-check-circle"
    dismissible=True
%}
```

### 5. **form-group.html** - Grupo de Formulario
```django
{% include "components/form-group.html" with 
    label="Email"
    field=form.email
    help_text="Opcional: tu email"
%}
```

Nota: El campo debe ser un campo de formulario Django que incluya automáticamente errores.

### 6. **pagination.html** - Paginación
```django
{% include "components/pagination.html" with 
    page_obj=page_obj
    query_params="&tipo=activo&search=test"
%}
```

### 7. **table.html** - Tabla
```django
{% include "components/table.html" with 
    columns=columns_config
    data=items
    empty_message="Sin resultados"
%}
```

**Configuración de columns:**
```python
columns = [
    {"label": "Código", "key": "codigo"},
    {"label": "Nombre", "key": "nombre"},
    {"label": "Estado", "key": "estado", "type": "badge", "variant": "success"},
    {"label": "Monto", "key": "monto", "type": "currency"},
    {"label": "Fecha", "key": "fecha", "type": "date"},
]
```

### 8. **page-header.html** - Encabezado de Página
```django
{% include "components/page-header.html" with 
    title="Asientos Contables"
    subtitle="Listado del libro diario"
    action_label="Nuevo Asiento"
    action_url="{% url 'contabilidad:asiento_create' %}"
    action_icon="fa-plus"
%}
```

### 9. **breadcrumb.html** - Migajas de Pan
```django
{% include "components/breadcrumb.html" with items=breadcrumb_items %}
```

**Configuración de items:**
```python
items = [
    {"label": "Home", "url": "/"},
    {"label": "Contabilidad", "url": "/contabilidad"},
    {"label": "Asientos"},
]
```

### 10. **modal.html** - Modal
```django
{% include "components/modal.html" with 
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

### Insignias (variant)
- `success` - Estado activo/completado
- `danger` - Estado crítico/error
- `warning` - Atención requerida
- `info` - Información general
- `gray` - Estado neutral

### Alertas (variant)
- `success` - Operación exitosa
- `danger` - Error crítico
- `warning` - Advertencia
- `info` - Información general

## Tamaños

### Botones (size)
- `sm` - Pequeño (px-2 py-1)
- `md` - Mediano (px-4 py-2)
- `lg` - Grande (px-6 py-3)

### Insignias (size)
- `sm` - Pequeña
- `md` - Mediana
- `lg` - Grande

## Ejemplos Completos

### Ejemplo 1: Lista con Paginación
```django
{% load static %}

{% include "components/page-header.html" with 
    title="Asientos Contables"
    subtitle="Listado del libro diario"
    action_label="Nuevo Asiento"
    action_url="..." %}

{% include "components/table.html" with 
    columns=columns
    data=asientos
    empty_message="No hay asientos registrados" %}

{% include "components/pagination.html" with page_obj=page_obj %}
```

### Ejemplo 2: Formulario
```django
{% include "components/card.html" with title="Crear Cuenta" %}
    <form method="post">
        {% csrf_token %}
        {% include "components/form-group.html" with label="Código" field=form.codigo %}
        {% include "components/form-group.html" with label="Nombre" field=form.nombre %}
        {% include "components/form-group.html" with label="Tipo" field=form.tipo %}
        
        <div class="mt-6 flex gap-2">
            {% include "components/button.html" with label="Guardar" variant="success" type="submit" icon="fa-save" %}
            {% include "components/button.html" with label="Cancelar" variant="ghost" %}
        </div>
    </form>
```

### Ejemplo 3: Confirmación
```django
{% include "components/modal.html" with 
    modal_id="delete-modal"
    title="Eliminar Registro"
    show_actions=True
    confirm_label="Eliminar"
    content="¿Está seguro de que desea eliminar este registro?" %}
```

## Notas Importantes

1. **Componentes anidables**: Puedes usar componentes dentro de otros (ej: badge dentro de table)
2. **Flexibilidad**: Todos los parámetros con valores por defecto son opcionales
3. **Consistencia**: Usar componentes asegura coherencia visual en toda la aplicación
4. **Mantenibilidad**: Los cambios de estilos se aplican globalmente
5. **Accesibilidad**: Los componentes incluyen atributos ARIA y semántica HTML correcta

## Clases CSS Disponibles

Los componentes utilizan clases CSS de Tailwind + DaisyUI. Principales:

- `.btn` - Clase base para botones
- `.btn-{variant}` - Variante de color
- `.badge` - Clase base para insignias
- `.alert` - Clase base para alertas
- `.form-group` - Grupo de formulario

Ver `staticfiles/css/` para más detalles sobre estilos.
