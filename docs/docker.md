# Deploy con Docker

Guía para ejecutar Sarello ERP en producción con Docker.

---

## Prerequisitos

- Docker y Docker Compose instalados
- Archivo `docker-compose.yml` existente en el proyecto

### Instalar Docker

- **Windows/Mac:** Docker Desktop desde https://www.docker.com/products/docker-desktop
- **Linux:** `sudo apt install docker.io docker-compose`

Una vez instalado, ejecutá Docker Desktop y esperá a que diga "Docker is running".

---

## Configuración

### 1. Crear archivo .env

```bash
# Windows
copy .env.example .env
# Mac/Linux
cp .env.example .env
```

Editá `.env` para producción:

```env
SECRET_KEY=CAMBIAME-POR-UNA-CLAVE-MUY-LARGA-Y-SEGURA
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,tu-dominio.com
DATABASE_URL=postgres://sarello:sarello123@db:5432/sarello
REDIS_URL=redis://redis:6379/0
```

### 2. Construir y ejecutar

```bash
docker-compose up -d --build
```

> La primera vez tarda 5-10 minutos (descarga Python, PostgreSQL, Redis, etc.)

### 3. Configurar base de datos

```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

### 4. Acceder

Abrí http://localhost:8000 en tu navegador.

---

## Comandos de Docker

| Comando | Descripción |
|---------|-------------|
| `docker-compose up -d --build` | Construir y ejecutar |
| `docker-compose logs -f` | Ver logs en tiempo real |
| `docker-compose ps` | Ver qué está corriendo |
| `docker-compose restart` | Reiniciar servicios |
| `docker-compose down` | Detener todo |
| `docker-compose exec web bash` | Entrar al contenedor |
| `docker-compose exec web python manage.py migrate` | Migrar en Docker |
| `docker-compose exec web python manage.py createsuperuser` | Crear admin en Docker |

---

## Arquitectura Docker

El stack incluye:
- **web:** Aplicación Django con Gunicorn
- **db:** PostgreSQL (producción)
- **redis:** Redis para cache y Celery

---

## Troubleshooting

| Problema | Solución |
|----------|----------|
| Docker no arranca | Verificá que Docker Desktop esté corriendo. En Windows, ejecutalo como Administrador |
| Linux Docker | `sudo systemctl start docker && sudo systemctl enable docker` |
| Error de PostgreSQL | `docker-compose ps` y `docker-compose logs db` para ver el estado |
| No accesible desde otra PC | Agregá la IP a `ALLOWED_HOSTS` en `.env` |

---

## Ver también

- [Guía de inicio](guia-inicio.md) — Desarrollo local sin Docker
- [Comandos útiles](comandos.md) — Todos los comandos de Docker
- [Troubleshooting](troubleshooting.md) — Problemas comunes
