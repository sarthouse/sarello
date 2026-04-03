# Setup Inicial - Assets & Development Environment

Guía rápida para configurar el entorno de desarrollo con assets (CSS/JS).

## Prerequisitos

- Python 3.12+
- Node.js 18+ (para npm)
- Git

## Paso 1: Clonar el Repositorio

```bash
git clone <repository-url>
cd sarello
```

## Paso 2: Configurar Python Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

## Paso 3: Instalar Dependencias Python

```bash
pip install -r requirements/local.txt
```

## Paso 4: Instalar Dependencias Node.js

```bash
npm install
```

Esto instala:
- Tailwind CSS
- DaisyUI
- PostCSS
- Autoprefixer

## Paso 5: Configurar Django

```bash
# Crear archivo de variables de entorno
cp .env.example .env
# O usa la configuración de desarrollo
cp .env.development .env
```

Edita `.env` según necesites (cambiar SECRET_KEY, ALLOWED_HOSTS, etc.)

## Paso 6: Configurar Base de Datos

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Paso 7: Compilar Assets (Primera Vez)

```bash
npm run build
```

Esto genera:
- `staticfiles/css/output.css` (CSS compilado)
- `staticfiles/css/theme-output.css` (CSS de tema)

## Paso 8: Iniciar Servidor de Desarrollo

Abre **2 terminales**:

### Terminal 1: Watch CSS (npm dev)
```bash
npm run dev
```

Deja esta terminal ejecutándose. Recompila CSS automáticamente cuando editas archivos.

### Terminal 2: Django Dev Server
```bash
python manage.py runserver
```

Abre http://localhost:8000 en tu navegador.

## Flujo de Desarrollo Diario

### Iniciar sesión de desarrollo

```bash
# Terminal 1: CSS watch
npm run dev

# Terminal 2: Django server (otra terminal)
python manage.py runserver
```

### Editar CSS

1. Edita archivos en `staticfiles/css/`
2. `npm run dev` recompila automáticamente
3. Recarga el navegador

### Editar JavaScript

1. Edita archivos en `staticfiles/js/`
2. Recarga el navegador

### Editar Templates

1. Edita archivos en `templates/`
2. Recarga el navegador

### Editar Python (Modelos, Vistas, etc.)

1. Edita archivos Python
2. Django dev server reinicia automáticamente
3. Recarga el navegador

## Before Committing

Antes de hacer commit y push:

```bash
# Compilar assets para producción (minificar)
npm run build

# Ejecutar tests
pytest

# Verificar código con Ruff
ruff check .
ruff format .

# Hacer commit
git add .
git commit -m "tu mensaje"
```

## Troubleshooting

### "npm: command not found"
- Instala Node.js desde https://nodejs.org/

### "npm install" falla
```bash
# Limpia cache
npm cache clean --force
# Intenta de nuevo
npm install
```

### CSS no aparece en el navegador
```bash
# Asegurate que npm run dev está ejecutándose
# Verifica que templates/base.html incluya output.css
# Recarga el navegador (Ctrl+Shift+Delete para cache)
```

### "module not found" en python
```bash
# Asegurate que venv está activado
# Reinstala dependencias
pip install -r requirements/local.txt
```

### Cambios en CSS no se ven
```bash
# Detén npm run dev
# Limpia archivos compilados
rm staticfiles/css/output.css*
# Reinicia
npm run dev
```

## Estructura de Carpetas Importantes

```
sarello/
├── staticfiles/          # ← Assets en desarrollo (NO en git)
│   ├── css/             # CSS source y compilado
│   └── js/              # JavaScript
├── templates/           # Templates HTML
├── apps/               # Aplicaciones Django
├── static/             # ← Assets compilados para producción (NO en git)
├── manage.py           # Django CLI
├── package.json        # Dependencias npm
├── tailwind.config.js  # Config de Tailwind
└── .env               # Variables de entorno (NO en git)
```

## Recursos Útiles

### Documentación
- [Tailwind CSS](https://tailwindcss.com/docs)
- [DaisyUI](https://daisyui.com/)
- [Django](https://docs.djangoproject.com/)
- [npm Scripts](https://docs.npmjs.com/cli/v8/using-npm/scripts)

### Archivos de Guía
- `ASSETS_README.md` - Guía detallada de assets
- `AGENTS.md` - Convenciones de código
- `README.md` - Configuración general del proyecto

## Próximos Pasos

Una vez que todo funciona:

1. Familiarízate con la estructura en `AGENTS.md`
2. Lee `ASSETS_README.md` para detalles de CSS/JS
3. Comienza con la Fase 2: Extracción de JavaScript

¡Feliz desarrollo! 🚀
