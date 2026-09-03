# -*- coding: utf-8 -*-
"""Genera ahorros_argentina.csv — la hoja AHORROS del libro de Argentina, en CSV.

Existe porque el libro completo (9 pestañas, 42 KB) no se puede subir a Drive por
la conexión MCP: los binarios hay que transcribirlos enteros en un solo envío y a
ese tamaño se corta. El CSV sí sube y Drive lo convierte en un Sheet nativo.

Los números son los mismos que la hoja AHORROS de ARGENTINA_CMC2026_Costo_Total.xlsx:
US$102.464,15 cotizado → US$62.856,97 cerrado = US$39.607,18 (39%).
"""
import csv, io

TC = 1510.0   # dólar operativo, igual que construir_argentina.py

# (rubro, referencia cotizada, ref USD, lo que se cerró, cerrado USD)
AHORROS = [
    ('Infraestructura — armado de stands',
     'La Rural: panelería + dirección técnica + guardias', 16858366.2 / TC,
     'Armado del stand de staff, el de producción y el camarín', 9270.0),
    ('Mobiliario — sillas y montaje',
     'La Rural: 5.000 sillas imperio bordó, armado incluido', 28431.0,
     'FDL Eventos: 5.500 sillas + flete, más montaje, acomodación y desmontaje', 17450.0),
    ('Entelado', 'Primer presupuesto recibido', 25490.0,
     'Negociado por Agustina', 16500.0),
    ('Catering', 'Primera propuesta de Grupo Ambient', 30000000.0 / TC,
     '600 lunchbox VIP + desayuno, almuerzo y cena para 150 personas', 14569.0),
    ('Merch e impresos', 'Proveedor de Cumbre, precios unitarios al 06/07', 16261.12,
     'Proveedores argentinos conseguidos por Agustina', 5067.97),
    ('Vallado del público', 'Presupuestado en la hoja de Argentina', 1250.0,
     '500 vallas bonificadas por el proveedor de técnica', 0.0),
]

# Las siete cotizaciones de técnica. No entran en la tabla de ahorros: los
# alcances no son comparables y el número no se sostendría ante el CEO.
TECNICA = [
    ('Sound-Light', '16/06', 'por encima de $100.000.000',
     'El PDF no se pudo abrir (mail de 33 MB). El mail del 19/06 les dice que las otras '
     'estaban "prácticamente la mitad".'),
    ('Bonetto', '17/06', '$94.936.000',
     'Sonido e iluminación 69,7M + LED 20,7M + CCTV 4,5M. Grúas y efectos aparte: '
     'la chispa fría la cobra POR MINUTO.'),
    ('Dixi Group', '26/06', '$99.220.000 c/IVA',
     'Llave en mano, rigging completo, encomiendas y 4 máquinas de chispa fría.'),
    ('Prina', '18/06', '$59.150.850 c/IVA',
     'VENCIDA. Cotiza 40 m² de LED cuando el rider pide 65, y deja afuera grúas y energía.'),
    ('2MG', '24/06', '$54.450.000 c/IVA + $19.202.700 de adicionales',
     'Sonido más liviano, cotizado para "2000 / 5000 pax".'),
    ('VMG', '29/06', '$15.276.250 c/IVA', 'Sólo las pantallas LED de 65 m².'),
    ('GRUPO MET (contratado)', '—', 'US$60.000 = $90.600.000',
     'Con el circuito cerrado el paquete queda cerca de $100.000.000.'),
]

filas = []
def f(*c): filas.append(list(c))

f('AHORROS · ARGENTINA — CUMBRE DE LOS MILLONARIOS CONSCIENTES 2026')
f('Lo cotizado contra lo que se cerró · corte al 02/09/2026 · dólar $1.510')
f()
f('Rubro', 'Referencia cotizada', 'Ref. USD', 'Lo que se cerró', 'Cerrado USD',
  'Ahorro USD', '% ahorro')
total_ref = total_cerrado = 0.0
for rubro, ref, ref_usd, cerrado, cerrado_usd in AHORROS:
    total_ref += ref_usd
    total_cerrado += cerrado_usd
    ahorro = ref_usd - cerrado_usd
    f(rubro, ref, round(ref_usd, 2), cerrado, round(cerrado_usd, 2),
      round(ahorro, 2), '{:.0%}'.format(ahorro / ref_usd))
f('AHORRO TOTAL', '', round(total_ref, 2), '', round(total_cerrado, 2),
  round(total_ref - total_cerrado, 2),
  '{:.0%}'.format((total_ref - total_cerrado) / total_ref))
f()
f('TÉCNICA — la comparación no es directa, por eso no entra en la tabla de arriba')
f('Se pidió cotización a NUEVE empresas el 13 y 14 de junio. Respondieron seis con número.')
f('Proveedor', 'Fecha', 'Monto', 'Qué incluye')
for fila in TECNICA:
    f(*fila)
f()
for t in [
 'POR QUÉ NO SE CUENTA COMO AHORRO: Grupo MET es prácticamente lo mismo que Dixi llave en mano y menos que Bonetto,',
 'pero está POR ENCIMA de 2MG y de Prina. Los alcances no son iguales: Prina cotizó 38% menos de LED, 2MG un sonido',
 'más chico, y Grupo MET incluye lo que se agregó tras la visita al predio. Ponerlo como ahorro no se sostendría ante el CEO.',
 '',
 'LO QUE SÍ SE SOSTIENE: las 500 vallas y los efectos especiales van bonificados. Bonetto los cobra: $300.000 la máquina',
 'de humo y $600.000 POR MINUTO las dos de chispa fría. Con los 6 disparos por día que pide el rider, en cualquier otra',
 'propuesta eso es plata. Ese es el renglón "Vallado del público" de la tabla de arriba.',
 '',
 'FALTA UNA SOLA COSA para cerrar el ahorro de técnica con un número: el PDF de Grupo MET con el alcance final.',
 'Es el único de los siete proveedores sin presupuesto escrito en el correo.',
]:
    f(t) if t else f()

sal = io.StringIO()
csv.writer(sal, lineterminator='\n').writerows(filas)
io.open('ahorros_argentina.csv', 'w', encoding='utf-8').write(sal.getvalue())
print('AHORRO TOTAL: {:,.2f} -> {:,.2f} = {:,.2f} ({:.0%})'.format(
    total_ref, total_cerrado, total_ref - total_cerrado,
    (total_ref - total_cerrado) / total_ref))
