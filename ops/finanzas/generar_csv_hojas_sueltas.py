# -*- coding: utf-8 -*-
"""Vuelca TABLERO, MERCH, DECISIONES e INFRAESTRUCTURA a CSV, con los valores ya calculados.

Son las cuatro pestañas del libro de Argentina que no están en Drive. El libro
entero no se puede subir por la conexión MCP (los binarios hay que transcribirlos
completos y a ese tamaño fallan), pero el texto sí, y Drive convierte cada CSV en
un Sheet nativo.

Las fórmulas no sobreviven a la importación CSV, así que acá se resuelven en
Python y va el número. Los estados se suman desde argentina_costo_total.csv, que
ya trae los valores de COSTOS UNIFICADOS.

Un arreglo respecto del .xlsx: el bloque "ESTADO DE LOS RUBROS" de TABLERO listaba
Contratado, Cotizado, Sin cotizar y Alternativa, y se dejaba afuera Cerrado
(US$106.273, el balde más grande) y En negociación. Sumaba US$135.477 contra un
total de US$242.347. Acá van los seis estados y cierra.
"""
import csv, io, collections, openpyxl

TC = 1510.0
LIBRO = 'ARGENTINA_CMC2026_Costo_Total.xlsx'

# ---- valores de COSTOS UNIFICADOS, desde el CSV de valores estáticos ----------
por_estado = collections.OrderedDict()
total_usd = estimado = 0.0
for fila in csv.reader(io.open('argentina_costo_total.csv', encoding='utf-8')):
    if len(fila) < 12 or not fila[3]:
        continue
    try:
        usd = float(fila[9]) if fila[9] else 0.0
    except ValueError:
        continue
    if fila[0].startswith('Subtotal') or fila[3] == 'Estado':
        continue
    por_estado[fila[3]] = por_estado.get(fila[3], 0.0) + usd
    if fila[3] != 'Alternativa':      # las alternativas descartadas no suman
        total_usd += usd
    if fila[10]:
        try: estimado += float(fila[10])
        except ValueError: pass

wb = openpyxl.load_workbook(LIBRO)

def escribir(nombre, filas):
    sal = io.StringIO()
    csv.writer(sal, lineterminator='\n').writerows(filas)
    io.open(nombre, 'w', encoding='utf-8').write(sal.getvalue())
    print('{:<34} {:>3} filas'.format(nombre, len(filas)))

def limpiar(fila):
    v = ['' if c is None else c for c in fila]
    while v and v[-1] == '': v.pop()
    return v

# ---------------------------------------------------------------- TABLERO
f = []
f.append(['Argentina en una pantalla'])
f.append(['La Rural · Pabellón Azul · 3 y 4 de octubre de 2026'])
f.append(['Valores calculados al 02/09/2026. La versión editable, con fórmulas, es el .xlsx.'])
f.append([])
f.append(['Tipo de cambio (ARS por USD)', '', TC, '',
          'Dólar con el que trabaja Agustina. Verificado contra dos de sus cifras: '
          '$900.000 de montaje = US$596 y $24.500.000 de entelado = US$16.225.'])
f.append([])
f.append(['COSTO DEL EVENTO'])
f.append(['Costo total (cotizaciones reales + estimados)', '', round(total_usd, 2), '',
          'Suma de contratado, cotizado y lo que sólo tiene estimado. No incluye las alternativas descartadas.'])
f.append(['Lo que decía el presupuesto original', '', round(estimado, 2), '',
          'Total de la hoja "Argentina (3 oct-4 oct)" del master.'])
f.append(['Diferencia contra el presupuesto', '', round(total_usd - estimado, 2), '',
          'Cuánto se corre el evento respecto de lo presupuestado, con los precios que hoy están sobre la mesa.'])
f.append([])
f.append(['COSTO POR PERSONA'])
f.append(['Base de cálculo', 'Personas', 'Costo por persona', '', 'Qué incluye'])
for base, pax, nota in [
    ('Aforo general', 5000, 'Asistentes de entrada general según la hoja del master.'),
    ('VIP', 1000, 'Asistentes VIP.'),
    ('Asistentes pagos (general + VIP)', 6000, 'La base más útil para decidir el precio de la entrada.'),
    ('Mastermind del martes', 246, 'Actividad aparte, no comparte la mayoría de los costos.'),
    ('Total de personas en el predio', 6108, 'Asistentes pagos + 100 de staff + 8 del equipo interno.'),
]:
    f.append([base, pax, round(total_usd / pax, 2), '', nota])
f.append([])
f.append(['ESTADO DE LOS RUBROS'])
f.append(['Estado', '', 'USD', '', 'Qué hay adentro'])
NOTAS = {
    'Cerrado': 'Técnica, entelado, CCTV, catering, infraestructura y montaje: cerrados por Agustina.',
    'Contratado': 'Sede, las nueve facturas de merch e intercoms.',
    'Cotizado': 'Sillas, WiFi, seguridad, servicio médico, limpieza, retiro de residuos y seguro.',
    'En negociación': 'Montaje, acomodación y desmontaje de las sillas.',
    'Sin cotizar': 'Ecobaños, marquetería, replanteo de sillas y cheques/escarapelas/diplomas. Definidos por Agustina, todavía sin precio.',
    'Alternativa': 'Cotización descartada de Blocko. NO suma al costo.',
    'Bonificado': 'Vallas, efectos especiales y food trucks: sin cargo.',
    'Otro pais': 'Gráfica de Uruguay. NO suma al costo de Argentina.',
    'Reemplazado': 'Estimado global de merch del master, ya cubierto por las facturas reales.',
}
suma_estados = 0.0
for estado in ['Cerrado', 'Contratado', 'Cotizado', 'En negociación', 'Sin cotizar',
               'Alternativa', 'Bonificado', 'Otro pais', 'Reemplazado']:
    if estado in por_estado:
        f.append([estado, '', round(por_estado[estado], 2), '', NOTAS.get(estado, '')])
        if estado not in ('Alternativa', 'Bonificado', 'Otro pais', 'Reemplazado'):
            suma_estados += por_estado[estado]
f.append(['SUMA (sin alternativas ni bonificados)', '', round(suma_estados, 2), '',
          'Tiene que dar igual al costo total de arriba.'])
escribir('tablero_argentina.csv', f)

# ------------------------------------------------------- MERCH / DECISIONES / INFRA
# Estas tres se leen del libro y se les resuelven las fórmulas conocidas.
def valor_merch(ws, fila, col, crudo):
    """Resuelve las fórmulas de MERCH: totales con IVA, imputación por país y ahorros."""
    F = lambda c: ws.cell(fila, c).value or 0
    if col == 8:                                   # Total con IVA = F*(1+IVA)
        return round(F(6) * (1 + (F(7) or 0)), 2)
    if col == 12:                                  # Costo Argentina = %arg * total / TC
        return round(F(11) * (F(6) * (1 + (F(7) or 0))) / TC, 2)
    if col in (13, 14) and isinstance(crudo, str): # Falta pagar = %arg * literal
        lit = float(crudo.split('*')[-1])
        return round(F(11) * lit, 2)
    return crudo

ws = wb['MERCH']
f = []
for i, fila in enumerate(ws.iter_rows(min_row=1, max_row=ws.max_row), start=1):
    linea = []
    for j, celda in enumerate(fila, start=1):
        v = celda.value
        if isinstance(v, str) and v.startswith('='):
            if 5 <= i <= 12:
                v = valor_merch(ws, i, j, v)
            elif i == 13 and j in (12, 13, 14):    # totales de la tabla de facturas
                v = round(sum(valor_merch(ws, r, j, ws.cell(r, j).value) for r in range(5, 13)), 2)
            elif 25 <= i <= 41:                    # canasta: ahorro y %
                D, F_ = ws.cell(i, 4).value, ws.cell(i, 6).value
                num = isinstance(D, (int, float)) and isinstance(F_, (int, float))
                if j == 7 and num: v = round(D - F_, 2)
                elif j == 8 and num and D: v = round((D - F_) / D, 4)
                else: v = ''
            else:
                v = ''
        linea.append('' if v is None else v)
    while linea and linea[-1] == '': linea.pop()
    f.append(linea)
# subtotales de la canasta, que son SUMIF sobre filas con precio de Agustina
def canasta(desde, hasta):
    d = s = 0.0
    for r in range(desde, hasta + 1):
        if ws.cell(r, 6).value is not None:
            d += ws.cell(r, 4).value or 0
            s += ws.cell(r, 6).value or 0
    return round(d, 2), round(s, 2), round(d - s, 2), round((d - s) / d, 4)
for fila_idx, (desde, hasta) in [(33, (25, 32)), (40, (35, 39))]:
    d, s, a, p = canasta(*(desde, hasta))
    f[fila_idx - 1] = [f[fila_idx - 1][0], '', '', d, '', s, a, p]
d1, s1, a1, _ = canasta(25, 32); d2, s2, a2, _ = canasta(35, 39)
f[40] = ['TOTAL DE LA CANASTA — ARGENTINA + URUGUAY', '', '', round(d1 + d2, 2), '',
         round(s1 + s2, 2), round(a1 + a2, 2), round((a1 + a2) / (d1 + d2), 4)]
f.insert(2, ['Valores calculados al 02/09/2026. La versión editable, con fórmulas, es el .xlsx.'])
escribir('merch_argentina.csv', f)

ws = wb['DECISIONES']
f = []
for fila in ws.iter_rows(min_row=1, max_row=ws.max_row):
    linea = []
    for celda in fila:
        v = celda.value
        if isinstance(v, str) and v.startswith('='):
            expr = v[1:].replace('TABLERO!$C$4', str(TC))
            try: v = round(eval(expr), 2)
            except Exception: v = ''
        linea.append('' if v is None else v)
    while linea and linea[-1] == '': linea.pop()
    f.append(linea)
f.insert(2, ['Valores calculados al 02/09/2026. La versión editable, con fórmulas, es el .xlsx.'])
escribir('decisiones_argentina.csv', f)

ws = wb['INFRAESTRUCTURA']
f = []
total_ars = queda_ars = 0.0
for i, fila in enumerate(ws.iter_rows(min_row=1, max_row=ws.max_row), start=1):
    linea = []
    for j, celda in enumerate(fila, start=1):
        v = celda.value
        if isinstance(v, str) and v.startswith('='):
            precio, se_queda = ws.cell(i, 4).value, ws.cell(i, 6).value
            if j == 5 and isinstance(precio, (int, float)):      # USD
                v = round(precio / TC, 2)
            elif j == 7:                                          # si se queda (ARS)
                v = precio if se_queda == 'SÍ' else 0
            else:
                v = ''
        linea.append('' if v is None else v)
    if 6 <= i <= 39 and isinstance(ws.cell(i, 4).value, (int, float)):
        total_ars += ws.cell(i, 4).value
        if ws.cell(i, 6).value == 'SÍ': queda_ars += ws.cell(i, 4).value
    while linea and linea[-1] == '': linea.pop()
    f.append(linea)
for idx, (etiqueta, ars) in [(41, ('TOTAL del presupuesto de La Rural', None)),
                             (42, ('Lo que se queda (marcado SÍ)', None)),
                             (43, ('Lo que se saca (marcado NO)', None))]:
    ars = {41: total_ars, 42: queda_ars, 43: total_ars - queda_ars}[idx]
    f[idx - 1] = ['', '', etiqueta, round(ars, 2), round(ars / TC, 2)]
f.insert(2, ['Valores calculados al 02/09/2026. Los SÍ/NO son la selección de hoy; '
             'para cambiarlos y que recalcule, usá el .xlsx.'])
escribir('infraestructura_argentina.csv', f)

print('\nCosto total {:,.2f} · suma por estado {:,.2f} · diferencia {:,.2f}'.format(
    total_usd, suma_estados, total_usd - suma_estados))
