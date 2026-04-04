# Estructura del Proyecto

Mapa de carpetas y qué hace cada módulo de Sarello ERP.

---

## Vista general

```
sarello/
├── apps/                          # Aplicaciones Django
│   ├── base/                      # Modelos base (TimeStampedModel, DocumentoBase)
│   ├── contabilidad/              # Plan de cuentas, asientos, libro diario, mayor, MapeoContable, impuestos
│   ├── tesoreria/                 # Cajas, bancos, movimientos con líneas, conciliación
│   ├── contactos/                 # Clientes y proveedores
│   ├── inventario/                # Productos y stock
│   ├── ventas/                    # Facturación y ventas
│   ├── compras/                   # Órdenes de compra y proveedores
│   ├── manufactura/               # Producción y BOM
│   ├── configuracion/             # Parámetros del sistema, datos de empresa
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
│   ├── base.txt                   # Core: Django, DRF, Celery, Pillow
│   ├── local.txt                  # Dev: Faker, django-extensions, IPython, pytest, ruff
│   └── production.txt             # Prod: Gunicorn, psycopg2
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
- `DocumentoBase`: base para documentos con estados (borrador → confirmado → anulado/cancelado)

### contabilidad
Módulo central del ERP:
- Plan de cuentas (CuentaContable)
- Ejercicios fiscales (Ejercicio)
- Asientos contables (Asiento, LineaAsiento)
- Libro diario y mayor
- Balance y estado de resultados
- Mapeo contable (MapeoContable) — configuración de eventos contables
- Impuestos (TipoImpuesto, Alicuota, ConfiguracionImpuesto) — fusionado desde app `impuestos`

### tesoreria
Gestión de dinero en efectivo y bancos:
- Cuentas de tesorería (CuentaTesoreria) vinculadas a cuentas contables
- Movimientos con líneas (MovimientoTesoreria, LineaMovimientoTesoreria)
- Tipos: cobro, pago, transferencia, ajuste de saldo
- Generación automática de asientos contables al confirmar
- Conciliación de saldos (tesorería vs contabilidad)

### contactos
CRM básico:
- Clientes y proveedores
- Datos fiscales (CUIT, condición IVA)

### configuracion
Settings del sistema:
- Parámetros del sistema (ParametroSistema)
- Datos de la empresa (DatosEmpresa)

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

### integraciones
Conexiones externas:
- AFIP (factura electrónica — Fase 7)
- Otras integraciones futuras

---

## Flujo de datos típico

```
Movimiento de tesorería (confirmar)
    ↓ genera automáticamente
Asiento contable (origen='tesoreria')
    ↓
Libro diario → Mayor → Balance / Estado de resultados

Contacto (cliente/proveedor) → ... → Movimiento de tesorería
                                                    ↓
                                           Asiento contable
                                                    ↓
                                           Estados financieros
```

---

## Ver también

- [Guía de inicio](guia-inicio.md) — Setup del entorno
- [Convenciones de código](convenciones.md) — Cómo escribir código en cada módulo
- [Comandos útiles](comandos.md) — Comandos para trabajar con cada app
- [NIIF en Argentina](niif-argentina.md) — Normas contables aplicables
- [Normas ISO](normas-iso.md) — Estándares de calidad y seguridad
