# Finanzas CUMBRE 2026 — consolidado

Unifica los dos archivos que hoy viven separados en Drive:

| Fuente | Archivo | Qué aporta |
|---|---|---|
| CRONOGRAMA | `Cronograma_Pagos_Cumbre (1).xlsx` (`1MbTsbcMKau4WA4V2-0PM7EtJv2w4XA5P`) | Calendario de cuotas (54) + histórico de pagos (31) |
| MASTER | `INVERSIÓN GIRA CUMBRE 2026.xlsx` (`1rRjt9YDSJKZR23nFlHJrAOf9CENc3CL2`) | Contratos/reservas (44) + presupuesto línea por línea de 13 eventos |

## Archivos

| Archivo | Qué es |
|---|---|
| `CUMBRE_2026_Consolidado.xlsx` | El entregable. 8 hojas: LEEME, TABLERO, CALENDARIO UNIFICADO, PAGOS REALIZADOS, CONTRATOS, EVENTOS, HALLAZGOS, GASTOS EQUIPO |
| `datos_origen.json` | Dataset normalizado de las dos fuentes (lo consume el agente) |
| `extraer_origen.py` | Lee los dos `.xlsx` y produce `datos_origen.json` |
| `construir_consolidado.py` | Produce `CUMBRE_2026_Consolidado.xlsx` a partir del JSON |
| `factura_reintegro.py` | Genera la factura de reintegro de gastos en el formato estándar (el de la factura 2601020) |

## Regenerar

```bash
pip install openpyxl reportlab
python extraer_origen.py        # necesita cronograma.xlsx e inversion.xlsx en el cwd
python construir_consolidado.py
python factura_reintegro.py --demo          # verifica el formato de la factura
python factura_reintegro.py gasto.json factura_2601021.pdf
```

## Fecha de corte

Todo el análisis está calculado al **02/09/2026**. La celda `TABLERO!G2` es la fecha de corte:
cambiala y se recalculan los semáforos de vencimiento del calendario.

## Advertencias

- Las hojas por evento del MASTER están en moneda local con tasas inconsistentes dentro de la
  misma hoja (México presupuesta a 0,059 y paga a 0,051; Colombia a 3.700 y 4.080). La hoja
  `EVENTOS` documenta qué tasa se usó para cada conversión.
- `$1.087.979` (presupuesto de producción) y `$417.765` (calendario de contratos) **no son
  comparables ni sumables**: miden cosas distintas.
- `CALENDARIO UNIFICADO` y `PAGOS REALIZADOS` son conjuntos disjuntos (el histórico termina el
  03/07/2026, el calendario empieza el 10/07/2026): sumarlos no duplica.
- El libro se genera con openpyxl, que no guarda valores en caché de las fórmulas. Excel y
  Google Sheets las calculan al abrir; un visor rápido puede mostrarlas vacías.
