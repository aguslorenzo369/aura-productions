# -*- coding: utf-8 -*-
"""Genera el CSV de una sola hoja para subir a Google Sheets (con fórmulas vivas)."""
import csv, io, importlib.util, sys

spec = importlib.util.spec_from_file_location('ca', 'construir_argentina.py')
# Reutilizamos la lista ITEMS sin ejecutar la construcción del xlsx
fuente = open('construir_argentina.py', encoding='utf-8').read()
ini = fuente.index('ARS_, USD_ =')
fin = fuente.index('# ====', ini)
ns = {}
exec(fuente[ini:fin], ns)
ITEMS = ns['ITEMS']
TC = 1535.0

filas = []
def f(*c): filas.append(list(c))

f('ARGENTINA · CUMBRE DE LOS MILLONARIOS CONSCIENTES 2026')
f('La Rural, Pabellón Azul · montaje 2 de octubre · evento 3 y 4 de octubre de 2026')
f('Unifica los presupuestos recibidos por mail (jun-ago 2026) con la hoja Argentina del master de inversión. Corte al 02/09/2026.')
f()
f('Tipo de cambio (ARS por USD)', TC, 'Dólar oficial venta, Banco Nación, 02/09/2026. Editá este número y se recalcula todo.')
FILA_TC = len(filas)          # 1-indexada
f()
f('Rubro', 'Proveedor', 'Detalle', 'Estado', 'Moneda', 'Monto sin IVA',
  'IVA', 'Total moneda origen', 'Total USD', 'Estimado del sheet (USD)', 'Diferencia', 'Fuente')
FILA_HDR = len(filas)

orden = ['Sede', 'Técnica', 'Servicios', 'Merch', 'Catering', 'Producción', 'Equipo']
subtotales = []
for bloque in orden:
    grupo = [x for x in ITEMS if x[0] == bloque]
    if not grupo: continue
    f(bloque.upper())
    ini_b = len(filas) + 1
    for (_, rubro, prov, det, mon, monto, iva, estado, est, fuente_txt) in grupo:
        n = len(filas) + 1
        f(rubro, prov, det, estado, mon,
          monto if monto else '', iva if iva else '',
          f'=IF(F{n}="","",F{n}*(1+N(G{n})))',
          f'=IF(H{n}="",N(J{n}),IF(E{n}="USD",H{n},H{n}/$B${FILA_TC}))',
          est if est else '',
          f'=IF(D{n}="Alternativa","",I{n}-N(J{n}))',
          fuente_txt)
    n = len(filas) + 1
    f(f'Subtotal {bloque}', '', '', '', '', '', '', '',
      f'=SUMIF($D${ini_b}:$D${n-1},"<>Alternativa",$I${ini_b}:$I${n-1})',
      f'=SUM($J${ini_b}:$J${n-1})',
      f'=I{n}-J{n}')
    subtotales.append(n)

f()
n = len(filas) + 1
f('COSTO TOTAL DEL EVENTO', '', '', '', '', '', '', '',
  '=' + '+'.join(f'I{x}' for x in subtotales),
  '=' + '+'.join(f'J{x}' for x in subtotales),
  '=' + '+'.join(f'K{x}' for x in subtotales))
FILA_TOTAL = n

f()
f('COSTO POR PERSONA')
f('Base de cálculo', 'Personas', 'Costo por persona', '', 'Qué incluye')
for etiqueta, personas, nota in [
    ('Aforo general', 5000, 'Asistentes de entrada general.'),
    ('VIP', 1000, 'Asistentes VIP.'),
    ('Asistentes pagos (general + VIP)', 6000, 'La base más útil para fijar el precio de la entrada.'),
    ('Mastermind del martes', 246, 'Actividad aparte, no comparte la mayoría de los costos.'),
    ('Total de personas en el predio', 6108, 'Asistentes pagos + 100 de staff + 8 del equipo interno.'),
]:
    n = len(filas) + 1
    f(etiqueta, personas, f'=IFERROR($I${FILA_TOTAL}/B{n},"")', '', nota)

f()
f('ESTADO DE LOS RUBROS')
for etiqueta, criterio in [
    ('Contratado (hay contrato o anticipo pagado)', 'Contratado'),
    ('Cotizado (hay presupuesto formal por mail)', 'Cotizado'),
    ('Sin cotizar (sólo estimado del sheet, o nada)', 'Sin cotizar'),
    ('Alternativas descartadas (NO suman al total)', 'Alternativa'),
]:
    f(etiqueta, '', f'=SUMIF($D${FILA_HDR+1}:$D${FILA_TOTAL-1},"{criterio}",$I${FILA_HDR+1}:$I${FILA_TOTAL-1})')

f()
f('DECISIONES ABIERTAS QUE MUEVEN EL NÚMERO')
f('Decisión', 'Opción A', 'Opción B', 'Qué hay que hacer')
for dec, a, b, accion in [
 ('Sillas del público',
  'La Rural: 5.000 sillas por $42.500.000 (armado incluido)',
  'FDL Eventos: 5.500 sillas por $25.800.000 + IVA, sin armado',
  'Pedir a La Rural el costo del armado por separado. Si armar las de FDL cuesta menos que la diferencia (unos US$7.350), conviene FDL.'),
 ('Técnica',
  'Prina integral: $48.885.000 + IVA',
  'Por partes: VMG sólo LED $12.625.000 + IVA, más sonido e iluminación aparte',
  'La cotización de Prina venció en junio. Revalidar con Prina, Sound-Light y Dixi sobre el mismo pliego.'),
 ('Catering',
  'AmbientHouse: $28.500 + IVA por persona por día, base mínima 480',
  'Teist: propuesta del 26/06 sin cerrar',
  'Es el hueco más grande. Definir alcance y pedir tres cotizaciones comparables esta semana.'),
 ('Vuelos y alojamiento del equipo', 'Sin cotizar', 'Sin cotizar',
  'No hay ni un mail ni una línea en el sheet. Con 8 personas, es plata que hoy no está en ningún número.'),
 ('Facturación al exterior',
  'FDL Eventos y Vittal no confirmaron si pueden facturar a la empresa de EE.UU.',
  'Buscar proveedores que sí facturen, o resolver un circuito de pago local',
  'Resolverlo antes de firmar: puede trabar los dos contratos.'),
]:
    f(dec, a, b, accion)

f()
f('CÓMO LEER ESTA HOJA')
for t in [
 'Contratado = hay contrato firmado o anticipo pagado. Cotizado = hay presupuesto formal por mail. Alternativa = segunda opción del mismo ítem, NO suma al total. Sin cotizar = sólo hay un estimado del sheet, o ni eso.',
 'La columna "Total USD" toma la cotización real cuando existe y cae al estimado del sheet cuando no hay cotización.',
 'Las cotizaciones argentinas vienen casi todas sin IVA: la columna IVA aplica la alícuota de cada una (21% general, 10,5% el servicio médico).',
 'Los pesos son de la fecha de cada cotización, no de hoy. Prina venció en junio, VMG recotiza si el dólar salta más de 15% y La Rural ajusta el saldo por IPC.',
 'Catering entra con el estimado del sheet. Vuelos y alojamiento del equipo entran en cero porque no hay ni estimado: el costo por persona es un piso, no un techo.',
]:
    f('', t)

sal = io.StringIO()
csv.writer(sal, lineterminator='\n').writerows(filas)
open('argentina_costo_total.csv', 'w', encoding='utf-8').write(sal.getvalue())
print('filas:', len(filas), '· fila TC:', FILA_TC, '· fila TOTAL:', FILA_TOTAL)
