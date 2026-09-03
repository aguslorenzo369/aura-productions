# -*- coding: utf-8 -*-
"""Checklist de pagos de Argentina. Debe cerrar contra el total del evento."""
import importlib.util, sys, csv, io
spec = importlib.util.spec_from_file_location('gen', 'construir_argentina.py')
m = importlib.util.module_from_spec(spec); sys.modules['gen'] = m; spec.loader.exec_module(m)
TC = m.TC_DEFECTO

def pct(it): return it[10] if len(it) > 10 else 1.0
def usd(it):
    _, ru, pr, de, mon, monto, iva, est, e, fu = it[:10]
    if est in ('Bonificado', 'Reemplazado'): return 0.0
    if monto:
        b = monto * (1 + iva)
        return pct(it) * (b if mon == 'USD' else b / TC)
    return pct(it) * e
TOTAL = sum(usd(i) for i in m.ITEMS if i[7] != 'Alternativa')

MET   = 'Grupo MET · Lalo Aizenberg'
RURAL = 'La Rural'
# (tramo, rubro, proveedor, concepto, a_pagar, vence, como, contacto, telefono, nota)
FILAS = [
 ('1 · VENCIDO O YA FACTURADO', 'Sede', RURAL, 'Saldo del contrato CC-00957, cuota 1 de 2',
  15777.00, '24 ago — VENCIDA', 'Transferencia', 'Victoria Grosi · vgrosi@larural.com.ar',
  'congresosyeventos@larural.com.ar', 'Lleva 10 días vencida.'),
 ('1 · VENCIDO O YA FACTURADO', 'Merch', 'REMERASYESTAMPADOS', 'Remeras premium x250 — factura 2601017',
  2780.64, 'facturado 16 ago', 'USDT BEP20', 'Leandro Petracci · CUIT 20-30367082-4',
  'Uruguay 41, Villa Martelli', 'Wallet 0xae874c3db52ca1e45604549a5527f450a877b97a'),
 ('1 · VENCIDO O YA FACTURADO', 'Merch', 'REMERASYESTAMPADOS', 'Bordado de 940 gorras — factura 2601016',
  1721.95, 'facturado 10 ago', 'USDT BEP20', 'Leandro Petracci · CUIT 20-30367082-4',
  'Uruguay 41, Villa Martelli', 'Mismo wallet que las remeras.'),

 ('2 · ANTICIPOS QUE DESTRABAN CONTRATOS', 'Técnica', MET, 'Producción técnica — resto del anticipo del 50%',
  25000.00, 'urgente', 'Transferencia / Mercury', 'Lalo Aizenberg', '11 6411-6748',
  'El 50% son US$30.000; ya se pagaron US$5.000 con la factura INV-11 del 31/07.'),
 ('2 · ANTICIPOS QUE DESTRABAN CONTRATOS', 'Catering', 'Grupo Ambient · Ángeles', 'Catering — anticipo del 50%',
  7284.50, 'urgente', 'Transferencia', 'Ángeles', 'angeles@grupoambient.com.ar',
  'Total cerrado US$14.569 por las dos propuestas.'),

 ('3 · PROVEEDORES DEL PREDIO — firmar y señar', 'Mobiliario', 'FDL Eventos · Federico', '5.500 sillas + flete',
  20674.17, 'a definir', 'A resolver', 'Federico', '11 4403-0698 / 11 4040-7012',
  'PENDIENTE: no confirmaron si pueden facturar al exterior. Lo hacen con un tercero que emite en EE.UU.'),
 ('3 · PROVEEDORES DEL PREDIO — firmar y señar', 'Infraestructura', RURAL, 'Armado de stands',
  9270.00, 'a definir', 'Transferencia', 'Arq. Christian Riccio', '+54 9 11 3481-2179',
  'criccio@larural.com.ar · falta pedirle los espejos.'),
 ('3 · PROVEEDORES DEL PREDIO — firmar y señar', 'Servicios', 'Road Seguridad S.A.', '263 h de vigilancia + planos + supervisión',
  5784.70, 'a definir', 'Transferencia', 'Javier Celiz', 'Cel 11 6303-7845 · Of. 4756-5691',
  'presupuestos@roadseguridad.com.ar · versión V3 del 12/08, lista para firmar.'),
 ('3 · PROVEEDORES DEL PREDIO — firmar y señar', 'Servicios', 'Vittal', 'Servicio médico, 3 días',
  4658.94, 'a definir', 'A resolver', 'vtomas@vittal.com.ar', '—',
  'PENDIENTE: tampoco confirmaron si pueden facturar al exterior.'),
 ('3 · PROVEEDORES DEL PREDIO — firmar y señar', 'Servicios', 'Higia Eventos', 'Limpieza, 205,5 h — ANTICIPO 50%',
  1349.21, 'antes del armado', 'Transferencia', 'Malena Carrizo / Yanina Cruz', 'malena.carrizo@higiaeventos.com',
  'Piden 50% de anticipo antes del armado. El saldo (US$1.349) va contra el evento.'),
 ('3 · PROVEEDORES DEL PREDIO — firmar y señar', 'Servicios', 'Gale Servicios', 'Retiro de residuos — 100% ADELANTADO',
  1179.24, 'antes del evento', 'Transferencia', 'Yanina Cruz', 'info@galeservicios.com',
  'Se factura 100% por adelantado. Trabajan con ARCILLEX; hay que estar dado de alta como generador.'),
 ('3 · PROVEEDORES DEL PREDIO — firmar y señar', 'Servicios', RURAL, 'Conectividad WiFi, 2 redes privadas',
  1174.79, 'a definir', 'Transferencia', 'Gonzalo', 'conectividad@larural.com.ar',
  'Presupuesto N.º 2 del 05/08. Ajusta por IPC.'),
 ('3 · PROVEEDORES DEL PREDIO — firmar y señar', 'Servicios', 'Chanes Seguros', 'Seguro de accidentes, 150 personas',
  631.23, 'antes del armado', 'Transferencia', 'Néstor', 'nestor@chanesseguros.com.ar',
  'Lo exige La Rural para habilitar. Premio único.'),
 ('3 · PROVEEDORES DEL PREDIO — firmar y señar', 'Mobiliario', 'A definir', 'Montaje, acomodación y desmontaje de sillas',
  596.03, 'a definir', 'Transferencia', '—', '—',
  'EN NEGOCIACIÓN: cerrar el número antes de firmar las sillas.'),

 ('4 · PROGRAMADO', 'Merch', 'REMERASYESTAMPADOS', 'Pañuelos — saldo 50% (parte Argentina)',
  3429.73, '13 sep', 'USDT BEP20', 'Leandro Petracci', 'Uruguay 41, Villa Martelli',
  'Factura 2601019 por 5.276,51 USDT; a Argentina le toca el 65%.'),
 ('4 · PROGRAMADO', 'Sede', RURAL, 'Saldo del contrato CC-00957, cuota 2 de 2',
  15777.00, '23 sep', 'Transferencia', 'Victoria Grosi', 'vgrosi@larural.com.ar', ''),
 ('4 · PROGRAMADO', 'Merch', 'DERQUI IMPRESIONES', 'Gráfica Argentina — saldo',
  1192.37, '13 sep', 'USDT BEP20', 'Germán Marino · CUIT 20-37540906-3', 'Charrúa 3366, CABA',
  'A CONFIRMAR: la factura 2601014 viene por el total, no por el saldo.'),
 ('4 · PROGRAMADO', 'Merch', 'LEOTEX', 'Lanyards — saldo',
  816.10, '13 sep', 'USDT BEP20', 'DNI 33914106', 'Marengo 4178, Villa Ballester',
  'A CONFIRMAR: la factura 2601018 viene por el total, no por el saldo.'),

 ('5 · RESTO DEL SALDO — sin fecha acordada', 'Técnica', MET, 'Producción técnica — saldo del 50%',
  30000.00, 'a definir', 'Transferencia / Mercury', 'Lalo Aizenberg', '11 6411-6748',
  'Falta el PDF con el alcance final.'),
 ('5 · RESTO DEL SALDO — sin fecha acordada', 'Técnica', MET, 'Entelado del pabellón',
  16225.17, 'a definir', 'Transferencia', 'Lalo Aizenberg', '11 6411-6748', ''),
 ('5 · RESTO DEL SALDO — sin fecha acordada', 'Técnica', MET, 'Circuito cerrado de cámaras (CCTV)',
  6209.00, 'a definir', 'Transferencia', 'Lalo Aizenberg', '11 6411-6748', 'Con grúa incluida.'),
 ('5 · RESTO DEL SALDO — sin fecha acordada', 'Catering', 'Grupo Ambient · Ángeles', 'Catering — saldo del 50%',
  7284.50, 'a definir', 'Transferencia', 'Ángeles', 'angeles@grupoambient.com.ar', ''),
 ('5 · RESTO DEL SALDO — sin fecha acordada', 'Servicios', 'Higia Eventos', 'Limpieza — saldo del 50%',
  1349.20, 'contra el evento', 'Transferencia', 'Malena Carrizo', 'malena.carrizo@higiaeventos.com', ''),

 ('6 · SIN COTIZAR — pedir presupuesto', 'Producción', 'A definir', 'Master Mind Hit (sala adicional)',
  3000.00, 'pedir', '—', '—', '—', 'Estimado de la planilla, sin cotización.'),
 ('6 · SIN COTIZAR — pedir presupuesto', 'Producción', 'A definir', 'Unifilas',
  1200.00, 'pedir', '—', '—', '—', 'Estimado de la planilla.'),
 ('6 · SIN COTIZAR — pedir presupuesto', 'Producción', 'A definir', 'Escoltas (2)',
  1000.00, 'pedir', '—', '—', '—', 'Estimado de la planilla.'),
 ('6 · SIN COTIZAR — pedir presupuesto', 'Producción', 'A definir', 'DJ',
  500.00, 'pedir', '—', '—', '—', 'Estimado de la planilla.'),
 ('6 · SIN COTIZAR — pedir presupuesto', 'Servicios', 'A definir', 'Ecobaños',
  0.00, 'pedir', '—', '—', '—', 'Decidido que van ecobaños. Sin cotizar: hoy entra en cero.'),
 ('6 · SIN COTIZAR — pedir presupuesto', 'Merch', 'A definir', 'Marquetería y enmarcado',
  0.00, 'pedir', '—', '—', '—', 'Certificaciones y premios. Sin cotizar.'),
 ('6 · SIN COTIZAR — pedir presupuesto', 'Merch', 'A definir', 'Cheques, escarapelas, diplomas, placas y manillas',
  0.00, 'pedir', '—', '—', '—', 'Lo único del merch que las facturas no cubren.'),
 ('6 · SIN COTIZAR — pedir presupuesto', 'Mobiliario', 'A definir', 'Replanteo de sillas con ingeniero',
  0.00, 'pedir', '—', '—', '—', 'Va aparte de la dirección técnica de La Rural.'),
 ('6 · SIN COTIZAR — pedir presupuesto', 'Equipo', 'A definir', 'Vuelos, alojamiento y traslados del equipo (8 personas)',
  0.00, 'pedir', '—', '—', '—', 'El hueco más grande: no hay cotización ni estimado.'),
]

PAGADO = 55891.15
falta = TOTAL - PAGADO
suma = sum(f[4] for f in FILAS)
print('Costo total del evento     {:>12,.2f}'.format(TOTAL))
print('Ya pagado                  {:>12,.2f}'.format(PAGADO))
print('Falta desembolsar          {:>12,.2f}'.format(falta))
print('Suma del checklist         {:>12,.2f}'.format(suma))
print('Diferencia                 {:>12,.2f}'.format(falta - suma))
print()
tramos = {}
for f in FILAS: tramos[f[0]] = tramos.get(f[0], 0.0) + f[4]
for t in sorted(tramos): print('  {:<44} {:>12,.2f}'.format(t, tramos[t]))

FILAS.append(('7 · AJUSTE DE CONCILIACIÓN', 'Merch', '—', 'Diferencia de tipo de cambio y saldo de gráfica a confirmar',
              round(falta - suma, 2), '—', '—', '—', '—',
              'Las facturas de merch se emitieron a dólar $1.535 y los pagos de junio se hicieron a $1.475, '
              'así que las mitades no suman exacto. El grueso es el saldo de la gráfica de Argentina: el master '
              'dice US$1.839 y la factura 2601014 viene por US$2.385.'))

filas = []
def f(*c): filas.append(list(c))
f('CHECKLIST DE PAGOS · ARGENTINA · CUMBRE DE LOS MILLONARIOS CONSCIENTES 2026')
f('La Rural, Pabellón Azul · montaje 2 de octubre · evento 3 y 4 · corte al 2 de septiembre · dólar $1.510')
f()
f('Costo total del evento', round(TOTAL, 2))
f('Ya pagado', round(PAGADO, 2))
f('FALTA DESEMBOLSAR', round(falta, 2))
f()
f('Pagado', 'Prioridad', 'Rubro', 'Proveedor', 'Concepto', 'A pagar (USD)', 'Cuándo',
  'Cómo se paga', 'Contacto', 'Teléfono / mail', 'Notas')
tramo_actual = None
for tr, rubro, prov, conc, monto, vence, como, cont, tel, nota in FILAS:
    if tr != tramo_actual:
        tramo_actual = tr
        f('', tr, '', '', '', round(tramos.get(tr, monto if tr.startswith('7') else 0), 2))
    f('☐', '', rubro, prov, conc, round(monto, 2), vence, como, cont, tel, nota)
f()
f('TOTAL DEL CHECKLIST', '', '', '', '', round(sum(x[4] for x in FILAS), 2))
f()
f('CONTACTOS')
f('Proveedor', 'Persona', 'Mail', 'Teléfono')
for prov, per, mail, tel in [
 ('La Rural — contrato y eventos', 'Victoria Grosi', 'vgrosi@larural.com.ar', 'congresosyeventos@larural.com.ar'),
 ('La Rural — infraestructura', 'Arq. Christian Riccio', 'criccio@larural.com.ar', '+54 9 11 3481-2179'),
 ('La Rural — conectividad', 'Gonzalo', 'conectividad@larural.com.ar', '—'),
 ('Grupo MET — técnica y entelado', 'Lalo Aizenberg', 'lalo@somosgrupomet.com', '11 6411-6748'),
 ('Grupo Ambient — catering', 'Ángeles', 'angeles@grupoambient.com.ar', '—'),
 ('FDL Eventos — sillas', 'Federico', 'fdleventos@gmail.com', '11 4403-0698 / 11 4040-7012'),
 ('Road Seguridad S.A.', 'Javier Celiz', 'presupuestos@roadseguridad.com.ar', 'Cel 11 6303-7845 · Of. 4756-5691/1435'),
 ('Vittal — servicio médico', '—', 'vtomas@vittal.com.ar', '—'),
 ('Higia Eventos — limpieza', 'Malena Carrizo / Yanina Cruz', 'malena.carrizo@higiaeventos.com', 'yanina.cruz@higiaeventos.com'),
 ('Gale Servicios — residuos', 'Yanina Cruz', 'info@galeservicios.com', '—'),
 ('Chanes Seguros', 'Néstor', 'nestor@chanesseguros.com.ar', '—'),
 ('REMERASYESTAMPADOS — pañuelos, remeras, bordado', 'Leandro Petracci', 'CUIT 20-30367082-4', 'Uruguay 41, Villa Martelli'),
 ('DERQUI IMPRESIONES — gráfica', 'Germán Marino', 'CUIT 20-37540906-3', 'Charrúa 3366, CABA'),
 ('LEOTEX — lanyards', '—', 'DNI 33914106', 'Marengo 4178, Villa Ballester'),
 ('TEXTIL RYU — gorras', '—', 'CUIT 30-71927319-6', 'Larrea 377, Balvanera · YA PAGADO'),
]:
    f(prov, per, mail, tel)
f()
f('CÓMO USAR ESTA HOJA')
for t in [
 'Marcá la columna "Pagado" con una X a medida que salen los pagos.',
 'Los tramos están ordenados por urgencia: el 1 son cosas vencidas o ya facturadas, el 2 son los anticipos del 50% que destraban los contratos de técnica y catering.',
 'Los pagos de merch van en USDT por red BEP20. La wallet de Remerasyestampados es 0xae874c3db52ca1e45604549a5527f450a877b97a y la de Leotex y Derqui es 0x7d0a6c347008305af1d6643c2382e1495af7dc0e. Verificá siempre la dirección con el proveedor antes de operar.',
 'FDL Eventos (sillas) y Vittal (servicio médico) todavía no confirmaron si pueden facturar a la empresa de EE.UU. Es lo primero a resolver de los dos.',
 'Higia pide 50% de anticipo antes del armado y Gale factura el 100% por adelantado: esos dos hay que pagarlos antes del evento sí o sí.',
]:
    f('', t)

sal = io.StringIO(); csv.writer(sal, lineterminator='\n').writerows(filas)
io.open('checklist_pagos_argentina.csv', 'w', encoding='utf-8').write(sal.getvalue())
print('\nfilas del CSV:', len(filas))
print('TOTAL del checklist: {:,.2f}  (falta desembolsar {:,.2f})'.format(sum(x[4] for x in FILAS), falta))
