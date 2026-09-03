# Dashboard de pagos · CMC 2026

`index.html` es el tablero de pagos actualizado con el checklist centralizado de Argentina.

## Cómo se regenera

```
cd ops/finanzas
python3 actualizar_html_pagos.py <index.html original> dashboard_pagos/index.html
```

El script toma el HTML original y:

1. Deja intactos los 47 pagos de los otros países (su cronograma proyectado sigue valiendo).
2. Reemplaza las 7 filas de Argentina por las 33 del checklist verificado
   (`generar_checklist_pagos.py`), que cierra exactamente contra el costo total del evento.
3. Mueve "Gráfica URU" (US$42) a Uruguay, que es de donde era.
4. Admite `fecha_limite: null` para los pagos sin fecha acordada, en vez de inventar fechas.
5. Arregla tres cosas que estaban rotas en el HTML original:
   - el semáforo por urgencia (el JS emitía clases `vencido/urgente/enfecha` y el CSS
     tenía `urg/urg7/ok`, así que ningún color se aplicaba);
   - el chip de categoría (el JS ponía la clase `pago-cat`, que es el contenedor, en vez de `cat`);
   - si el CDN de Firebase no cargaba, `firebase.initializeApp` tiraba y se llevaba puesto
     al `render()`: la página quedaba en blanco. Ahora degrada y el tablero se ve igual.

## Números al 3 de septiembre de 2026

| | pagos | USD |
|---|---:|---:|
| Argentina (falta desembolsar) | 33 | 186.456,06 |
| Resto de los países | 47 | 402.262,32 |
| **Total** | **80** | **588.718,38** |

Argentina: costo total US$242.347,21 · ya pagado US$55.891,15 · dólar $1.510.

## Pagos sin fecha acordada

24 de los 80 pagos no tienen fecha de pago acordada (US$112.677). No se les inventó una:
aparecen con la etiqueta que corresponde ("A definir", "Pedir presup.", "Antes del armado",
"Contra el evento") y se pueden aislar con el filtro **Sin fecha acordada**.
Los dos anticipos que destraban contratos (Grupo MET y Grupo Ambient) tampoco tienen fecha,
pero van marcados como urgentes a mano porque lo son.
