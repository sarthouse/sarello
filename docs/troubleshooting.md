# Troubleshooting

Problemas comunes y cómo resolverlos.

---

## Python y Django

### "python no se reconoce como comando"

**Windows:** Marcá "Add Python to PATH" durante la instalación. O ejecutá:

```cmd
C:\Python312\python.exe -m venv venv
```

### "Puerto 8000 ya está en uso"

```bash
# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000

# O usá otro puerto
python manage.py runserver 8001
```

### "module not found" en Python

```bash
# Verificá que el venv está activado
pip install -r requirements/local.txt
```

### "Error al hacer migrate"

En desarrollo, podés eliminar la base de datos y empezar de nuevo:

```bash
rm db.sqlite3
python manage.py migrate
```

---

## Assets (CSS/JS)

### CSS no aparece en el navegador

1. Verificá que `npm run dev` está corriendo
2. Verificá que `templates/base.html` incluye `output.css`
3. Forzá recarga del navegador (Ctrl+Shift+R / Cmd+Shift+R)

### Cambios en CSS no se ven

```bash
# Detené npm run dev
# Limpiá archivos compilados
rm staticfiles/css/output.css*
# Reiniciá
npm run dev
```

### Tailwind classes no funcionan

1. Verificá que el archivo esté en `staticfiles/css/`
2. Verificá que el path esté en `tailwind.config.js` content
3. Reiniciá `npm run dev`

### Tema no aplicado

1. Verificá que `theme-output.css` se carga en `base.html`
2. Verificá que `<html data-theme="light">` está en el HTML
3. Reiniciá el servidor Django

---

## Node.js / npm

### "npm: command not found"

Instalá Node.js desde https://nodejs.org/

### "npm install" falla

```bash
npm cache clean --force
npm install
```

---

## Docker

### Docker no funciona

1. Verificá que Docker Desktop está instalado y corriendo
2. En Windows, ejecutalo como Administrador
3. En Linux:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

### Error de conexión a PostgreSQL

```bash
docker-compose ps
docker-compose logs db
```

### No puedo acceder desde otra computadora

Editá `ALLOWED_HOSTS` en `.env`:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100
```

(Reemplazá `192.168.1.100` por la IP de tu computadora)

---

## Ver también

- [Guía de inicio](guia-inicio.md) — Setup completo
- [Deploy con Docker](docker.md) — Configuración de producción
- [Gestión de assets](assets.md) — Soluciones de CSS/JS
