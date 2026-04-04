# Normas NIIF aplicables en Argentina

## Introducción

Las **Normas Internacionales de Información Financiera (NIIF / IFRS)** son un conjunto de estándares contables emitidos por el **International Accounting Standards Board (IASB)**. Su objetivo es establecer un lenguaje contable común a nivel global, permitiendo que los estados financieros sean comparables, transparentes y confiables independientemente del país de origen.

### Marco regulatorio argentino

En Argentina, la adopción de NIIF se formalizó a través de:

- **Ley 26.215** (2007): Establece la obligación de uniformar las normas contables con estándares internacionales.
- **Resolución Técnica 26** (FACPCE, 2009): Primera adopción para grandes empresas.
- **Resolución General CNV 551/2010**: Obligó a empresas emisoras de valores negociables a presentar estados financieros bajo NIIF desde 2012.
- **Resolución Técnica 419/10** (FACPCE): Marco conceptual para PyMEs basado en NIIF para PyMEs.
- **RT 52** (FACPCE, 2021): Actualización del marco normativo profesional.

### Quiénes deben cumplir

| Tipo de empresa | Obligación | Norma aplicable |
|----------------|------------|-----------------|
| Grandes empresas (CNV) | Obligatorio desde 2012 | NIIF completas |
| PyMEs | Obligatorio desde 2019 | NIIF para PyMEs |
| Entidades sin fines de lucro | Obligatorio | NIIF simplificadas |
| Cooperativas y mutuales | Obligatorio | NIIF adaptadas |
| Microempresas | Opcional | NIIF para PyMEs |

---

## NIIF aplicables al proyecto Sarello

### NIC 1 — Presentación de estados financieros

**Qué regula:** La estructura mínima y contenido de los estados financieros con propósito general.

**Requisitos clave:**
- Estado de situación patrimonial (Balance)
- Estado de resultados integrales
- Estado de cambios en el patrimonio neto
- Estado de flujos de efectivo
- Notas, incluyendo resumen de políticas contables significativas
- Información comparativa del período anterior
- Clasificación corriente / no corriente

**Estado en Sarello:**
- ✅ Balance de sumas y saldos implementado
- ✅ Estado de resultados implementado
- ✅ Información comparativa por trimestres
- ❌ Estado de cambios en el patrimonio neto
- ❌ Estado de flujos de efectivo
- ❌ Notas a los estados financieros
- ❌ Clasificación corriente/no corriente

**Importancia:** Es la norma fundamental. Sin ella, los demás estados carecen de marco de presentación válido.

---

### NIC 2 — Inventarios

**Qué regula:** El reconocimiento, medición y presentación de inventarios.

**Requisitos clave:**
- Valuación al menor entre costo y valor neto de realización (VNR)
- Métodos de costo permitidos: FIFO o promedio ponderado (LIFO prohibido)
- Reconocimiento de deterioro cuando VNR < costo
- Revelación de políticas contables y montos

**Estado en Sarello:**
- ❌ Módulo de inventario no implementado
- ❌ Sin cálculo de costo vs VNR
- ❌ Sin métodos FIFO/promedio

**Importancia:** Crítico para empresas con stock. La valuación incorrecta de inventarios distorsiona resultados y patrimonio.

---

### NIC 7 — Estado de flujos de efectivo

**Qué regula:** La presentación de información sobre cambios en efectivo y equivalentes de efectivo.

**Requisitos clave:**
- Clasificación en actividades de operación, inversión y financiamiento
- Método directo o indirecto para actividades operativas
- Conciliación con el resultado del período (método indirecto)
- Revelación de políticas de efectivo y equivalentes

**Estado en Sarello:**
- ❌ No se genera el estado
- ✅ Cuentas de tesorería con conciliación (base para el método directo)

**Importancia:** Permite evaluar la capacidad de la entidad para generar efectivo. Esencial para análisis financiero y toma de decisiones.

---

### NIC 8 — Políticas contables, cambios en estimaciones y errores

**Qué regula:** La selección y aplicación de políticas contables, y el tratamiento de cambios y correcciones.

**Requisitos clave:**
- Jerarquía de fuentes para seleccionar políticas (NIIF → Pronunciamientos → Otras fuentes)
- Aplicación retroactiva de cambios de política
- Aplicación prospectiva de cambios de estimación
- Reexpresión retroactiva de errores materiales
- Revelación de naturaleza e impacto de cambios

**Estado en Sarello:**
- ✅ Ejercicios contables con cierre y apertura
- ✅ Trazabilidad de asientos por origen
- ❌ Registro de cambios en políticas contables
- ❌ Registro de corrección de errores

**Importancia:** Garantiza comparabilidad interperíodo y transparencia en cambios metodológicos.

---

### NIC 10 — Hechos posteriores a la fecha de cierre

**Qué regula:** El tratamiento de eventos ocurridos entre la fecha de cierre y la fecha de autorización de los estados financieros.

**Requisitos clave:**
- Hechos que ajustan: se reflejan en los estados financieros
- Hechos que no ajustan: se revelan en notas
- Revelación de fecha de autorización y quién la otorgó

**Estado en Sarello:**
- ✅ Ejercicios con fecha de cierre definida
- ❌ Registro de hechos posteriores
- ❌ Fecha de autorización de estados financieros

**Importancia:** Los eventos entre cierre y emisión pueden ser materialmente significativos.

---

### NIC 12 — Impuesto a las ganancias

**Qué regula:** El reconocimiento, medición y presentación del impuesto a las ganancias, incluyendo impuestos diferidos.

**Requisitos clave:**
- Impuesto corriente: calculado sobre resultado imponible
- Impuesto diferido: diferencias temporarias entre base contable y fiscal
- Activos por impuestos diferidos: solo si es probable que haya ganancias futuras
- Tasa impositiva vigente o sustancialmente promulgada

**Estado en Sarello:**
- ✅ Módulo de impuestos con tipos y alícuotas
- ✅ Configuración de impuestos por jurisdicción
- ❌ Cálculo de impuesto diferido
- ❌ Diferencias temporarias

**Importancia:** El impuesto diferido puede representar activos/pasivos significativos. Su omisión distorsiona la situación patrimonial.

---

### NIC 16 — Propiedad, planta y equipo

**Qué regula:** El reconocimiento, medición y revelación de activos tangibles de uso prolongado.

**Requisitos clave:**
- Reconocimiento inicial al costo
- Modelo de costo o modelo de revaluación
- Depreciación sistemática durante la vida útil
- Test de deterioro cuando hay indicios
- Baja cuando se dispone del activo

**Estado en Sarello:**
- ❌ Sin módulo de activos fijos
- ❌ Sin cálculo de depreciación

**Importancia:** Fundamental para empresas con infraestructura significativa. La depreciación impacta directamente en resultados.

---

### NIC 19 — Beneficios a los empleados

**Qué regula:** El reconocimiento y medición de todos los beneficios que una entidad otorga a sus empleados.

**Requisitos clave:**
- Beneficios a corto plazo: reconocimiento cuando se devengan
- Beneficios post-empleo: planes de beneficio definido vs contribución definida
- Indemnizaciones por despido: reconocimiento cuando la entidad se compromete
- Otros beneficios a largo plazo

**Estado en Sarello:**
- ❌ Sin módulo de recursos humanos
- ❌ Sin cálculo de provisiones laborales

**Importancia:** En Argentina, las provisiones laborales (indemnizaciones, vacaciones, SAC) son significativas.

---

### NIC 21 — Efectos de las variaciones en las tasas de cambio

**Qué regula:** El tratamiento contable de transacciones en moneda extranjera y la conversión de estados financieros.

**Requisitos clave:**
- Reconocimiento inicial al tipo de cambio de la fecha de transacción
- Medición posterior: partidas monetarias al tipo de cambio de cierre
- Diferencias de cambio: reconocimiento en resultados
- Conversión de estados financieros de entidades en el extranjero

**Estado en Sarello:**
- ✅ Soporte multi-moneda en cuentas de tesorería (ARS, USD, EUR)
- ❌ Conversión automática a moneda funcional
- ❌ Reconocimiento de diferencias de cambio

**Importancia:** Crítico en economías con alta inflación y volatilidad cambiaria como la argentina.

---

### NIC 36 — Deterioro del valor de los activos

**Qué regula:** La evaluación y reconocimiento de pérdidas por deterioro de activos.

**Requisitos clave:**
- Test de deterioro cuando hay indicios
- Valor recuperable: mayor entre valor razonable menos costos de disposición y valor en uso
- Reversión de deterioro (excepto para plusvalía)
- Revelación de supuestos y sensibilidad

**Estado en Sarello:**
- ❌ Sin evaluación de deterioro
- ❌ Sin cálculo de valor en uso

**Importancia:** Evita sobrevaluación de activos en los estados financieros.

---

### NIC 37 — Provisiones, pasivos contingentes y activos contingentes

**Qué regula:** El reconocimiento y medición de provisiones y contingencias.

**Requisitos clave:**
- Provisión: obligación presente, probable salida de recursos, estimación confiable
- Pasivo contingente: solo revelación (no reconocimiento)
- Activo contingente: solo revelación si es probable
- Mejor estimación del desembolso necesario

**Estado en Sarello:**
- ❌ Sin gestión de provisiones
- ❌ Sin registro de contingencias

**Importancia:** Las provisiones (garantías, litigios, reestructuraciones) pueden ser materialmente significativas.

---

### NIC 38 — Activos intangibles

**Qué regula:** El reconocimiento, medición y revelación de activos intangibles.

**Requisitos clave:**
- Reconocimiento si es probable beneficios futuros y costo medible
- Vida útil definida o indefinida
- Amortización sistemática (vida definida)
- Test de deterioro anual (vida indefinida)

**Estado en Sarello:**
- ❌ Sin módulo de intangibles
- ❌ Sin cálculo de amortización

**Importancia:** Relevante para empresas con software, marcas, patentes, know-how.

---

### NIIF 9 — Instrumentos financieros

**Qué regula:** Clasificación, medición, deterioro y cobertura de instrumentos financieros.

**Requisitos clave:**
- Clasificación: costo amortizado, valor razonable con cambios en OCI, valor razonable con cambios en resultados
- Modelo de deterioro esperado (ECL) en 3 etapas
- Contabilidad de coberturas (opcional)

**Estado en Sarello:**
- ❌ Sin clasificación de instrumentos
- ❌ Sin modelo de deterioro esperado
- ❌ Sin contabilidad de coberturas

**Importancia:** Fundamental para entidades financieras y empresas con instrumentos complejos.

---

### NIIF 15 — Ingresos por contratos con clientes

**Qué regula:** El reconocimiento de ingresos basado en la transferencia de control de bienes o servicios.

**Requisitos clave (modelo de 5 pasos):**
1. Identificar el contrato
2. Identificar las obligaciones de desempeño
3. Determinar el precio de transacción
4. Asignar el precio a las obligaciones
5. Reconocer ingreso cuando se satisface cada obligación

**Estado en Sarello:**
- ❌ Módulo de ventas no implementado
- ❌ Sin reconocimiento por desempeño
- ❌ Sin identificación de obligaciones de desempeño

**Importancia:** Cambió radicalmente cómo se reconoce el ingreso. Crítico para contratos complejos.

---

### NIIF 16 — Arrendamientos

**Qué regula:** El reconocimiento, medición y revelación de arrendamientos.

**Requisitos clave:**
- Reconocimiento de activo por derecho de uso y pasivo por arrendamiento
- Excepciones: corto plazo (< 12 meses) y bajo valor
- Depreciación del activo + interés del pasivo
- Revelaciones extensas

**Estado en Sarello:**
- ❌ Sin módulo de arrendamientos
- ❌ Sin cálculo de valor presente de pagos

**Importancia:** Elimina la distinción operativo/financiero. Todos los arrendamientos van al balance.

---

## Arquitectura NIIF del proyecto

### Cómo Sarello soporta el cumplimiento NIIF

**Doble entrada como base:**
Cada movimiento genera un asiento contable con partida doble, garantizando que la ecuación patrimonial se mantenga. Esto es requisito fundamental de NIC 1.

**Trazabilidad completa:**
Cada asiento tiene `origen` y `origen_id`, permitiendo rastrear cualquier registro hasta su documento fuente (factura, movimiento de tesorería, ajuste).

**Mapeo contable configurable:**
El modelo `MapeoContable` permite asociar eventos del negocio con cuentas contables específicas, facilitando la clasificación correcta según NIIF.

**Ejercicios contables:**
El modelo `Ejercicio` con estados (abierto/cerrado/anulado) soporta el cierre contable y la generación de asientos de apertura, requisito de NIC 8.

**Conciliación:**
La conciliación entre saldos de tesorería y contabilidad asegura la integridad de los datos, base para estados financieros confiables.

---

## Hoja de ruta de cumplimiento NIIF

### Fase 1 — NIC 1 completa (prioridad alta)
- [ ] Estado de cambios en el patrimonio neto
- [ ] Estado de flujos de efectivo (NIC 7)
- [ ] Notas a los estados financieros
- [ ] Clasificación corriente/no corriente
- [ ] Información comparativa completa

### Fase 2 — Módulos operativos (prioridad media)
- [ ] Módulo de inventarios (NIC 2)
- [ ] Módulo de ventas con NIIF 15
- [ ] Módulo de activos fijos (NIC 16)
- [ ] Módulo de recursos humanos (NIC 19)

### Fase 3 — Complejidad contable (prioridad media-baja)
- [ ] Impuesto diferido (NIC 12)
- [ ] Provisiones y contingentes (NIC 37)
- [ ] Arrendamientos (NIIF 16)
- [ ] Deterioro de activos (NIC 36)
- [ ] Instrumentos financieros (NIIF 9)

---

## Referencias

- [IASB — IFRS Standards](https://www.ifrs.org/issued-standards/)
- [FACPCE — Federación Argentina de Consejos Profesionales de Ciencias Económicas](https://www.facpce.org.ar/)
- [CNV — Comisión Nacional de Valores](https://www.cnv.gob.ar/)
- [Ley 26.215 — Uniformidad de normas contables](https://www.argentina.gob.ar/normativa/nacional/ley-26215-2007)
- [RT 26 — Primera adopción NIIF](https://www.facpce.org.ar/)
- [RT 419/10 — NIIF para PyMEs](https://www.facpce.org.ar/)
- [Deloitte — NIIF en Argentina](https://www2.deloitte.com/ar/es.html)
- [PwC — Manual de NIIF](https://www.pwc.com/ar/es/publicaciones/ifrs.html)
