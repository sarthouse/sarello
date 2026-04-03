# Gestión de Assets (CSS/JS)

Guía para trabajar con los archivos estáticos de Sarello ERP.

---

## Estructura de directorios

```
staticfiles/
├── js/
│   ├── app.js                    # Entry point principal
│   ├── modules/
│   │   ├── accounting/          # Módulo contabilidad
│   │   ├── forms.js
│   │   ├── tables.js
│   │   ├── modals.js
│   │   ├── navigation.js
│   │   └── utils.js
│   ├── lib/                     # Librerías externas
│   └── vendor/                  # Código de terceros
├── css/
│   ├── main.css                 # Entry point (se compila a output.css)
│   ├── theme.css                # Tema específico (se compila a theme-output.css)
│   ├── output.css               # Generado — NO editar
│   ├── theme-output.css         # Generado — NO editar
│   ├── components/
│   │   ├── buttons.css
│   │   ├── forms.css
│   │   ├── tables.css
│   │   ├── cards.css
│   │   ├── modals.css
│   │   └── alerts.css
│   ├── pages/
│   ├── themes/
│   │   └── variables.css        # CSS custom properties
│   └── utilities.css
├── images/
│   ├── icons/
│   ├── logos/
│   └── backgrounds/
└── fonts/
```

> `staticfiles/` = fuente en desarrollo. `static/` = compilado para producción (generado por `collectstatic`).

---

## Setup

```bash
# Instalar dependencias (Tailwind CSS 3.4, DaisyUI 4.7, PostCSS, Autoprefixer)
npm install

# Watch mode — recompila CSS al editar
npm run dev

# Compilar para producción (minificar)
npm run build

# Compilar solo el tema
npm run build:theme
```

---

## Flujo de desarrollo

### Editar CSS

1. Editá `staticfiles/css/main.css` o archivos en `staticfiles/css/components/`
2. `npm run dev` recompila automáticamente a `output.css`
3. Recargá el navegador

### Editar JavaScript

1. Creá o editá archivos en `staticfiles/js/modules/`
2. Recargá el navegador

### Editar tema

1. Editá `staticfiles/css/theme.css`
2. `npm run build:theme` regenera `theme-output.css`

---

## Estructura de CSS

### main.css (Entry Point)

Importa en este orden:
1. Tailwind directives (`@tailwind`)
2. Componentes custom
3. Temas y variables
4. Utilities

### theme.css (Tema separado)

Contiene:
- Paleta de colores del tema
- Colores de contabilidad (debe, haber, etc.)
- Estilos para modo oscuro
- Estilos de impresión

**Ventaja:** Podés compilar y actualizar temas sin recompilar todo.

### components/*.css

Estilos reutilizables para botones, formularios, tablas, tarjetas, modales, alertas.

**Convención:** Usar clases prefijadas (ej: `.btn-`, `.form-`, `.table-`)

### utilities.css

Utilidades custom que extienden Tailwind: helpers de flexbox/grid, utilidades de texto, estados (loading, disabled), accesibilidad.

---

## Convenciones de nombres

### CSS Classes

```
.{component}-{modifier}
.btn-primary
.form-control
.table-accounting
.alert-success
.card-stat
```

### JavaScript Modules

```
staticfiles/js/modules/{feature}/{functionality}.js
staticfiles/js/modules/accounting/asientos.js
staticfiles/js/modules/forms.js
```

### CSS Custom Properties

```
--{property}-{variant}
--primary
--primary-light
--primary-dark
--accounting-debe
--space-4
--radius-md
```

---

## Tailwind CSS Configuration

Archivo: `tailwind.config.js`

**Configuración actual:**
- Theme colors: primarios, secundarios, accounting
- DaisyUI: habilitado con temas light y dark
- Content scanning: templates y JS modules

Para agregar nuevos colores:

```js
// tailwind.config.js
theme: {
  extend: {
    colors: {
      'tu-color': '#hexcode',
    },
  },
}
```

Luego reiniciá `npm run dev`.

---

## Producción

```bash
# 1. Compilar assets (minificar)
npm run build

# 2. Copiar a carpeta de producción
python manage.py collectstatic
```

---

## Troubleshooting

| Problema | Solución |
|----------|----------|
| CSS no se actualiza | Detené `npm run dev`, borrá `staticfiles/css/output.css*`, reiniciá |
| Tailwind classes no funcionan | Verificá que el path esté en `tailwind.config.js` content |
| Tema no aplicado | Verificá que `theme-output.css` se carga en `base.html` y que `<html data-theme="light">` está presente |

---

## Performance

| Asset | Sin minificar | Minificado |
|-------|---------------|------------|
| output.css | ~50KB | ~15KB |
| theme-output.css | ~8KB | ~3KB |
| app.js | ~2KB | — |

Los módulos JavaScript se cargan bajo demanda (solo si `data-module="accounting"`).

---

## Ver también

- [Guía de inicio](guia-inicio.md) — Setup completo
- [Comandos útiles](comandos.md) — Comandos npm
- [Componentes de template](componentes.md) — Componentes HTML reutilizables
