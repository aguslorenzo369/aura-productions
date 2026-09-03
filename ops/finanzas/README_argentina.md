# Argentina · CMC 2026 — costo total y costo por persona

La Rural, Pabellón Azul. Montaje 2 de octubre, evento 3 y 4 de octubre de 2026.

## Entregables

| Qué | Dónde |
|---|---|
| Google Sheet (una hoja, valores calculados) | https://docs.google.com/spreadsheets/d/1JaRn7MCDlVf8fC1KveJiMSg0lp6ZuNI74yTzRpvxS0Y/edit |
| Informe al CEO (artifact) | https://claude.ai/code/artifact/a3d38d15-ee52-4433-935c-692bbf18aca4 |
| Libro con fórmulas vivas (7 hojas) | `ARGENTINA_CMC2026_Costo_Total.xlsx` |
| CSV fuente del Google Sheet | `argentina_costo_total.csv` |
| Generadores | `construir_argentina.py`, `generar_csv_argentina.py` |

## Los números

| | USD |
|---|---:|
| Costo total del evento | 242.347 |
| Presupuesto original (hoja Argentina del master) | 176.159 |
| Diferencia | +66.188 (+37,6 %) |
| Costo por asistente pago (6.000) | 40,39 |
| **Ahorro negociado contra lo cotizado** | **52.102** (~$78,7 M) |

Por bloque: Sede 106.715 · Técnica 82.434 · Merch 17.417 · Servicios 14.953 · Catering 14.569 · Producción 6.260 · Equipo 0.

Por estado: cerrado 106.273 · contratado 92.977 · cotizado 36.801 · sin cotizar 5.700 · en negociación 596.

Tipo de cambio: **ARS 1.510 por USD**, que es el que usa Agustina. Verificado contra dos de sus
cifras: el montaje de $900.000 le da US$596 y el entelado de $24.500.000 le da US$16.225.

## Merch — las nueve facturas de Drive

Todo el merch sale de la carpeta compartida *Presupuestos merch* (facturas 2601009 a 2601019,
emisor IIDAI LLC). Reemplazan el renglón único de US$8.689 que traía el master. Los proveedores
son **argentinos**, no colombianos como decía la hoja PAGOS.

| Proveedor | Ítem | Cant. | Total ARS | % ARG | Costo ARG (USD) | Estado de pago |
|---|---|---:|---:|---:|---:|---|
| REMERASYESTAMPADOS | Pañuelos / pañoletas estampados | 8.500 | 16.198.875 | 65 % | 6.973 | 50 % abonado |
| REMERASYESTAMPADOS | Remeras premium estampadas | 250 | 4.268.275 | 100 % | 2.827 | **sin pagar** |
| REMERASYESTAMPADOS | Bordado computarizado en gorras | 940 | 2.643.200 | 100 % | 1.750 | **sin pagar** |
| TEXTIL RYU | Gorra Flex unicolor/bicolor | 940 | 2.692.226 | 100 % | 1.783 | pagada 100 % |
| LEOTEX | Lanyard premium doble raso 25 mm | 1.360 | 2.505.426 | 100 % | 1.659 | 50 % abonado |
| DERQUI IMPRESIONES | Gráfica oficial — Argentina | — | 3.660.565 | 100 % | 2.424 | 50 % abonado |
| DERQUI IMPRESIONES | Gráfica oficial — Uruguay | — | 1.893.197 | 0 % | 0 | otro evento |
| Blocko | Cintas portacredencial | 1.300 | 2.117.258 | — | 0 | alternativa descartada |
| | **Total imputado a Argentina** | | | | **17.417** | |

**Falta pagar:** US$9.941 por la regla del 50 %, o US$11.949 si las facturas reemitidas de
agosto están bien. Lo urgente son las remeras (US$2.781) y el bordado de gorras (US$1.722),
que no tienen nada abonado.

Dos duplicaciones que se sacaron del costo:

- **Blocko** cotizó las cintas portacredencial (US$1.402) — es el mismo ítem que los lanyards de
  LEOTEX, que ya está contratado y con anticipo pagado. Estaba sumando dos veces.
- **La gráfica de Uruguay** (US$1.233) figuraba en la hoja PAGOS del master con país = Argentina.

Tres cosas a confirmar:

1. Las facturas reemitidas de **LEOTEX** (2601018) y **Derqui Argentina** (2601014) vienen por el
   total, pero la carpeta y el master dicen que ya se abonó el 50 %. Son US$2.008 de diferencia en
   el calendario de pagos, no en el costo.
2. Los **8.500 pañuelos** son una compra compartida con Uruguay y la factura no separa unidades.
   Acá se imputó el 65 % a Argentina (5.500 de 8.500, la misma proporción que la gráfica). Si van
   todos a Argentina, el costo sube US$3.755.
3. Conviene corregir la gráfica de Uruguay también en el master, para que no se siga arrastrando.

## De dónde salen las cotizaciones

Todas se extrajeron de los adjuntos del correo de agustinalorenzog@gmail.com:

| Proveedor | Rubro | Monto | Fecha del mail |
|---|---|---:|---|
| La Rural — Infraestructura | Paneles, mobiliario, dirección técnica, guardias | ARS 23.994.708 (sin las sillas) | 17/08/2026 |
| La Rural — Infraestructura | 5.000 sillas (alternativa) | ARS 42.500.000 | 17/08/2026 |
| FDL Eventos (presup. 026-2697) | 1.000 sillas hotel + 4.500 plásticas Munro + flete, alquiler 4 días | ARS 25.800.000 + IVA | 07/08/2026 |
| La Rural — Conectividad | 2 redes WiFi privadas (presup. N.º 2) | ARS 1.466.064 + IVA | 05/08/2026 |
| Prina | Técnica integral | ARS 48.885.000 + IVA | 18/06/2026 |
| VMG | Pantallas LED 65 m² (alternativa) | ARS 12.625.000 + IVA | 29/06/2026 |
| Road Seguridad | 263 h de vigilancia + planos + supervisión | ARS 7.218.929 + IVA | 12/08/2026 |
| Vittal | Servicio médico, 3 días | ARS 6.366.521 + IVA 10,5 % | 28/08/2026 |
| Higia Eventos | Limpieza, 205,5 h | ARS 3.367.441 + IVA | 22/06/2026 |
| Gale Servicios | Retiro de residuos | ARS 1.471.609 + IVA | 22/06/2026 |
| Chanes Seguros | Accidentes personales, 150 personas | ARS 953.152 | 13/07/2026 |
| Blocko | 1.300 cintas portacredencial (descartada) | ARS 1.749.800 + IVA | 09/06/2026 |

El merch no sale del correo sino de la carpeta de Drive *Presupuestos merch*: ver la tabla de arriba.

## Merch — lo que iba a costar contra lo que costó

Fuente: `merch.cmc2026.com`, precios unitarios al 06/07/2026, dólar $1.515. Compara el proveedor que
traía Cumbre contra los proveedores argentinos conseguidos por Agustina.

| Producto | Cant. | Unit. Cumbre | Total Cumbre | Unit. Agustina | Total Agustina | Ahorro |
|---|---:|---:|---:|---:|---:|---:|
| Gorras negras | 1.000 | 9,90 | 9.901 | 1,64 | 1.637 | **8.264** (83 %) |
| Remeras estampadas | 100 | 16,17 | 1.617 | 9,31 | 931 | 686 (42 %) |
| Hojas A4 (contrato) | 5.500 | 0,20 | 1.107 | 0,05 | 265 | 842 (76 %) |
| Bolsas de friselina | 1.000 | 1,14 | 1.142 | 0,64 | 645 | 497 (44 %) |
| Tarjetas (cheque) | 5.500 | 0,12 | 672 | 0,02 | 110 | 562 (84 %) |
| Cinta colgante / lanyard | 1.000 | 1,25 | 1.248 | 1,00 | 1.005 | 243 (19 %) |
| Credenciales 10 × 13 cm | 1.000 | 0,57 | 575 | 0,48 | 475 | 100 (17 %) |
| **Subtotal Argentina** | | | **16.261** | | **5.068** | **11.193 (69 %)** |
| *Uruguay* | | | | | | |
| Escarapelas / credenciales | 600 | 1,322 | 793 | 0,475 | 285 | 508 (64 %) |
| Mapas de niveles de consciencia | 3.000 | 0,254 | 763 | 0,089 | 266 | 497 (65 %) |
| Contratos (hojas A4) | 3.000 | 0,153 | 458 | 0,048 | 145 | 313 (68 %) |
| Cheques (tarjetas) | 3.000 | 0,127 | 382 | 0,020 | 60 | 322 (84 %) |
| **Subtotal Uruguay** | | | **2.396** | | **756** | **1.640 (68 %)** |
| **Total Argentina + Uruguay** | | | **18.657** | | **5.824** | **12.833 (69 %)** |

La gorra sola explica tres cuartos del ahorro de Argentina. Quedan fuera de los dos lados las pulseras
tyvek y los cordones con mosquetón de Uruguay, porque no hay precio comparable. Uruguay va con su propio
subtotal: es la misma negociación con los mismos proveedores, pero **no** entra en el costo del evento
de Argentina.

**Esta canasta no reemplaza el costo del rubro.** Mide el ahorro por precio unitario sobre siete ítems y
deja fuera los pañuelos y el bordado de gorras; además las cantidades del sitio no son exactamente las de
las facturas finales (remeras 100 contra 250, gorras 1.000 contra 940). El costo real del merch
—US$17.417— sale de las nueve facturas de Drive.

## Técnica — las siete cotizaciones

Se pidió cotización a **nueve empresas** el 13 y 14 de junio de 2026. Respondieron seis con número;
Black-Out y 4A Latam nunca contestaron y una dirección de Sound-Light rebotó.

| Proveedor | Fecha | Sin IVA | Con IVA | Alcance |
|---|---|---:|---:|---|
| Sound-Light | 16/06 | — | +$100 M | PDF no legible (mail de 33 MB). El correo del 19/06 les pide revisar porque las otras estaban «prácticamente la mitad». |
| Bonetto | 17/06 | 94.936.000 | 114.872.560 | Sonido e iluminación 69.736.000 · LED 20.720.000 · CCTV 4.480.000. Grúas 4.480.000 y efectos aparte: chispa fría **$600.000 por minuto**. |
| Prina | 18/06 | 48.885.000 | 59.150.850 | LED de sólo 40 m² (el rider pide 65). Sin grúas ni energía. Validez vencida. |
| 2MG | 24/06 | 45.000.000 | 54.450.000 | Con descuento especial (lista 53.655.470). Adicionales aparte por 19.202.700. Sonido más liviano, «2000 / 5000 pax». |
| Dixi Group | 26/06 | 82.000.000 | 99.220.000 | Llave en mano: rigging completo, encomiendas, plano de arquitecto, 4 máquinas de chispa fría. |
| VMG | 29/06 | 12.625.000 | 15.276.250 | Sólo pantallas LED de 65 m². No comparable. |
| **Grupo MET** | contratado | — | **90.600.000** | US$60.000 por sonido, iluminación, video y LED. Bonifica 500 vallas y los efectos. |

**Por qué técnica no entra en la tabla de ahorros.** Sumándole el circuito cerrado (US$6.209), el paquete
de Grupo MET queda cerca de los $100 M: prácticamente lo mismo que Dixi llave en mano y por debajo de
Bonetto, pero **por encima de 2MG y de Prina**. Los alcances no son iguales — Prina cotizó 38 % menos de
LED y dejó afuera grúas y energía, 2MG cotizó un sonido más chico — pero eso hay que poder probarlo, y
para eso hace falta el PDF de Grupo MET con el alcance final.

Notas de extracción: el PDF de Bonetto trae el texto vectorizado (sin fuentes), así que hubo que
renderizarlo a imagen con `pymupdf` y leerlo visualmente. El de Sound-Light no se pudo bajar: pedir el
mensaje en formato RAW tumba la sesión del conector de Gmail por el tamaño (33 MB).

Hay un borrador en Gmail, *«Comparativa de técnica — las 7 cotizaciones de Argentina»*, con los montos y
el link directo a cada mail original.

## Advertencias

- **Técnica cerrada** con Grupo MET en US$60.000, pero sin PDF en el correo. Es el único de los siete proveedores sin respaldo escrito: ver la sección de abajo.
- **Los pesos son de la fecha de cada cotización.** VMG recotiza si el dólar salta más de 15 % y La Rural ajusta el saldo por IPC.
- **Catering cerrado** con Grupo Ambient en US$14.569 (600 lunchbox VIP + desayuno, almuerzo y cena para 150 personas), contra los US$33.820 que tenía el presupuesto.
- **Vuelos y alojamiento del equipo entran en cero.** No hay cotización en el correo ni monto en el sheet.
- **Cuatro rubros sin cotizar:** ecobaños, marquetería de certificaciones y premios, replanteo de sillas con ingeniero, y los cheques, escarapelas, diplomas, placas y manillas. El costo por persona es un piso, no un techo.
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
| Infraestructura y mobiliario | 26.490 | 9.270 | 17.220 (65 %) |
| Sillas del público | 28.146 | 21.270 | 6.876 (24 %) |
| Entelado | 25.828 | 16.225 | 9.603 (37 %) |
| Catering | 19.868 | 14.569 | 5.299 (27 %) |
| Vallado | 1.250 | 0 | 1.250 (100 %) |
| **Total** | **101.581** | **61.334** | **40.247 (40 %)** |

Técnica queda fuera de la comparativa: se cerró con Grupo MET en US$60.000 con todos los agregados,
y las otras cotizaciones (Sound-Light ~$100 M, 2MG $45–78 M, Prina $59,2 M, VMG $15,3 M sólo LED)
son sobre el pliego base. Falta el PDF de Grupo MET para comparar contra el mismo alcance.

## Presupuestos que estaban perdidos

| Qué | Dónde está |
|---|---|
| Retiro de residuos (Gale Servicios, $1.471.609 + IVA) | Adjunto `GALE SERVICIOS - CUMBRE DE LOS MILLONARIOS 2026.docx.pdf` en el mail de Higia Eventos reenviado el 29/06 por Nahuel |
| Conectividad, presupuesto actualizado | Mail de `conectividad@larural.com.ar` del **05/08/2026**, adjunto `Cumbre MC - Gira Millonarios (2).pdf`. Presupuesto N.º 2, base IPC junio: $1.466.063,84 + IVA (2 redes × $733.031,92). El del 16/06 era $1.438.728,01 |
| 2MG, producción técnica | Mail de `rocio.g@2mg.net` del 24/06, adjunto `20261003 y 04 - Cumbre de los Millonarios Conscientes - La R.pdf` |
