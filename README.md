# Sarello ERP

Sistema de gestión empresarial (ERP) desarrollado con Django para Argentina.

**Versión:** 0.1.0 · **Última actualización:** Abril 2026

---

## ¿Qué es Sarello?

ERP argentino con:

- Contabilidad completa (plan de cuentas, asientos, libro diario, mayor)
- Tesorería (cajas, bancos, ingresos, egresos)
- Impuestos (IVA, IIBB, retenciones, percepciones)
- Contactos (clientes y proveedores)
- Preparado para factura electrónica AFIP

---

## Documentación

| Para... | Leé... |
|---------|--------|
| Empezar a desarrollar | [Guía de inicio](docs/guia-inicio.md) |
| Ver la estructura del proyecto | [Estructura](docs/estructura.md) |
| Comandos de Django, pytest, Docker | [Comandos útiles](docs/comandos.md) |
| Trabajar con CSS/JS (Tailwind, DaisyUI) | [Gestión de assets](docs/assets.md) |
| Componentes de template reutilizables | [Componentes](docs/componentes.md) |
| Convenciones de código y estilo | [Convenciones](docs/convenciones.md) |
| Deploy en producción | [Docker](docs/docker.md) |
| Resolver problemas comunes | [Troubleshooting](docs/troubleshooting.md) |

> Todas las guías están en [docs/](docs/index.md).

---

## Inicio rápido

```bash
# 1. Clonar y entrar
git clone <URL_DEL_REPOSITORIO>
cd sarello

# 2. Entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements/local.txt
npm install

# 4. Configurar
cp .env.example .env

# 5. Base de datos
python manage.py migrate
python manage.py createsuperuser

# 6. Compilar assets (primera vez)
npm run build

# 7. Iniciar (2 terminales)
npm run dev                  # Terminal 1: CSS watch
python manage.py runserver   # Terminal 2: Django
```

Abrí http://localhost:8000

> Instrucciones detalladas: [Guía de inicio](docs/guia-inicio.md)

---

## Notas técnicas

- **Moneda:** Pesos argentinos (ARS)
- **Decimal:** Siempre `DecimalField`, nunca float para dinero
- **Auditoría:** Todos los modelos heredan de `TimeStampedModel`
- **Zona horaria:** America/Argentina/Buenos_Aires
- **AFIP:** Factura electrónica en Fase 7
- **Testing:** pytest con pytest-django

---

## ¿Necesitás ayuda?

1. [Troubleshooting](docs/troubleshooting.md) — Problemas comunes
2. [Comandos útiles](docs/comandos.md) — Todos los comandos
3. [Django Docs](https://docs.djangoproject.com/)
