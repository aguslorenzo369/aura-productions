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
| Costo total del evento | 250.302 |
| Presupuesto original (hoja Argentina del master) | 176.159 |
| Diferencia | +74.143 (+42,1 %) |
| Costo por asistente pago (6.000) | 41,72 |
| **Ahorro negociado contra lo cotizado** | **40.412** (~$61,8 M) |

Composición: cerrado 105.074 · contratado 92.547 · cotizado 37.704 · sin cotizar 14.389 · en negociación 588.
Tipo de cambio: ARS 1.530 por USD.

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

## Auditoría de números (02/09)

Se contrastó cada monto contra su origen. Único error encontrado: **Gráfica URU (US$1.283) está
cargada con país Argentina** en la hoja PAGOS del master, y el cronograma le pone las cuotas en el
calendario argentino (US$1.241 pagados el 25/06 y US$42 al 13/09). Nunca entró al costo del evento,
pero infla los totales de Argentina de la planilla original.

Totales depurados de Argentina en el cronograma: vencido US$16.057 · programado US$40.294 ·
pagado US$52.253.

## Comparativa de ahorro

| Rubro | Referencia cotizada | Cerrado | Ahorro |
|---|---:|---:|---:|
| Infraestructura y mobiliario | 26.144 | 9.270 | 16.874 (65 %) |
| Sillas del público | 27.778 | 20.992 | 6.786 (24 %) |
| Entelado | 25.490 | 16.013 | 9.477 (37 %) |
| Catering | 19.608 | 13.582 | 6.026 (31 %) |
| Vallado | 1.250 | 0 | 1.250 (100 %) |
| **Total** | **100.270** | **59.857** | **40.412 (40 %)** |

Técnica queda fuera de la comparativa: se cerró con Grupo MET en US$60.000 con todos los agregados,
y las otras cotizaciones (Sound-Light ~$100 M, 2MG $45–78 M, Prina $59,2 M, VMG $15,3 M sólo LED)
son sobre el pliego base. Falta el PDF de Grupo MET para comparar contra el mismo alcance.

## Presupuestos que estaban perdidos

| Qué | Dónde está |
|---|---|
| Retiro de residuos (Gale Servicios, $1.471.609 + IVA) | Adjunto `GALE SERVICIOS - CUMBRE DE LOS MILLONARIOS 2026.docx.pdf` en el mail de Higia Eventos reenviado el 29/06 por Nahuel |
| Conectividad, presupuesto actualizado | Mail de `conectividad@larural.com.ar` del **05/08/2026**, adjunto `Cumbre MC - Gira Millonarios (2).pdf`. Presupuesto N.º 2, base IPC junio: $1.466.063,84 + IVA (2 redes × $733.031,92). El del 16/06 era $1.438.728,01 |
| 2MG, producción técnica | Mail de `rocio.g@2mg.net` del 24/06, adjunto `20261003 y 04 - Cumbre de los Millonarios Conscientes - La R.pdf` |
