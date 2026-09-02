# Argentina · CMC 2026 — costo total y costo por persona

La Rural, Pabellón Azul. Montaje 2 de octubre, evento 3 y 4 de octubre de 2026.

## Entregables

| Qué | Dónde |
|---|---|
| Google Sheet (una hoja, valores calculados) | https://docs.google.com/spreadsheets/d/1SfTv0IzslQQjWe5ROmxbHTaAK51zUMRdTrW2wGwK1L4/edit |
| Libro con fórmulas vivas (4 hojas) | `ARGENTINA_CMC2026_Costo_Total.xlsx` |
| CSV fuente del Google Sheet | `argentina_costo_total.csv` |
| Generadores | `construir_argentina.py`, `generar_csv_argentina.py` |

## Los números

| | USD |
|---|---:|
| Costo total del evento | 233.732 |
| Presupuesto original (hoja Argentina del master) | 176.159 |
| Diferencia | +57.573 (+32,7 %) |
| Costo por asistente pago (6.000) | 38,96 |

Composición: contratado 92.547 · cotizado 91.726 · sin cotizar 49.459.
Alternativas descartadas (no suman): 37.639.

## De dónde salen las cotizaciones

Todas se extrajeron de los adjuntos del correo de agustinalorenzog@gmail.com:

| Proveedor | Rubro | Monto | Fecha del mail |
|---|---|---:|---|
| La Rural — Infraestructura | Paneles, mobiliario, dirección técnica, guardias | ARS 23.994.708 (sin las sillas) | 17/08/2026 |
| La Rural — Infraestructura | 5.000 sillas (alternativa) | ARS 42.500.000 | 17/08/2026 |
| FDL Eventos | 5.500 sillas + flete | ARS 25.800.000 + IVA | 07/08/2026 |
| La Rural — Conectividad | 2 redes WiFi privadas | ARS 1.438.728 + IVA | 16/06/2026 |
| Prina | Técnica integral | ARS 48.885.000 + IVA | 18/06/2026 |
| VMG | Pantallas LED 65 m² (alternativa) | ARS 12.625.000 + IVA | 29/06/2026 |
| Road Seguridad | 263 h de vigilancia + planos + supervisión | ARS 7.218.929 + IVA | 12/08/2026 |
| Vittal | Servicio médico, 3 días | ARS 6.366.521 + IVA 10,5 % | 28/08/2026 |
| Higia Eventos | Limpieza, 205,5 h | ARS 3.367.441 + IVA | 22/06/2026 |
| Gale Servicios | Retiro de residuos | ARS 1.471.609 + IVA | 22/06/2026 |
| Chanes Seguros | Accidentes personales, 150 personas | ARS 953.152 | 13/07/2026 |
| Blocko | 1.300 cintas portacredencial | ARS 1.749.800 + IVA | 09/06/2026 |

Tipo de cambio: ARS 1.535 por USD (dólar oficial venta, Banco Nación, 02/09/2026).

## Advertencias

- **Prina venció.** La cotización de técnica tenía validez de 10 días y es del 18 de junio. Es el ítem más caro en pesos: hay que revalidarla.
- **Los pesos son de la fecha de cada cotización.** VMG recotiza si el dólar salta más de 15 % y La Rural ajusta el saldo por IPC.
- **Catering no tiene cotización aceptada.** Entra al total con el estimado del sheet (US$33.820). AmbientHouse se rechazó por precio y Teist no cerró.
- **Vuelos y alojamiento del equipo entran en cero.** No hay cotización en el correo ni monto en el sheet. El costo por persona es un piso, no un techo.
- **Facturación al exterior sin resolver** con FDL Eventos y Vittal (la empresa que paga es de EE.UU.).

## Cómo se reconstruyeron los adjuntos

Los montos viven en PDF y XLS adjuntos, no en el cuerpo de los mails. `scripts/` del scratchpad tiene el
pipeline: se pide el mensaje en formato RAW, se parsea el MIME, se extraen los adjuntos y se vuelcan a
texto (`pypdf` para PDF, `xlrd` para XLS legacy, detectando el formato por los bytes de cabecera porque
los nombres MIME vienen rotos).
