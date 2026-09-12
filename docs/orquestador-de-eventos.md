# Orquestador de Eventos — Aura Productions

Plan de producto, arquitectura de agentes y hoja de ruta.
Versión 1.0 · Septiembre 2026

---

## 1. Punto de partida

Lo que hay hoy en el repositorio es una landing en Next.js 14 con siete secciones estáticas. No hay base de datos, ni autenticación, ni backend, ni un solo agente. Conviene decirlo sin vueltas porque cambia el encuadre: no vamos a escalar una app de producción, la vamos a construir. La landing sirve como cara pública y como base de stack, nada más.

Eso no es malo. Significa que podemos elegir bien el modelo de datos desde el día uno, que es lo único difícil de cambiar después.

---

## 2. Análisis de mercado

### 2.1 El mercado grande ya está tomado

El software de gestión de eventos mueve unos 14.290 millones de dólares en 2026 y crece a doble dígito anual. Los líderes son Cvent en corporativo, con unos 30.000 clientes en 175 países, Eventbrite en ticketing masivo y Bizzabo en eventos B2B con IA embebida. Además Salesforce, Microsoft y HubSpot están metiendo módulos de eventos dentro de sus suites.

Conclusión operativa: competir de frente en "plataforma de gestión de eventos" es suicida. Ese terreno se gana con integraciones y fuerza de ventas, no con producto.

### 2.2 El nicho de producción en vivo está fragmentado

Acá la foto es distinta. Las herramientas son chicas, viejas o de un solo uso:

| Herramienta | Qué resuelve | Límite |
|---|---|---|
| Master Tour | Giras, itinerarios, contactos | Caro, pesado, pensado para giras internacionales |
| Stage Portal | Shows, riders, crew, gastos en un lugar | Artista independiente, no productora |
| Ridermaker, StagePlot Pro, RiderForge | Stage plots y riders en PDF | Una sola función, sin datos del evento |
| Tour Assistant | Plantillas de rider y checklists | Documental, no operativo |
| SocialERP | ERP para productoras, costos | Genérico, sin IA, sin agentes |

Ninguna hace descubrimiento y negociación de proveedores. Ninguna trabaja por WhatsApp. Ninguna está pensada para Latinoamérica, donde el proveedor no está en un directorio sino en un contacto de teléfono.

### 2.3 La negociación con IA existe, pero arriba

Pactum hace negociación autónoma con proveedores, conectado a SAP Ariba y Coupa. Levelpath y Zip hacen orquestación de compras nativa con IA. Keelvar y Fairmarkit hacen sourcing. Todas son enterprise: contratos anuales de seis cifras, integración con ERP, pensadas para la cola larga de compras de una multinacional.

Nadie bajó eso a una productora de eventos de 5 a 50 personas en Latinoamérica.

### 2.4 Dónde está nuestro lugar

El hueco es la intersección exacta de tres cosas que hoy no se cruzan: producción de eventos en vivo, compras y negociación con proveedores, y Latinoamérica operando por WhatsApp.

Y hay un activo que se acumula solo: **la base de datos de proveedores con precios reales, tiempos de respuesta y desempeño por evento**. Eso no se puede copiar ni comprar, se construye evento a evento. Cada show que produce Aura la hace más valiosa. Ese es el foso defensivo del producto, no la interfaz.

---

## 3. El Orquestador de Eventos

### 3.1 Idea central

Un evento es una máquina de estados con plazos duros y dinero en juego. El Orquestador es el proceso que conoce ese estado y decide qué agente tiene que actuar, cuándo, y qué le tiene que preguntar a un humano antes de ejecutar.

No es un chatbot. Es un planificador con memoria del evento.

### 3.2 Máquina de estados del evento

```
BRIEF → PRESUPUESTO → SOURCING → CONTRATACIÓN → PRE-PRODUCCIÓN → DÍA D → CIERRE
```

En cada transición el Orquestador dispara trabajo y exige una aprobación humana concreta:

| Estado | Qué hace el Orquestador | Quién aprueba qué |
|---|---|---|
| BRIEF | Estructura el pedido: fecha, sede, público, rubros necesarios | Productor confirma el alcance |
| PRESUPUESTO | Arma presupuesto preliminar con precios históricos de la base | Productor fija el techo por rubro |
| SOURCING | Lanza el Agente de Proveedores por rubro | Productor aprueba la lista corta |
| CONTRATACIÓN | Genera órdenes de compra y contratos | Firma humana, siempre |
| PRE-PRODUCCIÓN | Agente de Riders genera y distribuye documentación | Técnico valida el rider |
| DÍA D | Cronograma vivo, checklist, incidencias | Jefe de producción |
| CIERRE | Conciliación final, post mortem, actualiza scoring de proveedores | Administración cierra números |

### 3.3 Arquitectura técnica

```
┌─────────────────────────────────────────────────────────┐
│  Interfaces:  Web (Next.js)  ·  WhatsApp  ·  Email       │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              ORQUESTADOR DE EVENTOS                      │
│  Máquina de estados · Planificador · Cola de aprobación  │
└──┬──────────────┬──────────────┬────────────────────┬───┘
   │              │              │                    │
┌──▼────────┐ ┌───▼──────┐ ┌─────▼──────┐ ┌───────────▼──┐
│Proveedores│ │ Finanzas │ │   Riders   │ │  (futuros)   │
└──┬────────┘ └───┬──────┘ └─────┬──────┘ └──────────────┘
   │              │              │
┌──▼──────────────▼──────────────▼─────────────────────────┐
│  Capa de herramientas: búsqueda · email · WhatsApp API ·  │
│  Sheets · PDF · almacenamiento · tipo de cambio           │
└──┬────────────────────────────────────────────────────────┘
   │
┌──▼────────────────────────────────────────────────────────┐
│  Datos: Postgres (eventos, proveedores, cotizaciones,      │
│  gastos, riders, contactos) + auditoría de toda acción     │
└───────────────────────────────────────────────────────────┘
```

**Stack recomendado**, elegido por velocidad de construcción y costo bajo al inicio:

- **Base y auth**: Supabase (Postgres, Row Level Security, storage de archivos).
- **App**: Next.js 14, el que ya está, con rutas de API y App Router.
- **Trabajos y colas**: Inngest o Trigger.dev. Los agentes corren como trabajos durables con reintentos, no dentro de un request HTTP.
- **Modelo**: Claude con tool use, un agente por rol y herramientas acotadas por agente.
- **Canales**: WhatsApp Cloud API de Meta, y un dominio propio de envío con Resend o Postmark.
- **Salida a planillas**: Google Sheets API, porque el equipo ya vive ahí.

### 3.4 Reglas que no se negocian

1. **Toda acción hacia afuera queda auditada.** Quién, cuándo, con qué prompt, qué respondió el modelo, qué se envió.
2. **Ningún agente firma, paga ni compromete dinero.** Propone; un humano aprueba.
3. **Autonomía por tramos de monto.** Bajo cierto monto el agente cierra solo, arriba escala. El umbral lo define Aura, no el modelo.
4. **Idempotencia.** Un reintento no puede mandar el mismo WhatsApp dos veces.
5. **Todo dato de contacto tiene origen y consentimiento registrados.**

---

## 4. Los agentes

### 4.1 Agente de Proveedores

El más valioso y el más delicado. Se divide en cinco capacidades que conviene construir en orden, no de una.

**Fase A — Descubrimiento.** Busca proveedores por rubro y ciudad: sonido, iluminación, estructuras, catering, seguridad, vallado, generadores, pantallas LED, transporte, backline. Fuentes: búsqueda web, directorios de cámaras y asociaciones del sector, redes sociales, y sobre todo la agenda histórica de Aura. Salida: ficha con razón social, rubro, ciudad, contacto, tamaño estimado y evidencia de trabajos.

**Fase B — Verificación y enriquecimiento.** Confirma que existe y opera: CUIT o identificador fiscal, antigüedad, referencias, equipamiento declarado, cobertura geográfica. Marca cada dato con su fuente y su confianza. Sin esto la base se llena de basura y el agente pierde credibilidad en la primera semana.

**Fase C — Contacto.** Acá está la restricción real, y hay que diseñar con ella, no contra ella:

> **WhatsApp no sirve para contacto frío.** Meta exige plantillas aprobadas para iniciar conversación, opt-in explícito y documentado, y arranca con un límite de 1.000 contactos únicos por día. Si más del 2% de los destinatarios bloquea o reporta, el número recibe restricciones y se puede perder. Además, desde el 1 de octubre de 2026 se cobra todo mensaje de servicio saliente por API.

Por eso el diseño correcto es:

- **Email es el canal frío.** A contacto comercial publicado, desde un dominio secundario, con calentamiento previo y volumen controlado. En Argentina rige la Ley 25.326: consentimiento libre, expreso e informado, y la base de datos se inscribe ante la AAIP. Esto hay que hacerlo bien una vez, no improvisarlo.
- **WhatsApp es el canal caliente.** Se activa cuando el proveedor responde o deja su número, y ahí sí la conversación fluye dentro de la ventana de 24 horas.

**Fase D — Cotización estructurada.** El agente no manda "hola, ¿cuánto sale?". Manda una solicitud con alcance, fecha, horarios, requerimientos técnicos, condiciones de pago y fecha límite de respuesta. Después parsea lo que vuelva, venga en PDF, en cuerpo de mail, en audio de WhatsApp o en una foto de un presupuesto escrito a mano, y lo normaliza a la misma grilla comparable.

**Fase E — Negociación asistida.** El agente prepara la posición: precio de mercado según la base histórica, rango objetivo, concesiones aceptables, alternativas disponibles. Redacta la contraoferta. **Un humano la aprueba antes de que salga.** Recién cuando haya cien negociaciones registradas y un historial medible se puede dar autonomía en compras chicas.

**Métricas del agente**: proveedores válidos nuevos por mes, tasa de respuesta por canal, tiempo desde pedido hasta tres cotizaciones comparables, ahorro promedio versus precio de lista, tasa de cumplimiento del proveedor el día del evento.

### 4.2 Agente de Finanzas

El de menor riesgo y el de valor más inmediato. Por eso va primero en el roadmap.

**Entrada por WhatsApp.** El productor manda lo que tiene a mano: "3.500 de flete para el show de Córdoba", una foto del ticket, un audio. El agente extrae monto, moneda, rubro, evento, proveedor y fecha. Si algo no cierra, repregunta una sola vez y de forma concreta.

**Registro.** Escribe en Postgres como fuente de verdad y refleja a Google Sheets, que es donde el equipo mira. Maneja pesos y dólares con tipo de cambio del día y lo deja registrado, porque en Latinoamérica reconstruir un gasto sin su tipo de cambio es imposible.

**Control.** Cada gasto se compara contra el presupuesto del evento por rubro. Si un rubro se pasa del umbral, avisa en el momento, no el martes.

**Informe de los martes.** Por email y por WhatsApp: gastos de la semana, acumulado por evento, desvíos contra presupuesto, pagos pendientes, y proyección de cierre de cada evento abierto. Un PDF y un resumen de cinco líneas, porque nadie lee el PDF desde el teléfono.

**Métricas**: porcentaje de gastos cargados el mismo día, exactitud de la extracción, desvío real versus proyectado al cierre.

### 4.3 Agente de Riders

Toma los datos del evento y genera la documentación técnica, que hoy se hace a mano y se copia mal de un evento anterior.

- **Rider técnico**: lista de canales, backline, requerimientos de sonido e iluminación, energía, horarios de montaje y prueba de sonido.
- **Stage plot**: plano de escenario renderizado, con posiciones, microfonía y monitores.
- **Rider de hospitality**: camarines, catering, transporte, alojamiento.
- **Paquete de advancing**: todo junto en PDF, versionado, listo para mandar a la sede y al proveedor técnico.

Lo importante es que se alimente del evento, no de una plantilla suelta. Si el Orquestador sabe que hay cinco músicos, una batería y dos guitarras, el rider sale solo. Y cada versión queda guardada, porque el rider del año pasado es el mejor borrador del de este año.

**Métricas**: tiempo de armado del paquete, cantidad de correcciones del técnico por rider, incidencias el día del evento atribuibles a documentación.

---

## 5. Escalabilidad y profesionalismo

Esto es lo que separa un experimento de un producto. Doce puntos, en orden de urgencia.

1. **Un solo modelo de datos, decidido antes de escribir agentes.** Evento, Sede, Proveedor, Contacto, Rubro, Cotización, OrdenDeCompra, Gasto, Presupuesto, Rider, Documento, Aprobación, Interacción. Todo lo demás se deriva.
2. **Entornos separados.** Desarrollo, staging y producción con bases distintas. Un agente que manda mails no puede correr nunca contra datos reales por accidente.
3. **Los agentes corren en colas durables.** Con reintentos, backoff e idempotencia. Nunca dentro de un request HTTP.
4. **Human-in-the-loop como parte del modelo de datos.** Una tabla de aprobaciones con estado, responsable y vencimiento. No un mensaje suelto de Slack.
5. **Auditoría completa.** Cada llamada al modelo con su prompt, su versión, su costo en tokens y su resultado. Sin esto no se puede depurar ni defender una decisión.
6. **Prompts versionados en el repositorio.** Como código, con revisión. Nunca pegados en una interfaz.
7. **Evaluaciones automáticas por agente.** Un set de casos reales con salida esperada, corriendo en CI. Antes de cambiar un prompt hay que poder medir si mejoró.
8. **Presupuesto de tokens por agente y por evento**, con corte automático. Un agente en bucle puede costar cientos de dólares en una noche.
9. **Seguridad de datos.** Row Level Security desde el inicio, secretos en gestor de secretos, datos personales de proveedores cifrados y con política de retención.
10. **Observabilidad.** Trazas, alertas de error, tablero de salud de cada agente. Un agente que falla en silencio es peor que no tenerlo.
11. **Tests e integración continua.** Tipado estricto, lint, tests de las funciones de dinero y de fechas. El repositorio hoy no tiene ni un test.
12. **Respaldos y plan de restauración probado.** La base de proveedores va a ser el activo más valioso de la empresa.

---

## 6. Hoja de ruta

Cada fase termina con un criterio de salida verificable. Sin ese criterio no se pasa a la siguiente.

### Fase 0 — Fundaciones · 2 semanas
Supabase, autenticación, modelo de datos completo, panel mínimo de eventos, un evento real cargado a mano de principio a fin.
**Salida**: un evento pasado de Aura entero en el sistema, con proveedores, gastos y rider.

### Fase 1 — Agente de Finanzas · 4 a 6 semanas
Ingreso por WhatsApp, extracción, escritura a Postgres y Sheets, control contra presupuesto, informe de los martes.
**Salida**: cuatro semanas seguidas de informe generado sin corrección manual.

### Fase 2 — Agente de Riders · 4 a 6 semanas
Generación de rider técnico, stage plot y hospitality desde los datos del evento, con versionado y exportación a PDF.
**Salida**: tres eventos reales producidos con documentación generada por el agente y validada por el técnico.

### Fase 3 — Agente de Proveedores · 10 a 14 semanas
En tres entregas separadas: primero descubrimiento y base de datos, después contacto y cotización, por último negociación asistida.
**Salida por entrega**: 200 proveedores verificados en cinco ciudades; tres cotizaciones comparables en menos de 72 horas; cinco negociaciones cerradas con ahorro medido.

### Fase 4 — Orquestador · 6 a 8 semanas
Máquina de estados completa, cola de aprobaciones, coordinación entre los tres agentes.
**Salida**: un evento producido de punta a punta con el Orquestador conduciendo.

### Fase 5 — Producto para terceros · a partir del mes 9
Multi-tenant, planes, incorporación de otras productoras.
**Salida**: tres productoras externas pagando.

Total hasta el Orquestador funcionando: entre siete y nueve meses de trabajo sostenido.

---

## 7. Plan de crecimiento

**Etapa 1, cliente cero.** Aura usa el sistema en todos sus eventos. El objetivo no es facturar, es que la base de proveedores y el historial de precios crezcan con datos reales. Sin esto no hay producto que vender.

**Etapa 2, productoras aliadas.** Cinco a diez productoras de Argentina, Chile, Uruguay, México y Colombia usando el sistema gratis o casi, a cambio de que sus datos de proveedores alimenten la base. Acá se prueba que el producto sirve fuera de Aura.

**Etapa 3, monetización.** Tres modelos posibles, y conviene probar los tres antes de elegir:

- Suscripción mensual por productora, con límite de eventos activos.
- Cargo por evento producido, que acompaña la estacionalidad del rubro.
- Porcentaje sobre el ahorro negociado, que es el que mejor alinea incentivos y el más difícil de auditar.

**Etapa 4, el activo.** Con miles de proveedores calificados y precios históricos por ciudad y rubro, aparecen negocios que hoy no existen en la región: índice de precios de producción, verificación de proveedores, financiamiento de eventos, seguros. Ahí el producto deja de ser una herramienta y pasa a ser infraestructura.

---

## 8. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Bloqueo del número de WhatsApp por reportes | Se cae el canal principal | Nunca contacto frío por WhatsApp, opt-in registrado, volumen gradual, número separado para el agente |
| Sanción por Ley 25.326 | Multas y suspensión de la base | Inscripción ante la AAIP, consentimiento registrado, baja inmediata a pedido |
| El agente negocia mal y quema un proveedor | Pérdida de relaciones que costaron años | Aprobación humana obligatoria, tono y límites definidos por Aura, lista de proveedores intocables |
| Datos sucios en la base de proveedores | El producto pierde credibilidad interna | Verificación obligatoria con fuente y confianza por campo |
| Costo de tokens fuera de control | Gasto imprevisible | Presupuesto por agente con corte automático |
| Dependencia de un solo proveedor de modelo | Riesgo operativo | Capa de abstracción sobre el modelo desde el inicio |

---

## 9. Qué necesito que carguen para avanzar

### 9.1 Datos de Aura, lo más urgente

Sin esto todo lo anterior es teoría. En orden de importancia:

1. **Planilla de proveedores actual**, con lo que haya: nombre, rubro, contacto, precios de la última vez. Aunque esté desordenada.
2. **Gastos de los últimos cinco a diez eventos**, con rubro y monto. Es lo que entrena el control de presupuesto.
3. **Tres a cinco riders reales** ya usados, con sus stage plots. Son las plantillas del agente.
4. **Un contrato tipo y una orden de compra tipo.**
5. **La política de compras**: quién aprueba qué monto, qué formas de pago se usan, qué plazos se aceptan.
6. **El tono de Aura**: cómo se le escribe a un proveedor. Un par de conversaciones reales alcanza.

### 9.2 Accesos técnicos

- **Supabase**, cuenta y proyecto.
- **Clave de API de Claude**, con presupuesto mensual definido.
- **WhatsApp Business API**, que exige verificación de Meta Business y un número dedicado. Es el trámite más lento, conviene empezarlo ya.
- **Dominio de envío de email** separado del corporativo, con registros SPF, DKIM y DMARC.
- **Google Sheets y Drive**, ya conectados en esta sesión.
- **Inscripción de la base de datos ante la AAIP**, trámite legal, en paralelo.

### 9.3 Habilidades y conectores a instalar

Conectores que ya están disponibles: Google Drive, Google Sheets, Gmail, Google Calendar, Notion, Asana, Canva, Vercel, GitHub.

Lo que falta y conviene sumar:

- **Supabase**, para que yo pueda crear y migrar el esquema directamente.
- **WhatsApp o Twilio**, para probar plantillas y flujos sin salir de acá.
- **Slack**, si el equipo lo usa para aprobaciones.
- **MercadoPago o Stripe**, cuando lleguemos a cobrar.

Habilidades propias de Aura que conviene crear, una por una, con la habilidad `skill-creator`:

- **Marca Aura**: tono, identidad visual, plantillas de documento.
- **Política de compras**: topes, aprobaciones, condiciones estándar.
- **Formato de rider**: la estructura exacta que usa Aura.
- **Informe financiero**: el formato del informe de los martes.
- **Catálogo de rubros**: la taxonomía de proveedores de Aura, que es la columna vertebral de toda la base.

Cada una de esas habilidades hace que yo trabaje con los criterios de Aura en lugar de con criterios genéricos. Es la diferencia más grande que pueden hacer con poco esfuerzo.

---

## 10. Lo primero que haría

Si hay que elegir una sola cosa para las próximas dos semanas: **el modelo de datos y la carga de un evento pasado completo**. Es aburrido y no se ve, pero define si los tres agentes se pueden construir o no. Todo lo demás depende de eso.

Y en paralelo, porque es trámite y tarda: iniciar la verificación de Meta Business para WhatsApp y la inscripción de la base ante la AAIP.
