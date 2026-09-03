# -*- coding: utf-8 -*-
"""Genera el CSV de una sola hoja para subir a Google Sheets.

Las fórmulas NO sobreviven la importación de un CSV a Google Sheets (las celdas
quedan en blanco), así que acá se escriben los valores ya calculados. La versión
con fórmulas vivas es el .xlsx que arma construir_argentina.py.
"""
import csv, io

fuente = open('construir_argentina.py', encoding='utf-8').read()
ns = {}
exec(fuente[fuente.index('ARS_, USD_ ='):fuente.index('# ====', fuente.index('ARS_, USD_ ='))], ns)
ITEMS = ns['ITEMS']
ini_m = fuente.index('MERCH = [')
exec(fuente[ini_m:fuente.index('\n]\n', ini_m) + 3], ns)
MERCH = ns['MERCH']

TC = 1510.0   # dólar operativo de Agustina

def pct_de(it):
    return it[10] if len(it) > 10 else 1.0

def total_usd(it):
    (_, rubro, prov, det, mon, monto, iva, estado, est, fuente_txt) = it[:10]
    if estado in ('Bonificado', 'Reemplazado'):
        return 0.0
    if monto:
        bruto = monto * (1 + iva)
        return pct_de(it) * (bruto if mon == 'USD' else bruto / TC)
    return pct_de(it) * est

def total_origen(it):
    monto, iva = it[5], it[6]
    return monto * (1 + iva) if monto else ''

filas = []
def f(*c): filas.append(list(c))

f('ARGENTINA · CUMBRE DE LOS MILLONARIOS CONSCIENTES 2026')
f('La Rural, Pabellón Azul · montaje 2 de octubre · evento 3 y 4 de octubre de 2026')
f('Corte al 02/09/2026. Incluye los cierres de técnica, entelado, CCTV, catering y las nueve facturas de merch de la carpeta de Drive.')
f()
f('Tipo de cambio usado (ARS por USD)', TC,
  'Dólar operativo de Agustina. Verificado contra dos de sus cifras: $900.000 de montaje = US$596 y $24.500.000 de entelado = US$16.225.')
f()
f('Rubro', 'Proveedor', 'Detalle', 'Estado', 'Moneda', 'Monto sin IVA', 'IVA',
  'Total con IVA (moneda origen)', '% Argentina', 'Total USD',
  'Estimado del sheet (USD)', 'Diferencia', 'Fuente')

orden = ['Sede', 'Infraestructura', 'Mobiliario', 'Técnica', 'Servicios', 'Merch', 'Catering', 'Producción', 'Equipo']
gran_total = gran_est = 0.0
for bloque in orden:
    grupo = [x for x in ITEMS if x[0] == bloque]
    if not grupo: continue
    f(bloque.upper())
    sub = sub_est = 0.0
    for it in grupo:
        (_, rubro, prov, det, mon, monto, iva, estado, est, fuente_txt) = it[:10]
        tu = total_usd(it)
        if estado != 'Alternativa':
            sub += tu; sub_est += est
        f(rubro, prov, det, estado, mon,
          round(monto, 2) if monto else '',
          {0.21: '21%', 0.105: '10,5%'}.get(iva, 'sin IVA' if monto else ''),
          round(total_origen(it), 2) if monto else '',
          f'{pct_de(it):.0%}',
          round(tu, 2), round(est, 2) if est else '',
          round(tu - est, 2) if estado != 'Alternativa' else '',
          fuente_txt)
    f(f'Subtotal {bloque}', '', '', '', '', '', '', '', '',
      round(sub, 2), round(sub_est, 2), round(sub - sub_est, 2))
    gran_total += sub; gran_est += sub_est

f()
f('COSTO TOTAL DEL EVENTO', '', '', '', '', '', '', '', '',
  round(gran_total, 2), round(gran_est, 2), round(gran_total - gran_est, 2))

f()
f('COSTO POR PERSONA')
f('Base de cálculo', 'Personas', 'Costo por persona (USD)', '', 'Qué incluye')
for etiqueta, personas, nota in [
    ('Aforo general', 5000, 'Asistentes de entrada general.'),
    ('VIP', 1000, 'Asistentes VIP.'),
    ('Asistentes pagos (general + VIP)', 6000, 'La base más útil para fijar el precio de la entrada.'),
    ('Mastermind del martes', 246, 'Actividad aparte.'),
    ('Total de personas en el predio', 6108, 'Pagos + 100 de staff + 8 del equipo interno.'),
]:
    f(etiqueta, personas, round(gran_total / personas, 2), '', nota)

f()
f('ESTADO DE LOS RUBROS', '', 'USD')
por_estado = {}
for it in ITEMS:
    por_estado[it[7]] = por_estado.get(it[7], 0.0) + total_usd(it)
for e, v in sorted(por_estado.items(), key=lambda x: -x[1]):
    f(e, '', round(v, 2))

f()
f('MERCH · FACTURA POR FACTURA')
f('Proveedor', 'Ítem', 'Cant.', 'Factura', 'Fecha', 'Neto (ARS)', 'IVA', 'Total (ARS)',
  'USDT de la factura', 'País', '% Argentina', 'Costo Argentina (USD)',
  'Falta pagar · regla 50%', 'Falta pagar · según factura', 'Nota')
t_arg = t_regla = t_fact = 0.0
for (prov, item, cant, fact, fecha, neto, iva, usdt, pais, pct, pagado, fr, ff, nota) in MERCH:
    bruto = neto * (1 + iva)
    ca = pct * bruto / TC
    t_arg += ca; t_regla += pct * fr; t_fact += pct * ff
    f(prov, item, cant, fact, fecha, round(neto, 2),
      {0.21: '21%'}.get(iva, 'sin IVA'), round(bruto, 2),
      round(usdt, 2) if usdt else '', pais, f'{pct:.0%}',
      round(ca, 2), round(pct * fr, 2), round(pct * ff, 2), nota)
f('TOTAL IMPUTADO A ARGENTINA', '', '', '', '', '', '', '', '', '', '',
  round(t_arg, 2), round(t_regla, 2), round(t_fact, 2))

f()
f('CÓMO LEER ESTA HOJA')
for t in [
 'Contratado = hay contrato o anticipo pagado. Cotizado = hay presupuesto formal por mail. Alternativa = segunda opción del mismo ítem, NO suma. Otro país = gasto de otro evento de la gira, entra en cero. Reemplazado = estimado viejo ya cubierto por facturas reales, entra en cero. Sin cotizar = sólo un estimado, o nada.',
 'La columna "% Argentina" es la parte de cada compra que se le imputa a este evento. Vale 100% en casi todo. Los pañuelos son una compra compartida con Uruguay y van al 65% (5.500 de 8.500 unidades); la gráfica de Uruguay va al 0%.',
 'Las cotizaciones argentinas vienen casi todas sin IVA: la columna IVA aplica la alícuota de cada una (21% general, 10,5% el servicio médico).',
 'Los pesos son de la fecha de cada cotización, no de hoy. La Rural ajusta el saldo por IPC y las facturas de merch se emitieron a dólar blue $1.535.',
 'Vuelos y alojamiento del equipo entran en cero porque no hay ni cotización ni estimado. Tampoco están cotizados los ecobaños, la marquetería, el replanteo de sillas ni los cheques, escarapelas, diplomas, placas y manillas. El costo por persona es un piso, no un techo.',
 'Del merch: las gorras están pagadas al 100%; pañuelos, lanyards y gráfica de Argentina tienen el 50% abonado; las remeras y el bordado de gorras no tienen nada pagado.',
 'A confirmar: las facturas reemitidas de LEOTEX y Derqui vienen por el total aunque ya se abonó el 50%. Son US$2.008 de diferencia en el calendario de pagos, no en el costo.',
]:
    f('', t)

sal = io.StringIO()
csv.writer(sal, lineterminator='\n').writerows(filas)
open('argentina_costo_total.csv', 'w', encoding='utf-8').write(sal.getvalue())
print('filas:', len(filas))
print('COSTO TOTAL: US$%s · estimado original US$%s · desvio US$%s'
      % (f'{gran_total:,.2f}', f'{gran_est:,.2f}', f'{gran_total-gran_est:,.2f}'))
print('MERCH ARG: US$%s · falta(regla) US$%s · falta(factura) US$%s'
      % (f'{t_arg:,.2f}', f'{t_regla:,.2f}', f'{t_fact:,.2f}'))
