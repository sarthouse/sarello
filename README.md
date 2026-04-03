# Sarello ERP

Sistema de gestión empresarial (ERP) desarrollado con Django para Argentina.

**Versión:** 0.1.0
**Última actualización:** Abril 2026

---

## Tabla de Contenidos

1. [¿Qué es Sarello?](#qué-es-sarello)
2. [Requisitos previos](#requisitos-previos)
3. [Desarrollo local (Windows/Mac/Linux)](#desarrollo-local-windowsmaclinux)
4. [Producción con Docker](#producción-con-docker)
5. [Solución de problemas](#solución-de-problemas)
6. [Comandos útiles](#comandos-útiles)

---

## ¿Qué es Sarello?

Es un sistema ERP (Enterprise Resource Planning) argentino con:

- Contabilidad completa (plan de cuentas, asientos, libro diario, mayor)
- Tesorería (cajas, bancos, ingresos, egresos)
- Impuestos (IVA, IIBB, retenciones, percepciones)
- Contactos (clientes y proveedores)
- Preparado para factura electrónica AFIP

---

## Requisitos previos

### Si usas Windows:
1. Instalar Python 3.12 desde https://www.python.org/downloads/
   - **IMPORTANTE:** Durante la instalación, marcar "Add Python to PATH"
2. Instalar Git desde https://git-scm.com/

### Si usas Mac:
```bash
# Instalar Homebrew (si no lo tenés)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python
```

### Si usas Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

### Instalar Docker (para producción):
- **Windows/Mac:** Descargar Docker Desktop desde https://www.docker.com/products/docker-desktop
- **Linux:** https://docs.docker.com/engine/install/ubuntu/

---

## Desarrollo local (Windows/Mac/Linux)

### Paso 1: Descargar el proyecto

```bash
# Si tenés Git instalado:
git clone <URL_DEL_REPOSITORIO>
cd sarello

# Si no tenés Git, podés descargar el ZIP desde GitHub
```

### Paso 2: Crear el entorno virtual

```bash
# Windows (en CMD o PowerShell)
python -m venv venv
venv\Scripts\activate

# Mac/Linux (en Terminal)
python3 -m venv venv
source venv/bin/activate
```

**¿Qué es esto?** El entorno virtual es como una "bolsa" separada donde se instalan las librerías del proyecto, sin afectar otras instalaciones de Python.

**Si ves `(venv)` al principio de tu línea de comandos**, ¡ya estás dentro!

### Paso 3: Instalar las librerías

```bash
# Esto instala Django, DRF, pytest, y todas las dependencias
pip install -r requirements/local.txt
```

**Tiempo estimado:** 2-5 minutos (depende de tu conexión a internet).

### Paso 4: Configurar el archivo .env

```bash
# Crear el archivo de configuración
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux
```

Editá el archivo `.env` con un editor de texto (Notepad, VS Code, etc.) y dejalo así:

```env
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Paso 5: Preparar la base de datos

```bash
# Crear las tablas de la base de datos
python manage.py migrate
```

**¿Qué hace esto?** Crea el archivo `db.sqlite3` con todas las tablas necesarias.

### Paso 6: Crear un usuario administrador

```bash
python manage.py createsuperuser
```

Seguí los pasos:
- **Email:** Tu email
- **Password:** Una contraseña segura (mínimo 8 caracteres)

### Paso 7: ¡Arrancar el servidor!

```bash
python manage.py runserver
```

### Paso 8: Acceder al sistema

Abrí tu navegador y escribí:

```
http://localhost:8000
```

**¡Listo!** Ya podés usar el sistema.

---

## Producción con Docker

### ¿Qué es Docker?

Docker es como un "contenedor" que tiene todo lo necesario para que el programa funcione: Python, PostgreSQL, Redis, etc. No importa si tenés Windows, Mac o Linux, el programa correrá igual.

### Paso 1: Instalar Docker

- **Windows/Mac:** Descargar e instalar Docker Desktop desde https://www.docker.com/products/docker-desktop
- **Linux:** `sudo apt install docker.io docker-compose`

**Importante:** Una vez instalado, ejecutar Docker Desktop y esperar a que diga "Docker is running".

**Nota:** El archivo `docker-compose.yml` ya existe en el proyecto. No es necesario crearlo nuevamente.

### Paso 2: Crear archivo .env

```bash
cp .env.example .env    # Mac/Linux
copy .env.example .env  # Windows
```

Editá el archivo `.env` con un editor de texto:

```env
SECRET_KEY=CAMBIAME-POR-UNA-CLAVE-MUY-LARGA-Y-SEGURA
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com
DATABASE_URL=postgres://sarello:sarello123@db:5432/sarello
REDIS_URL=redis://redis:6379/0
```

### Paso 3: Construir y ejecutar

```bash
# En la terminal, desde la carpeta del proyecto
docker-compose up -d --build
```

**Esto puede tardar 5-10 minutos la primera vez** (descarga Python, PostgreSQL, Redis, etc.)

### Paso 4: Configurar la base de datos

```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

### Paso 5: Acceder

Abrí tu navegador y ve a:

```
http://localhost:8000
```

**¡Listo!** El sistema está corriendo en producción con Docker.

---

## Solución de problemas

### "python no se reconoce como comando"

**Windows:** Asegurate de haber marcado "Add Python to PATH" durante la instalación. O ejecutá desde la carpeta donde está Python:

```cmd
C:\Python312\python.exe -m venv venv
```

### "Puerto 8000 ya está en uso"

```bash
# Buscar qué proceso usa el puerto 8000
# Windows:
netstat -ano | findstr :8000

# Mac/Linux:
lsof -i :8000

# O simplemente usar otro puerto:
python manage.py runserver 8001
```

### "Error de conexión a PostgreSQL"

Asegurate de que PostgreSQL esté corriendo:

```bash
# Docker
docker-compose ps
docker-compose logs db
```

### "No puedo acceder desde otra computadora"

Editá `ALLOWED_HOSTS` en `.env`:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100
```

(Reemplazá `192.168.1.100` por la IP de tu computadora)

### "Docker no funciona"

1. Asegurate de tener Docker Desktop instalado y corriendo
2. En Windows, ejecutá Docker Desktop como Administrador
3. En Linux:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

### "Error al hacer migrate"

Si estás en producción con SQLite (no deberías), primero eliminá la base de datos:

```bash
rm db.sqlite3
python manage.py migrate
```

---

## Comandos útiles

### Desarrollo
```bash
# Arrancar servidor
python manage.py runserver

# Crear migraciones (después de cambiar modelos)
python manage.py makemigrations

# Aplicar cambios a la base de datos
python manage.py migrate

# Ver qué migraciones están aplicadas
python manage.py showmigrations

# Consola interactiva de Django
python manage.py shell
```

### Testing y Calidad de Código
```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas de una app específica
pytest apps/contabilidad/

# Ejecutar con reporte de cobertura
pytest --cov=apps

# Verificar código con Ruff
ruff check .

# Auto-corregir con Ruff
ruff check . --fix

# Formatear código
ruff format .
```

### Docker
```bash
# Ver logs
docker-compose logs -f

# Ver qué está corriendo
docker-compose ps

# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Entrar al contenedor
docker-compose exec web bash
```

### Limpieza
```bash
# Eliminar base de datos SQLite (desarrollo)
rm db.sqlite3

# Eliminar entorno virtual
rm -rf venv          # Mac/Linux
rmdir /s /q venv    # Windows
```

---

## Estructura de carpetas

```
sarello/
├── apps/                          # Aplicaciones Django
│   ├── base/                      # Modelos base (TimeStampedModel, DocumentoBase)
│   ├── contabilidad/              # Módulo de contabilidad
│   ├── tesoreria/                 # Módulo de tesorería/cajas
│   ├── impuestos/                 # Módulo de impuestos
│   ├── contactos/                 # Módulo de contactos (clientes/proveedores)
│   ├── inventario/                # Módulo de inventario/productos
│   ├── ventas/                    # Módulo de ventas
│   ├── compras/                   # Módulo de compras
│   ├── manufactura/               # Módulo de manufactura
│   ├── configuracion/             # Módulo de configuración
│   └── integraciones/             # Integraciones (AFIP, etc)
├── core/                          # Configuración de Django
├── templates/                     # Plantillas HTML
├── static/                        # Archivos CSS/JS/imágenes
├── requirements/                  # Dependencias
│   ├── base.txt                   # Dependencias core
│   ├── local.txt                  # Extras de desarrollo
│   └── production.txt             # Dependencias de producción
├── manage.py                      # CLI de Django
├── AGENTS.md                      # Guía de código para agentes y desarrolladores
└── README.md                      # Este archivo
```

---

## Documentación y Guías

- **AGENTS.md** - Guía completa de estilo de código, comandos, y best practices para desarrolladores y agentes de código
- **README.md** - Este archivo (instalación y uso básico)
- **Django Docs** - https://docs.djangoproject.com/

---

## ¿Necesitás ayuda?

1. Revisá **AGENTS.md** para guías de código y best practices
2. Revisá los logs del servidor: `docker-compose logs -f` o `python manage.py runserver`
3. Buscá el error en Google
4. Consultá la documentación de Django: https://docs.djangoproject.com/

---

## Notas técnicas

- **Moneda:** Pesos argentinos (ARS)
- **Decimal:** Siempre usar `DecimalField`, nunca float para dinero
- **Auditoría:** Todos los modelos heredan de `TimeStampedModel` para timestamps automáticos
- **Estados:** Usar `DocumentoBase` para facturas, comprobantes (borrador → confirmado → cancelado)
- **Zona horaria:** America/Argentina/Buenos_Aires
- **AFIP:** Factura electrónica en Fase 7 (futuro)
- **Testing:** Usar pytest con pytest-django (ver AGENTS.md para detalles)

---

**¡Gracias por usar Sarello ERP!**

Última actualización: Abril 2026
