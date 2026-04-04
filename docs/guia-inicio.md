# Guía de Inicio Rápido

Configuración completa del entorno de desarrollo de Sarello ERP.

---

## Prerequisitos

| Herramienta | Versión | Para qué |
|-------------|---------|----------|
| Python | 3.12+ | Backend Django |
| Node.js | 18+ | Assets (Tailwind CSS, DaisyUI) |
| Git | Cualquiera | Control de versiones |
| Docker | Opcional | Producción (ver [Deploy con Docker](docker.md)) |

### Instalar prerequisitos

**Windows:**
1. Python 3.12 desde https://www.python.org/downloads/ — marcar **"Add Python to PATH"**
2. Git desde https://git-scm.com/
3. Node.js desde https://nodejs.org/

**Mac:**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python node git
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git nodejs npm
```

---

## Paso a paso

### 1. Clonar el proyecto

```bash
git clone <URL_DEL_REPOSITORIO>
cd sarello
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> Si ves `(venv)` al inicio de tu terminal, ya está activado.

### 3. Instalar dependencias de Python

```bash
pip install -r requirements/local.txt
```

### 4. Instalar dependencias de Node.js

```bash
npm install
```

Esto instala Tailwind CSS, DaisyUI, PostCSS y Autoprefixer.

### 5. Configurar variables de entorno

```bash
# Windows
copy .env.example .env
# Mac/Linux
cp .env.example .env
```

Editá `.env`:
```env
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Configurar base de datos

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 7. Compilar assets (primera vez)

```bash
npm run build
```

Genera `staticfiles/css/output.css` y `staticfiles/css/theme-output.css`.

### 8. Iniciar servidores de desarrollo

Necesitás **2 terminales**:

**Terminal 1 — Watch de CSS:**
```bash
npm run dev
```
Recompila CSS automáticamente al editar archivos. Dejala corriendo.

**Terminal 2 — Django:**
```bash
python manage.py runserver
```

Abrí http://localhost:8000 en tu navegador.

---

## Flujo de desarrollo diario

### Iniciar sesión de trabajo

```bash
# Terminal 1: CSS watch
npm run dev

# Terminal 2: Django server
python manage.py runserver
```

### Editar archivos

| Qué editás | Dónde | Qué pasa |
|------------|-------|----------|
| CSS | `staticfiles/css/` | `npm run dev` recompila automáticamente |
| JavaScript | `staticfiles/js/` | Recargá el navegador |
| Templates | `templates/` | Recargá el navegador |
| Python | `apps/` | Django reinicia automáticamente |

### Antes de commitear

```bash
# Compilar assets para producción
npm run build

# Ejecutar tests (infraestructura lista, tests por escribir)
pytest

# Verificar y formatear código
ruff check .
ruff format .

# Commit
git add .
git commit -m "tu mensaje"
```

---

## Ver también

- [Comandos útiles](comandos.md) — Django, pytest, Docker, npm, Ruff
- [Gestión de assets](assets.md) — Tailwind, DaisyUI, estructura CSS/JS
- [Troubleshooting](troubleshooting.md) — Problemas comunes
- [Deploy con Docker](docker.md) — Producción
