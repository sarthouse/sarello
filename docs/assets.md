# Gestión de Assets (CSS/JS)

Guía para trabajar con los archivos estáticos de Sarello ERP.

---

## Arquitectura

El proyecto usa **PostCSS CLI** como único build tool (no Vite, no Webpack). Las librerías externas se cargan por CDN.

**Build flow:**
```
staticfiles/css/main.css --(postcss-cli)--> staticfiles/css/output.css
```

**CDN (no se bundlean):**
- HTMX 2.0.4
- Alpine.js 3.x + collapse plugin
- Google Fonts — IBM Plex Sans + IBM Plex Mono
- Font Awesome 6.4.0

---

## Estructura de directorios

```
staticfiles/
├── css/
│   ├── main.css                 # Entry point (se compila a output.css)
│   ├── output.css               # Generado por PostCSS — NO editar
│   ├── utilities.css            # Utilidades custom (importado en main.css)
│   ├── components/              # Componentes CSS reutilizables
│   │   ├── alerts.css           # Alertas, toasts, callouts
│   │   ├── buttons.css          # Botones, grupos, loading states
│   │   ├── cards.css            # Cards, stat cards, empty states
│   │   ├── forms.css            # Inputs, selects, checkboxes, currency inputs
│   │   ├── modals.css           # Modales, dialogs, animaciones
│   │   └── tables.css           # Tablas, paginación, estilos contables
│   ├── pages/                   # (vacío — futuro)
│   └── themes/                  # (vacío — futuro)
├── js/
│   ├── app.js                   # Entry point principal (tema, Alpine, HTMX)
│   └── modules/
│       ├── accounting/          # Módulo contabilidad
│       │   ├── index.js         # Entry point del módulo
│       │   ├── asientos.js      # Gestión de líneas de asientos
│       │   ├── balance.js       # Árbol de balance
│       │   ├── estado-resultados.js
│       │   ├── importar-cuentas.js  # Importación CSV
│       │   └── plan-cuentas.js  # Acciones masivas en plan de cuentas
│       ├── forms.js             # FormManager + Validators
│       ├── modals.js            # ModalManager + helpers (showAlert, showConfirm)
│       ├── navigation.js        # DropdownManager, NavbarManager, TabsManager
│       ├── tables.js            # TableManager (sorting, filtering, export CSV)
│       ├── utils.js             # Utilidades + LocalStorage wrapper
│       ├── forms/               # (vacío — futuro)
│       ├── modals/              # (vacío — futuro)
│       ├── navigation/          # (vacío — futuro)
│       ├── tables/              # (vacío — futuro)
│       └── utils/               # (vacío — futuro)
├── images/                      # (vacío — futuro)
└── fonts/                       # (vacío — futuro)
```

> `staticfiles/` = fuente en desarrollo. `static/` = compilado para producción (generado por `collectstatic`, incluye Django admin + DRF assets).

---

## Setup

```bash
# Instalar dependencias
npm install

# Watch mode — recompila CSS al editar
npm run dev

# Compilar para producción (minificar)
npm run build
```

### Dependencias

| Paquete | Versión | Uso |
|---------|---------|-----|
| tailwindcss | ^3.4.0 | Framework CSS utility-first |
| daisyui | ^4.12.24 | Componentes UI (temas dark/light) |
| postcss | ^8.5.8 | Pipeline de transformación CSS |
| postcss-cli | ^11.0.1 | CLI de PostCSS |
| postcss-import | ^16.1.1 | Imports CSS |
| autoprefixer | ^10.4.0 | Vendor prefixes |
| tailwindcss-animate | ^1.0.7 | Animaciones Tailwind |

---

## Build

### postcss.config.js

```js
module.exports = {
  plugins: {
    'postcss-import': {},
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

Pipeline: `postcss-import` → `tailwindcss` → `autoprefixer`

### tailwind.config.js

```js
module.exports = {
  content: [
    './templates/**/*.html',
    './staticfiles/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        accounting: {
          debe: 'var(--accounting-debe)',
          haber: 'var(--accounting-haber)',
          saldo: 'var(--accounting-saldo)',
          activo: 'var(--accounting-activo)',
          pasivo: 'var(--accounting-pasivo)',
          patrimonio: 'var(--accounting-patrimonio)',
          ingreso: 'var(--accounting-ingreso)',
          egreso: 'var(--accounting-egreso)',
        },
      },
      fontFamily: {
        sans: ['IBM Plex Sans', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['IBM Plex Mono', 'monospace'],
      },
    },
  },
  plugins: [
    require('daisyui'),
    require('tailwindcss-animate'),
  ],
  daisyui: {
    themes: [{ dark: { /* tokens */ } }, { light: { /* tokens */ } }],
    defaultTheme: 'dark',
  },
}
```

**Puntos clave:**
- Colores de contabilidad mapeados a CSS custom properties
- Fuente: IBM Plex Sans (sans-serif) + IBM Plex Mono (monospace)
- Tema por defecto: **dark**
- Dos temas DaisyUI: `dark` y `light`

### main.css (Entry Point)

Estructura:
1. Imports de fuentes (Google Fonts CDN) y Font Awesome (CDN)
2. Imports de componentes (`@import './components/*.css'`)
3. `utilities.css` importado
4. Directivas Tailwind (`@tailwind base;`, `@tailwind components;`, `@tailwind utilities;`)
5. CSS custom properties en `:root` (sombras, colores contables, variables de componente)
6. `prefers-reduced-motion` para accesibilidad
7. `[x-cloak]` para Alpine.js

---

## Flujo de desarrollo

### Iniciar sesión de trabajo

```bash
# Terminal 1: CSS watch
npm run dev

# Terminal 2: Django server
python manage.py runserver
```

### Editar CSS

1. Editá `staticfiles/css/main.css` o archivos en `staticfiles/css/components/`
2. `npm run dev` recompila automáticamente a `output.css`
3. Recargá el navegador

### Editar JavaScript

1. Editá archivos en `staticfiles/js/modules/`
2. Recargá el navegador

### Tema (dark/light)

El tema se maneja mediante:
- **DaisyUI** en `tailwind.config.js` (tokens dark/light)
- **CSS custom properties** en `main.css` `:root`
- **JavaScript** en `app.js` (`initThemeToggle()`)
- **Inline script** en `base.html` que lee `localStorage.getItem('theme')`

Para cambiar tema: botón con atributo `data-theme-toggle` (manejado por `app.js`).

---

## Cómo se cargan los assets

En `templates/base.html`:

1. **Google Fonts** — preconnect + stylesheet (IBM Plex Mono + IBM Plex Sans)
2. **CSS compilado** — `{% static 'css/output.css' %}`
3. **HTMX** — CDN script (defer)
4. **Alpine.js** — CDN script + collapse plugin (defer)
5. **App JS** — `{% static 'js/app.js' %}` (defer)
6. **Theme init** — inline script inmediato (antes de DOM parsing, lee `localStorage`)

El `<html>` tiene `data-theme="dark"` por defecto.

---

## JavaScript: API global

`window.Sarello` expone:

| Método | Descripción |
|--------|-------------|
| `apiCall(url, options)` | Fetch wrapper con CSRF |
| `notify(message, type)` | Notificación al usuario |
| `debounce(fn, delay)` | Debounce |
| `throttle(fn, delay)` | Throttle |
| `formatCurrency(amount)` | Formatea como moneda ARS |
| `formatNumber(n)` | Formatea número |
| `parseCurrency(str)` | Parsea string a número |

### Módulos JavaScript

| Módulo | Función |
|--------|---------|
| `forms.js` | `FormManager` (validación, errores, loading) + `Validators` (required, email, number, pattern, etc.) |
| `modals.js` | `ModalManager` + helpers: `showAlert`, `showConfirm`, `showLoading`, `showInput` |
| `navigation.js` | `DropdownManager`, `NavbarManager` (menú mobile), `TabsManager` — auto-inicializa en DOMContentLoaded |
| `tables.js` | `TableManager` — sorting, filtering, selección de filas, export CSV |
| `utils.js` | Utilidades DOM, string helpers, `LocalStorage` wrapper, serialización de formularios |
| `accounting/asientos.js` | `AsientosManager` — gestión de líneas, totales debe/haber, validación de balance |
| `accounting/balance.js` | `BalanceTreeManager` — árbol expandible de balance, búsqueda, persistencia de estado |
| `accounting/estado-resultados.js` | `EstadoResultadosManager` — árbol de resultados, filtro por rango |
| `accounting/importar-cuentas.js` | `ImportarCuentasManager` — importación CSV, preview, validación, descarga template |
| `accounting/plan-cuentas.js` | `PlanCuentasManager` — acciones masivas en plan de cuentas |

---

## Convenciones de nombres

### CSS Classes

Usar clases de Tailwind + DaisyUI directamente. Para custom:

```
.{component}-{modifier}
.btn-primary
.form-control
.table-accounting
```

### CSS Custom Properties

```
--{property}-{variant}
--accounting-debe
--accounting-haber
--shadow-sm
--shadow-md
--shadow-lg
```

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
| Tema no aplicado | Verificá que `<html data-theme="dark">` esté en base.html; limpiá `localStorage` |
| Alpine.js no funciona | Verificá que HTMX y Alpine se cargan antes que `app.js` |

---

## Ver también

- [Guía de inicio](guia-inicio.md) — Setup completo
- [Comandos útiles](comandos.md) — Comandos npm
- [Componentes de template](componentes.md) — Componentes HTML reutilizables
