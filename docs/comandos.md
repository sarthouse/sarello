# Comandos Útiles

Todos los comandos que vas a necesitar para trabajar con Sarello ERP.

---

## Django

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# Crear migraciones (después de cambiar modelos)
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate

# Ver qué migraciones están aplicadas
python manage.py showmigrations

# Consola interactiva de Django
python manage.py shell

# Crear usuario administrador
python manage.py createsuperuser

# Recopilar archivos estáticos (producción)
python manage.py collectstatic --noinput
```

## Testing

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con salida detallada
pytest -v

# Ejecutar pruebas de una app específica
pytest apps/contabilidad/

# Ejecutar un archivo de pruebas específico
pytest apps/contabilidad/tests.py

# Ejecutar una clase de pruebas específica
pytest apps/contabilidad/tests.py::MiClaseTest

# Ejecutar un método de prueba específico
pytest apps/contabilidad/tests.py::MiClaseTest::test_metodo_nombre

# Ejecutar con reporte de cobertura
pytest --cov=apps
```

## Calidad de código (Ruff)

```bash
# Verificar código
ruff check .

# Auto-corregir problemas
ruff check . --fix

# Formatear código
ruff format .
```

## Assets (npm)

```bash
# Instalar dependencias
npm install

# Watch mode (desarrollo — recompila CSS al editar)
npm run dev

# Compilar para producción (minificar)
npm run build

# Compilar solo el tema
npm run build:theme
```

## Docker

```bash
# Construir y ejecutar (producción)
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f

# Ver qué está corriendo
docker-compose ps

# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Entrar al contenedor web
docker-compose exec web bash

# Ejecutar migraciones en Docker
docker-compose exec web python manage.py migrate

# Crear superusuario en Docker
docker-compose exec web python manage.py createsuperuser
```

## Limpieza

```bash
# Eliminar base de datos SQLite (desarrollo)
rm db.sqlite3          # Mac/Linux
del db.sqlite3         # Windows (CMD)
Remove-Item db.sqlite3 # Windows (PowerShell)

# Eliminar entorno virtual
rm -rf venv            # Mac/Linux
rmdir /s /q venv       # Windows (CMD)

# Limpiar archivos compilados de CSS
rm staticfiles/css/output.css*

# Limpiar cache de npm
npm cache clean --force

# Limpiar cache de Python
find . -type d -name __pycache__ -exec rm -rf {} +  # Mac/Linux
find . -type f -name "*.pyc" -delete
```

---

## Ver también

- [Guía de inicio](guia-inicio.md) — Setup completo
- [Deploy con Docker](docker.md) — Configuración de producción
- [Troubleshooting](troubleshooting.md) — Problemas comunes
