# Sarello ERP - Assets Management Guide

## Overview

Los assets (CSS y JavaScript) se encuentran en la carpeta `staticfiles/` durante el desarrollo. Para producción, se copian a `static/` usando `python manage.py collectstatic`.

## Estructura de Directorios

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
│   ├── output.css               # ⚠️ Generado - NO editar
│   ├── theme-output.css         # ⚠️ Generado - NO editar
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
    └── ... (fuentes locales si se usan)
```

## Setup Inicial

### 1. Instalar Dependencias

```bash
npm install
```

Esto instala:
- Tailwind CSS 3.4
- DaisyUI 4.7
- PostCSS y Autoprefixer

### 2. Iniciar Watch Mode (Desarrollo)

```bash
npm run dev
```

Esto compila CSS automáticamente cada vez que editas `main.css` o `theme.css`.

**Deja esta terminal corriendo** mientras desarrollas.

### 3. Iniciar Django

En otra terminal:

```bash
python manage.py runserver
```

## Flujo de Desarrollo

### Editar CSS

1. **Edita** `staticfiles/css/main.css` o cualquier archivo en `staticfiles/css/components/`
2. **npm run dev** recompila automáticamente a `output.css`
3. **Recarga** el navegador para ver cambios

### Editar JavaScript

1. **Crea o edita** archivos en `staticfiles/js/modules/`
2. **El navegador recargará automáticamente** si usas LiveReload o Django Dev Server
3. **Los cambios son inmediatos** (sin compilación necesaria)

### Editar Tema

Para compilar solo el tema:

```bash
npm run build:theme
```

Esto genera `theme-output.css` con los estilos del tema.

## Compilación para Producción

```bash
npm run build
```

Esto minifica CSS y prepara para producción. Genera:
- `staticfiles/css/output.css` (minificado)
- `staticfiles/css/output.css.map` (source map)

Luego ejecuta:

```bash
python manage.py collectstatic
```

Esto copia los assets a la carpeta `static/` para servir en producción.

## Estructura de CSS

### main.css (Entry Point Principal)

Importa en este orden:
1. Tailwind directives (@tailwind)
2. Componentes custom
3. Temas y variables
4. Utilities

### theme.css (Tema Separado)

Contiene estilos específicos del tema:
- Paleta de colores del tema
- Colores de contabilidad (debe, haber, etc.)
- Estilos para modo oscuro
- Estilos de impresión

**Ventaja:** Puedes compilar y actualizar temas sin recompilar todo.

### components/*.css

Estilos reutilizables para:
- Botones (buttons.css)
- Formularios (forms.css)
- Tablas (tables.css)
- Tarjetas (cards.css)
- Modales (modals.css)
- Alertas (alerts.css)

**Convención:** Usar clases prefijadas (ej: `.btn-`, `.form-`, `.table-`)

### utilities.css

Utilidades custom que extienden Tailwind:
- Helpers de flexbox/grid
- Utilidades de texto
- Estados (loading, disabled, etc.)
- Utilidades de accesibilidad

## Convenciones de Nombres

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
staticfiles/js/modules/accounting/balance.js
```

### Variables CSS (CSS Custom Properties)

```
--{property}-{variant}
--primary
--primary-light
--primary-dark
--accounting-debe
--space-4
--radius-md
```

## Tailwind CSS Configuration

Archivo: `tailwind.config.js`

**Configuración actual:**
- Theme colors: Colores primarios, secundarios, accounting
- DaisyUI: Habilitado con temas light y dark
- Content scanning: Templates y JS modules

Para agregar nuevas clases:

1. Abre `tailwind.config.js`
2. En `theme.extend`:
   ```js
   colors: {
     'tu-color': '#hexcode',
   },
   ```
3. Reinicia `npm run dev`

## Troubleshooting

### CSS no se actualiza

```bash
# Detén npm run dev
# Limpia la caché
rm staticfiles/css/output.css*
# Reinicia
npm run dev
```

### Tailwind classes no funcionan

1. Verifica que el archivo esté en `staticfiles/css/`
2. Verifica que el path esté en `tailwind.config.js` content
3. Reinicia `npm run dev`

### Tema no aplicado

1. Asegurate que `theme-output.css` se carga en `base.html`
2. Verifica que `<html data-theme="light">` esté en el HTML
3. Reinicia el servidor Django

## Performance

### Tamaño de Assets

- **output.css** (~50KB sin minificar, ~15KB minificado)
- **theme-output.css** (~8KB sin minificar, ~3KB minificado)
- **app.js** (~2KB)

### Lazy Loading

Los módulos JavaScript se cargan bajo demanda:
- Scripts accounting solo se cargan si `data-module="accounting"`
- Reduce tamaño inicial del bundle

## Próximos Pasos (Fase 2)

1. **Extracción de JavaScript:** Mover código inline a módulos
2. **Componentes Django:** Crear templates reutilizables
3. **Optimización:** Minificación de JavaScript, lazy loading

## Recursos

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [DaisyUI Components](https://daisyui.com/)
- [PostCSS](https://postcss.org/)
- [npm Scripts](https://docs.npmjs.com/cli/v8/using-npm/scripts)

## Soporte

Para problemas o preguntas:
1. Revisa esta guía
2. Consulta AGENTS.md para convenciones de código
3. Abre un issue en el repositorio
