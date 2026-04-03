# Estructura del Proyecto

Mapa de carpetas y qué hace cada módulo de Sarello ERP.

---

## Vista general

```
sarello/
├── apps/                          # Aplicaciones Django
│   ├── base/                      # Modelos base (TimeStampedModel, DocumentoBase)
│   ├── contabilidad/              # Plan de cuentas, asientos, libro diario, mayor
│   ├── tesoreria/                 # Cajas, bancos, ingresos, egresos
│   ├── impuestos/                 # IVA, IIBB, retenciones, percepciones
│   ├── contactos/                 # Clientes y proveedores
│   ├── inventario/                # Productos y stock
│   ├── ventas/                    # Facturación y ventas
│   ├── compras/                   # Órdenes de compra y proveedores
│   ├── manufactura/               # Producción y BOM
│   ├── configuracion/             # Settings del sistema
│   └── integraciones/             # AFIP, factura electrónica
├── core/                          # Configuración de Django (settings, urls, wsgi)
├── templates/                     # Plantillas HTML
│   ├── components/                # Componentes reutilizables (ver [Componentes](componentes.md))
│   └── ...                        # Plantillas por app
├── staticfiles/                   # Assets en desarrollo (fuente)
│   ├── css/                       # CSS: main.css, theme.css, components/
│   ├── js/                        # JavaScript: app.js, modules/
│   ├── images/                    # Iconos, logos, fondos
│   └── fonts/                     # Fuentes locales
├── static/                        # Assets compilados para producción (generado)
├── docs/                          # Documentación del proyecto
├── requirements/                  # Dependencias de Python
│   ├── base.txt                   # Core: Django, DRF, Celery, Pillow, pytest
│   ├── local.txt                  # Dev: Faker, django-extensions, IPython
│   └── production.txt             # Prod: Gunicorn, psycopg2, Ruff
├── manage.py                      # CLI de Django
├── AGENTS.md                      # Guía de código para agentes de IA
├── README.md                      # Entrada principal del proyecto
└── package.json                   # Dependencias de Node.js
```

---

## Módulos (apps/)

### base
Modelos abstractos que heredan todas las demás apps:
- `TimeStampedModel`: campos automáticos `creado_en` y `modificado_en`
- `DocumentoBase`: base para facturas y comprobantes con estados (borrador → confirmado → cancelado)

### contabilidad
Módulo central del ERP:
- Plan de cuentas (CuentaContable)
- Ejercicios fiscales (Ejercicio)
- Asientos contables (Asiento, LineaAsiento)
- Libro diario y mayor

### tesoreria
Gestión de dinero en efectivo y bancos:
- Cajas y cuentas bancarias (CuentaTesoreria)
- Movimientos de ingreso/egreso (MovimientoTesoreria)

### impuestos
Impuestos argentinos:
- IVA, IIBB, retenciones, percepciones
- Preparado para integración AFIP

### contactos
CRM básico:
- Clientes
- Proveedores

### inventario
Gestión de productos:
- Productos y variantes
- Stock y movimientos

### ventas
Proceso de venta:
- Presupuestos
- Pedidos de venta
- Facturación

### compras
Proceso de compra:
- Órdenes de compra
- Recepción de mercadería

### manufactura
Producción:
- Órdenes de fabricación
- Listas de materiales (BOM)

### configuracion
Settings del sistema:
- Configuración general
- Parámetros del ERP

### integraciones
Conexiones externas:
- AFIP (factura electrónica — Fase 7)
- Otras integraciones futuras

---

## Flujo de datos típico

```
Contacto (cliente) → Venta → Factura → Asiento contable → Movimiento de tesorería
                                                    ↓
                                               Impuesto (IVA)
```

---

## Ver también

- [Guía de inicio](guia-inicio.md) — Setup del entorno
- [Convenciones de código](convenciones.md) — Cómo escribir código en cada módulo
- [Comandos útiles](comandos.md) — Comandos para trabajar con cada app
