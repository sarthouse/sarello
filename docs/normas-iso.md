# Normas ISO aplicables a Sarello ERP

## Introducción

Las normas **ISO (International Organization for Standardization)** establecen estándares internacionales para procesos, sistemas y productos. Para un sistema ERP como Sarello, varias normas ISO son relevantes tanto en el desarrollo del software como en la operación del negocio que el sistema soporta.

Este documento identifica las normas ISO aplicables, su alcance, y cómo Sarello se posiciona respecto a cada una.

---

## ISO/IEC 27001 — Seguridad de la información

**Qué regula:** Sistema de Gestión de Seguridad de la Información (SGSI). Establece requisitos para establecer, implementar, mantener y mejorar continuamente la seguridad de la información.

**Controles principales:**
- Gestión de accesos y autenticación
- Cifrado de datos en tránsito y en reposo
- Gestión de incidentes de seguridad
- Copias de seguridad y recuperación
- Control de cambios
- Auditoría y logging

**Estado en Sarello:**
- ✅ Autenticación con Django Allauth
- ✅ Control de acceso por roles y permisos (`@permission_required`)
- ✅ HTTPS en producción (configurable)
- ✅ Registro de auditoría (campos `creado_en`, `modificado_en` en todos los modelos)
- ❌ Cifrado de datos sensibles en base de datos
- ❌ Gestión formal de incidentes
- ❌ Política de retención y eliminación de datos
- ❌ Log de accesos y acciones de usuario

**Relevancia para el proyecto:** Crítico. Sarello maneja datos financieros sensibles, información fiscal (CUIT, CUIL), y datos de contacto. La seguridad es un requisito legal bajo la Ley 25.326 de Protección de Datos Personales.

---

## ISO 9001 — Gestión de la calidad

**Qué regula:** Sistema de Gestión de Calidad (SGC). Enfoque en procesos, mejora continua y satisfacción del cliente.

**Principios clave:**
- Enfoque al cliente
- Liderazgo
- Compromiso del personal
- Enfoque basado en procesos
- Mejora continua
- Toma de decisiones basada en evidencia
- Gestión de las relaciones

**Estado en Sarello:**
- ✅ Documentación técnica completa (`docs/`)
- ✅ Convenciones de código (`AGENTS.md`, `convenciones.md`)
- ✅ Testing con pytest (estructura preparada)
- ✅ Control de versiones con Git
- ❌ Métricas de calidad del software
- ❌ Gestión formal de requisitos
- ❌ Revisiones de código sistemáticas
- ❌ Medición de satisfacción del usuario

**Relevancia para el proyecto:** Fundamental para garantizar que el ERP cumpla con las expectativas del usuario y los estándares de la industria contable.

---

## ISO 15489 — Gestión de documentos

**Qué regula:** Principios y requisitos para la gestión de documentos de archivo, tanto digitales como físicos.

**Requisitos clave:**
- Autenticidad: el documento es lo que dice ser
- Integridad: el documento está completo y sin alteraciones
- Fiabilidad: el documento refleja las transacciones que dice reflejar
- Usabilidad: el documento puede ser localizado, recuperado y utilizado
- Retención: períodos de conservación definidos
- Disposición: eliminación controlada al fin del período

**Estado en Sarello:**
- ✅ Trazabilidad de documentos contables (origen → asiento → estado financiero)
- ✅ Estados de documento (borrador → confirmado → anulado/cancelado)
- ✅ Inmutabilidad de asientos confirmados (no se pueden modificar)
- ✅ Anulación con asiento inverso (traza completa)
- ✅ Timestamps automáticos (`creado_en`, `modificado_en`)
- ❌ Períodos de retención configurables
- ❌ Firma digital de documentos
- ❌ Exportación a formatos de archivo (PDF/A)
- ❌ Política de eliminación al fin del período legal

**Relevancia para el proyecto:** Directa. Sarello genera documentos contables (asientos, libros, estados financieros) que son documentos de archivo con validez legal. La AFIP exige conservación por 10 años (Ley 11.683).

---

## ISO/IEC 20000 — Gestión de servicios de TI

**Qué regula:** Sistema de Gestión de Servicios de TI (SGSTI). Establece requisitos para la prestación de servicios de TI.

**Áreas principales:**
- Gestión de nivel de servicio (SLA)
- Gestión de disponibilidad
- Gestión de capacidad
- Gestión de continuidad del servicio
- Gestión de incidentes y problemas
- Gestión de cambios y configuraciones

**Estado en Sarello:**
- ✅ Docker para despliegue reproducible
- ✅ Configuración separada por entorno (local/producción)
- ✅ PostgreSQL + Redis en producción
- ❌ Monitoreo de disponibilidad
- ❌ Gestión de capacidad
- ❌ Plan de recuperación ante desastres
- ❌ SLA definidos

**Relevancia para el proyecto:** Importante si Sarello se ofrece como servicio (SaaS). Para uso interno, los requisitos son menores pero la disponibilidad sigue siendo crítica para operaciones contables.

---

## ISO 22301 — Continuidad del negocio

**Qué regula:** Sistema de Gestión de Continuidad del Negocio (SGCN). Preparación, respuesta y recuperación ante interrupciones.

**Requisitos clave:**
- Análisis de impacto en el negocio (BIA)
- Estrategias de continuidad
- Plan de respuesta ante incidentes
- Pruebas y ejercicios
- Mejora continua

**Estado en Sarello:**
- ✅ Base de datos con backups (PostgreSQL)
- ✅ Docker compose para recreación rápida
- ❌ Backups automatizados programados
- ❌ Plan de recuperación documentado
- ❌ Pruebas de recuperación
- ❌ Sitio de contingencia

**Relevancia para el proyecto:** Crítico para producción. La pérdida de datos contables puede tener consecuencias legales y financieras graves.

---

## ISO/IEC 25010 — Calidad del producto de software

**Qué regula:** Modelo de calidad para productos de software. Define 8 características de calidad.

**Características:**

| Característica | Qué evalúa | Estado en Sarello |
|---------------|-----------|-------------------|
| **Adecuación funcional** | Funcionalidad completa y correcta | ✅ Modelos contables completos, ❌ módulos operativos vacíos |
| **Eficiencia de rendimiento** | Tiempo de respuesta, uso de recursos | ⚠️ N+1 queries corregidos, ❌ sin profiling |
| **Compatibilidad** | Coexistencia e interoperabilidad | ✅ API REST (DRF), ⚠️ sin integración AFIP |
| **Usabilidad** | Reconocibilidad, aprendibilidad, operabilidad | ✅ Templates con componentes, ⚠️ sin tests de usuario |
| **Fiabilidad** | Madurez, disponibilidad, tolerancia a fallos | ✅ Validaciones de modelo, ⚠️ sin manejo de errores global |
| **Seguridad** | Confidencialidad, integridad, autenticidad | ✅ Auth y permisos, ❌ sin cifrado de datos sensibles |
| **Mantenibilidad** | Modularidad, reusabilidad, analizabilidad, modificabilidad | ✅ Apps separadas, componentes, ❌ sin cobertura de tests |
| **Portabilidad** | Adaptabilidad, instalabilidad, reemplazabilidad | ✅ Django multiplataforma, Docker |

**Relevancia para el proyecto:** Marco de referencia para evaluar y mejorar la calidad del software de forma sistemática.

---

## ISO 8000 — Calidad de datos

**Qué regula:** Requisitos de calidad de datos para intercambio y uso de información.

**Dimensiones de calidad:**
- Exactitud: los datos reflejan la realidad
- Completitud: todos los datos necesarios están presentes
- Consistencia: los datos no se contradicen entre sistemas
- Actualidad: los datos están actualizados
- Validez: los datos cumplen con las reglas de negocio

**Estado en Sarello:**
- ✅ Validaciones de modelo (`clean()`, `DecimalField`, `ForeignKey`)
- ✅ Conciliación de saldos (tesorería vs contabilidad)
- ✅ Tipos de datos correctos (Decimal para dinero, Date para fechas)
- ✅ Zona horaria configurada (America/Argentina/Buenos_Aires)
- ❌ Validación de CUIT/CUIL (algoritmo módulo 11)
- ❌ Detección de duplicados
- ❌ Auditoría de cambios en datos críticos
- ❌ Gobernanza de datos maestra

**Relevancia para el proyecto:** Directa. Los datos contables incorrectos generan estados financieros erróneos con consecuencias legales.

---

## Normas argentinas complementarias

### Ley 25.326 — Protección de Datos Personales

**Qué regula:** Tratamiento de datos personales en bases de datos públicas y privadas.

**Requisitos clave:**
- Consentimiento del titular
- Derecho de acceso, rectificación y supresión
- Inscripción de bases de datos en la AAIP
- Medidas de seguridad proporcionales
- Transferencia internacional regulada

**Estado en Sarello:**
- ✅ Datos de contacto almacenados con propósito definido
- ❌ Consentimiento registrado
- ❌ Procedimiento de ejercicio de derechos ARCO
- ❌ Inscripción de bases de datos
- ❌ Política de privacidad

### Ley 11.683 — Procedimiento Tributario

**Qué regula:** Obligaciones fiscales, conservación de documentación, facturación electrónica.

**Requisitos clave:**
- Conservación de documentación por 10 años
- Facturación electrónica (RG 4291/2018)
- Libros contables obligatorios
- IVA, Ganancias, IIBB

**Estado en Sarello:**
- ✅ Módulo de impuestos con tipos y alícuotas
- ✅ Configuración de datos de empresa
- ❌ Facturación electrónica (integración AFIP)
- ❌ Generación de libros contables formales
- ❌ Período de retención de 10 años

### RT 419/10 — FACPCE

**Qué regula:** Marco conceptual para la preparación de estados financieros bajo NIIF en Argentina.

**Relevancia:** Define cómo se aplican las NIIF en el contexto argentino. Ver [NIIF en Argentina](niif-argentina.md) para detalle.

---

## Hoja de ruta de cumplimiento ISO

### Fase 1 — Seguridad y calidad de datos (prioridad alta)
- [ ] Cifrado de datos sensibles en base de datos
- [ ] Log de accesos y acciones de usuario
- [ ] Validación de CUIT/CUIL
- [ ] Detección de duplicados
- [ ] Política de privacidad

### Fase 2 — Gestión de documentos (prioridad alta)
- [ ] Firma digital de documentos contables
- [ ] Períodos de retención configurables
- [ ] Exportación a PDF/A
- [ ] Integración AFIP (facturación electrónica)
- [ ] Generación de libros contables formales

### Fase 3 — Continuidad y disponibilidad (prioridad media)
- [ ] Backups automatizados programados
- [ ] Plan de recuperación documentado
- [ ] Monitoreo de disponibilidad
- [ ] Pruebas de recuperación

### Fase 4 — Calidad del software (prioridad media)
- [ ] Cobertura de tests > 80%
- [ ] Manejo global de errores
- [ ] Métricas de calidad (SonarQube o similar)
- [ ] Revisiones de código sistemáticas

---

## Referencias

- [ISO 27001 — Seguridad de la información](https://www.iso.org/standard/27001)
- [ISO 9001 — Gestión de la calidad](https://www.iso.org/standard/62085.html)
- [ISO 15489 — Gestión de documentos](https://www.iso.org/standard/39353.html)
- [ISO/IEC 20000 — Gestión de servicios de TI](https://www.iso.org/standard/66431.html)
- [ISO 22301 — Continuidad del negocio](https://www.iso.org/standard/75106.html)
- [ISO/IEC 25010 — Calidad del software](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010)
- [ISO 8000 — Calidad de datos](https://www.iso.org/standard/62363.html)
- [Ley 25.326 — Protección de Datos Personales](https://www.argentina.gob.ar/normativa/nacional/ley-25326-2000)
- [Ley 11.683 — Procedimiento Tributario](https://www.argentina.gob.ar/afip/ley-11683)
- [AAIP — Autoridad de Protección de Datos](https://www.argentina.gob.ar/aaip)
- [AFIP — Factura Electrónica](https://www.afip.gob.ar/fe/)
