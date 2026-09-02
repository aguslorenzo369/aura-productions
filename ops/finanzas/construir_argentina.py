# -*- coding: utf-8 -*-
"""
Consolida TODOS los costos del evento de Argentina (La Rural, 3-4 oct 2026) en un solo libro.

Fuentes:
  A. Cotizaciones reales recibidas por mail (agustinalorenzog@gmail.com), jun-ago 2026.
  B. Hoja "Argentina (3 oct-4 oct)" de INVERSIÓN GIRA CUMBRE 2026.xlsx (estimados en USD).
  C. Hoja PAGOS del mismo archivo (contratos con anticipo ya pagado).
"""
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L

HOY = datetime.date(2026, 9, 2)
TC_DEFECTO = 1535.0   # dolar oficial venta, Banco Nacion, 02/09/2026

F = 'Arial'
AZUL  = Font(name=F, size=10, color='0000FF')
NEGRO = Font(name=F, size=10)
VERDE = Font(name=F, size=10, color='008000')
BOLD  = Font(name=F, size=10, bold=True)
SUB   = Font(name=F, size=9, italic=True, color='595959')
TIT   = Font(name=F, size=14, bold=True, color='1F3864')
HDR   = Font(name=F, size=10, bold=True, color='FFFFFF')
FH    = PatternFill('solid', fgColor='1F3864')
FPAIS = PatternFill('solid', fgColor='1F3864')
FBLOQ = PatternFill('solid', fgColor='DCE6F1')
FGRIS = PatternFill('solid', fgColor='F2F2F2')
FAMAR = PatternFill('solid', fgColor='FFEB9C')
FROJO = PatternFill('solid', fgColor='FFC7CE')
FVERD = PatternFill('solid', fgColor='C6EFCE')
FIN   = PatternFill('solid', fgColor='FFFF00')
THIN  = Side(style='thin', color='BFBFBF')
BOX   = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
USD   = '"US$"#,##0.00;("US$"#,##0.00);-'
USD0  = '"US$"#,##0;("US$"#,##0);-'
ARS   = '"$"#,##0;("$"#,##0);-'
PCT   = '0.0%'
FECHA = 'DD/MM/YYYY'

wb = openpyxl.Workbook()

def hoja(nombre, titulo, bajada):
    ws = wb.create_sheet(nombre)
    ws['A1'] = titulo; ws['A1'].font = TIT
    ws['A2'] = bajada; ws['A2'].font = SUB
    return ws

def encabezados(ws, fila, cols):
    for j, (t, an) in enumerate(cols, 1):
        c = ws.cell(fila, j, t); c.font = HDR; c.fill = FH; c.border = BOX
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.column_dimensions[L(j)].width = an
    ws.freeze_panes = ws.cell(fila + 1, 1)

def banda(ws, fila, texto, ncols):
    ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=ncols)
    c = ws.cell(fila, 1, texto)
    c.font = Font(name=F, size=11, bold=True, color='FFFFFF'); c.fill = FPAIS
    c.alignment = Alignment(vertical='center', indent=1)
    ws.row_dimensions[fila].height = 20
    for j in range(1, ncols + 1): ws.cell(fila, j).fill = FPAIS
    return fila + 1

# ============================================================================
# DATOS
# ============================================================================
# (bloque, rubro, proveedor, detalle, moneda, monto_sin_iva, iva, estado,
#  estimado_usd_sheet, fuente)
# estado: Contratado / Cotizado / Alternativa / Sin cotizar
ARS_, USD_ = 'ARS', 'USD'
ITEMS = [
 # ---------------- SEDE ----------------
 ('Sede', 'Alquiler Pabellón Azul', 'La Rural (contrato CC-00957)',
  'Locación 2 días de evento + 1 día de montaje', USD_, 75000.0, 0.0, 'Contratado',
  70000.0, 'Contrato CC-00957 · hoja PAGOS del master (US$43.446 abonados el 27/04)'),
 ('Sede', 'Infraestructura y mobiliario', 'La Rural — Jefatura de Infraestructura',
  'Paneles oficina producción 25 m², sala staff 100 m², depósito 64 m² (2.500 barras), camarín speakers, mobiliario, dirección técnica, guardia eléctrica y técnica. NO incluye sillas (fila aparte).',
  ARS_, 23994708.20, 0.0, 'Cotizado', 0.0,
  'Mail criccio@larural.com.ar 17/08/2026 · total del PDF $66.494.708 menos $42.500.000 de sillas'),
 ('Sede', 'Sillas del público (5.000)', 'La Rural — Infraestructura',
  'Silla imperio bordó 5.000 u. a $8.500 c/u, dentro del presupuesto de infraestructura',
  ARS_, 42500000.0, 0.0, 'Alternativa', 0.0,
  'Mail criccio@larural.com.ar 17/08/2026'),
 ('Sede', 'Sillas del público (5.500)', 'FDL Eventos',
  '4.500 sillas plásticas Munro reforzadas + 1.000 sillas hotel negro + flete. NO incluye armado.',
  ARS_, 25800000.0, 0.21, 'Cotizado', 16500.0,
  'Mail fdleventos@gmail.com 07/08/2026 · pendiente de resolver facturación al exterior'),
 ('Sede', 'Conectividad WiFi', 'La Rural — Servicios de Conectividad',
  '2 redes privadas de 30 Mbps (técnica + staff/acreditación), 2 al 4 de octubre',
  ARS_, 1438728.01, 0.21, 'Cotizado', 800.0,
  'Mail conectividad@larural.com.ar 16/06/2026'),
 # ---------------- TÉCNICA ----------------
 ('Técnica', 'Producción técnica integral', 'Prina',
  'LED 40 m² + video 4 cámaras + sonido Adamson + iluminación + estructura, staff y guardias. 50% anticipo.',
  ARS_, 48885000.0, 0.21, 'Cotizado', 34000.0,
  'Mail valentin.andina@prina.net 18/06/2026 · validez 10 días (VENCIDA)'),
 ('Técnica', 'Pantallas LED (alternativa parcial)', 'VMG',
  'Sólo pantallas LED 65 m² con operadores y traslado',
  ARS_, 12625000.0, 0.21, 'Alternativa', 0.0,
  'Mail presupuestos@vmg-web.com 29/06/2026 · recotiza si el dólar salta más de 15%'),
 # ---------------- SERVICIOS ----------------
 ('Servicios', 'Seguridad y vigilancia', 'Road Seguridad S.A.',
  '263 horas de vigilancia (armado, evento y desarme) + planos de evacuación $715.000 + supervisión general $795.000',
  ARS_, 7218928.96, 0.21, 'Cotizado', 0.0,
  'Mail presupuestos@roadseguridad.com.ar 12/08/2026 (versión V3 con las modificaciones pedidas)'),
 ('Servicios', 'Servicio médico', 'Vittal — Socorro Médico Privado',
  '1 UTIM TRI con dos médicos + enfermero/chofer, los tres días (2, 3 y 4 de octubre)',
  ARS_, 6366521.27, 0.105, 'Cotizado', 0.0,
  'Mail vtomas@vittal.com.ar 28/08/2026 · tarifas actualizadas, sin consultorio'),
 ('Servicios', 'Limpieza', 'Higia Eventos',
  '205,5 horas de limpieza: auditorio, baños y guardarropas, del 2 al 5 de octubre',
  ARS_, 3367440.91, 0.21, 'Cotizado', 0.0,
  'Mail higiaeventos 22/06/2026 (reenviado 29/06) · 50% de anticipo antes del armado'),
 ('Servicios', 'Retiro de residuos', 'Gale Servicios',
  'Roll off con disposición final incluida. Cotización base abril 2026.',
  ARS_, 1471608.62, 0.21, 'Cotizado', 0.0,
  'Mail higiaeventos 22/06/2026 (adjunto Gale) · se factura 100% por adelantado'),
 ('Servicios', 'Seguro de accidentes personales', 'Chanes Seguros',
  'Cobertura MIA (muerte, invalidez y asistencia médica) para 150 personas, exigida por La Rural',
  ARS_, 953151.93, 0.0, 'Cotizado', 400.0,
  'Mail nestor@chanesseguros.com.ar 13/07/2026 · premio único, cotizado para 15-19/07'),
 # ---------------- MERCH Y GRÁFICA ----------------
 ('Merch', 'Cintas portacredencial (1.300)', 'Blocko',
  'Cinta raso 25 mm impresa 4 colores dos caras + mosquetón zamak, $1.346 c/u',
  ARS_, 1749800.0, 0.21, 'Cotizado', 0.0,
  'Mail hola@blocko.com.ar 09/06/2026 · producción 3 semanas'),
 ('Merch', 'Pañuelos', 'Proveedor Colombia',
  'Contrato cerrado, 50% abonado el 24/06. Saldo US$5.491 programado al 13/09.',
  USD_, 10982.0, 0.0, 'Contratado', 0.0, 'Hoja PAGOS del master'),
 ('Merch', 'Lanyards', 'Proveedor Colombia',
  'Contrato cerrado, 50% abonado el 25/06. Saldo US$850 al 13/09.',
  USD_, 1698.59, 0.0, 'Contratado', 0.0, 'Hoja PAGOS del master'),
 ('Merch', 'Gorras', 'Proveedor Colombia',
  'Pagado 100% el 25/06',
  USD_, 1825.0, 0.0, 'Contratado', 5000.0, 'Hoja PAGOS del master'),
 ('Merch', 'Gráfica Argentina', 'Proveedor Colombia',
  'Contrato cerrado, saldo US$1.839 al 13/09',
  USD_, 2481.0, 0.0, 'Contratado', 0.0, 'Hoja PAGOS del master'),
 ('Merch', 'Resto de merch e impresos', 'Varios (merch desde Colombia)',
  'Contratos, cheques, escarapelas, bolsas, camisetas, mapas, diplomas, placas, manillas',
  USD_, 0.0, 0.0, 'Sin cotizar', 8689.0,
  'Estimado de la hoja Argentina del master; sin cotización argentina'),
 # ---------------- CATERING ----------------
 ('Catering', 'Catering VIP, staff y equipo', 'A definir (Teist / Ambient / Azulado)',
  'AmbientHouse cotizó viandas a $28.500 + IVA por persona por día con base mínima de 480, y se rechazó por estar a precio de consumidor final. Teist envió propuesta el 26/06 sin cerrar.',
  USD_, 0.0, 0.0, 'Sin cotizar', 33820.0,
  'Estimado de la hoja Argentina del master; ninguna cotización aceptada todavía'),
 # ---------------- PRODUCCIÓN ----------------
 ('Producción', 'Unifilas y vallado', 'A definir', 'Estimado del sheet, sin cotización',
  USD_, 0.0, 0.0, 'Sin cotizar', 2450.0, 'Hoja Argentina del master (unifilas US$1.200 + vallas US$1.250)'),
 ('Producción', 'DJ', 'A definir', 'Estimado del sheet', USD_, 0.0, 0.0, 'Sin cotizar', 500.0,
  'Hoja Argentina del master'),
 ('Producción', 'Escoltas (2)', 'A definir', 'Estimado del sheet', USD_, 0.0, 0.0, 'Sin cotizar', 1000.0,
  'Hoja Argentina del master'),
 ('Producción', 'Master Mind Hit', 'A definir', 'Sala adicional', USD_, 0.0, 0.0, 'Sin cotizar', 3000.0,
  'Hoja Argentina del master'),
 ('Producción', 'Personal logístico', 'A definir', 'La hoja del master lo tiene en US$0',
  USD_, 0.0, 0.0, 'Sin cotizar', 0.0, 'Hoja Argentina del master · valor en cero'),
 ('Producción', 'Intercoms', 'Proveedor Colombia', 'Contrato US$560, sin abonar, 2 cuotas al 24/08 y 23/09',
  USD_, 560.0, 0.0, 'Contratado', 0.0, 'Hoja PAGOS del master'),
 # ---------------- EQUIPO ----------------
 ('Equipo', 'Vuelos del equipo', 'Sin cotizar',
  'No hay ninguna cotización de vuelos a Buenos Aires en el correo ni monto en la hoja del master',
  USD_, 0.0, 0.0, 'Sin cotizar', 0.0, 'No encontrado'),
 ('Equipo', 'Alojamiento del equipo', 'Sin cotizar',
  'No hay cotización de hotel en Buenos Aires en el correo ni monto en la hoja del master',
  USD_, 0.0, 0.0, 'Sin cotizar', 0.0, 'No encontrado'),
 ('Equipo', 'Traslados internos y viáticos', 'Sin cotizar', 'Sin registro',
  USD_, 0.0, 0.0, 'Sin cotizar', 0.0, 'No encontrado'),
]

# ============================================================================
# 1. LEEME
# ============================================================================
ws = hoja('LEEME', 'Costo total del evento de Argentina · CMC 2026',
          'La Rural, Pabellón Azul — montaje 2 de octubre, evento 3 y 4 de octubre de 2026.')
ws.column_dimensions['A'].width = 30; ws.column_dimensions['B'].width = 115
filas = [
 ('Qué es esto', 'Unifica los presupuestos que llegaron por mail (jun-ago 2026) con la hoja "Argentina (3 oct-4 oct)" del master de inversión, para poder decir cuánto sale el evento de verdad y cuánto por persona.'),
 ('Fecha de corte', 'Todo calculado al 02/09/2026.'),
 ('Tipo de cambio', 'Celda TABLERO!C4, editable. Por defecto $1.535 = dólar oficial venta del Banco Nación al 02/09/2026. Todas las conversiones de pesos a dólares salen de esa única celda.'),
 ('', ''),
 ('Cómo leer los estados', 'Contratado = hay contrato o anticipo pagado. Cotizado = hay presupuesto formal por mail. Alternativa = segunda opción para el mismo ítem, NO suma al total. Sin cotizar = sólo hay un estimado del sheet, o ni eso.'),
 ('Regla del total', 'El total suma los ítems Contratado + Cotizado + Sin cotizar. Los marcados "Alternativa" quedan fuera para no duplicar (las sillas de La Rural vs las de FDL, y las LED de VMG contra la técnica integral de Prina).'),
 ('IVA', 'Las cotizaciones argentinas casi todas vienen sin IVA. La columna IVA aplica la alícuota de cada una (21% general, 10,5% el servicio médico) para llegar al costo real.'),
 ('', ''),
 ('Advertencia 1 — vencimientos', 'La cotización de Prina (técnica, el ítem más caro en pesos) tenía validez de 10 días y venció en junio. VMG se reserva recotizar si el dólar salta más de 15%. La Rural ajusta el saldo por IPC. Los pesos de este libro son de la fecha de cada cotización, no de hoy.'),
 ('Advertencia 2 — huecos', 'Catering, vuelos y alojamiento del equipo no tienen ninguna cotización cerrada. Catering entra al total con el estimado del sheet (US$39.820); vuelos y alojamiento entran en cero porque no hay ni estimado. El costo por persona es, por lo tanto, un piso.'),
 ('Advertencia 3 — facturación', 'FDL Eventos (sillas) y Vittal (servicio médico) todavía no confirmaron si pueden facturar a la empresa de EE.UU. Si no pueden, hay que resolver el circuito de pago antes de cerrar.'),
 ('', ''),
 ('Fuentes de mail', 'La Rural infraestructura (criccio@larural.com.ar, 17/08) · La Rural conectividad (16/06) · Prina (18/06) · VMG (29/06) · Road Seguridad (12/08) · Vittal (28/08) · Higia + Gale (22/06) · Chanes Seguros (13/07) · Blocko (09/06) · FDL Eventos (07/08) · AmbientHouse (16/06).'),
 ('Fuente de planilla', 'INVERSIÓN GIRA CUMBRE 2026.xlsx — hojas "Argentina (3 oct-4 oct)" y "PAGOS".'),
]
r = 4
for a, b in filas:
    ws.cell(r, 1, a).font = BOLD if a else NEGRO
    c = ws.cell(r, 2, b); c.font = NEGRO; c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.row_dimensions[r].height = 30 if b else 8
    r += 1

# ============================================================================
# 2. COSTOS UNIFICADOS
# ============================================================================
ws = hoja('COSTOS UNIFICADOS', 'Todos los costos de Argentina, bloque por bloque',
          'Una fila por concepto. "Monto a usar" toma la cotización real cuando existe y el estimado del sheet cuando no.')
COLS = [('Rubro', 34), ('Proveedor', 30), ('Detalle', 62), ('Estado', 13), ('Moneda', 8),
        ('Monto sin IVA', 15), ('IVA', 8), ('Total moneda origen', 17),
        ('Total USD', 14), ('Estimado del sheet\n(USD)', 15), ('Diferencia', 14), ('Fuente', 62)]
NC = len(COLS)
encabezados(ws, 4, COLS)

orden_bloques = ['Sede', 'Técnica', 'Servicios', 'Merch', 'Catering', 'Producción', 'Equipo']
r = 5
filas_detalle, subtotales = [], []
for bloque in orden_bloques:
    grupo = [x for x in ITEMS if x[0] == bloque]
    if not grupo: continue
    r = banda(ws, r, bloque.upper(), NC)
    ini = r
    for (_, rubro, prov, det, mon, monto, iva, estado, est, fuente) in grupo:
        ws.cell(r, 1, rubro).font = BOLD
        ws.cell(r, 2, prov).font = AZUL
        ws.cell(r, 3, det).font = NEGRO
        ws.cell(r, 4, estado).font = BOLD
        ws.cell(r, 5, mon).font = AZUL
        c = ws.cell(r, 6, monto or None); c.font = AZUL; c.number_format = ARS if mon == ARS_ else USD
        c = ws.cell(r, 7, iva or None); c.font = AZUL; c.number_format = PCT
        c = ws.cell(r, 8, f'=IF(F{r}="","",F{r}*(1+N(G{r})))'); c.font = NEGRO
        c.number_format = ARS if mon == ARS_ else USD
        c = ws.cell(r, 9, f'=IF(H{r}="",N(J{r}),IF(E{r}="USD",H{r},H{r}/TABLERO!$C$4))')
        c.font = NEGRO; c.number_format = USD
        c = ws.cell(r, 10, est or None); c.font = AZUL; c.number_format = USD
        c = ws.cell(r, 11, f'=IF(D{r}="Alternativa","",I{r}-N(J{r}))'); c.font = NEGRO; c.number_format = USD
        ws.cell(r, 12, fuente).font = SUB
        relleno = {'Contratado': FVERD, 'Cotizado': None, 'Alternativa': FGRIS, 'Sin cotizar': FAMAR}[estado]
        if relleno:
            for j in range(1, NC + 1): ws.cell(r, j).fill = relleno
        for j in range(1, NC + 1):
            ws.cell(r, j).border = BOX
            ws.cell(r, j).alignment = Alignment(wrap_text=True, vertical='top')
        ws.row_dimensions[r].height = 42
        filas_detalle.append((r, estado))
        r += 1
    ws.cell(r, 1, f'Subtotal {bloque}').font = BOLD
    c = ws.cell(r, 9, f'=SUMIF($D${ini}:$D${r-1},"<>Alternativa",$I${ini}:$I${r-1})')
    c.font = BOLD; c.number_format = USD
    c = ws.cell(r, 10, f'=SUM($J${ini}:$J${r-1})'); c.font = BOLD; c.number_format = USD
    c = ws.cell(r, 11, f'=I{r}-J{r}'); c.font = BOLD; c.number_format = USD
    for j in range(1, NC + 1): ws.cell(r, j).fill = FGRIS; ws.cell(r, j).border = BOX
    subtotales.append(r)
    r += 1

r += 1
ws.cell(r, 1, 'COSTO TOTAL DEL EVENTO').font = Font(name=F, size=12, bold=True)
for col, letra in ((9, 'I'), (10, 'J'), (11, 'K')):
    c = ws.cell(r, col, '=' + '+'.join(f'{letra}{x}' for x in subtotales))
    c.font = Font(name=F, size=12, bold=True); c.number_format = USD0; c.fill = FVERD; c.border = BOX
fila_total = r
ws.auto_filter.ref = f'A4:{L(NC)}4'

# ============================================================================
# 3. TABLERO
# ============================================================================
ws = hoja('TABLERO', 'Argentina en una pantalla', 'La Rural · Pabellón Azul · 3 y 4 de octubre de 2026')
ws.column_dimensions['A'].width = 42
for col in 'BCD': ws.column_dimensions[col].width = 18
ws.column_dimensions['E'].width = 76

ws['A4'] = 'Tipo de cambio (ARS por USD)'; ws['A4'].font = BOLD
ws['C4'] = TC_DEFECTO; ws['C4'].font = AZUL; ws['C4'].fill = FIN; ws['C4'].number_format = '#,##0.00'
ws['E4'] = 'Dólar oficial venta, Banco Nación, 02/09/2026. Editá esta celda y se recalcula todo el libro.'
ws['E4'].font = SUB

fila = 6
ws.cell(fila, 1, 'COSTO DEL EVENTO').font = Font(name=F, size=12, bold=True, color='1F3864')
fila += 1
lineas = [
 ('Costo total (cotizaciones reales + estimados)', f"='COSTOS UNIFICADOS'!I{fila_total}", USD0,
  'Suma de contratado, cotizado y lo que sólo tiene estimado. No incluye las alternativas descartadas.'),
 ('Lo que decía el presupuesto original', f"='COSTOS UNIFICADOS'!J{fila_total}", USD0,
  'Total de la hoja "Argentina (3 oct-4 oct)" del master: US$176.159.'),
 ('Diferencia contra el presupuesto', f"='COSTOS UNIFICADOS'!K{fila_total}", USD0,
  'Cuánto se corre el evento respecto de lo presupuestado, con los precios que hoy están sobre la mesa.'),
]
filas_kpi = {}
for etiqueta, formula, fmt, nota in lineas:
    ws.cell(fila, 1, etiqueta).font = NEGRO
    c = ws.cell(fila, 3, formula); c.font = VERDE; c.number_format = fmt; c.border = BOX
    ws.cell(fila, 5, nota).font = SUB
    filas_kpi[etiqueta] = fila
    fila += 1
f_total = filas_kpi['Costo total (cotizaciones reales + estimados)']
f_orig  = filas_kpi['Lo que decía el presupuesto original']
f_dif   = filas_kpi['Diferencia contra el presupuesto']
ws.cell(f_dif, 3).fill = FROJO

fila += 1
ws.cell(fila, 1, 'COSTO POR PERSONA').font = Font(name=F, size=12, bold=True, color='1F3864')
fila += 1
ws.cell(fila, 1, 'Base de cálculo').font = HDR; ws.cell(fila, 1).fill = FH
ws.cell(fila, 2, 'Personas').font = HDR; ws.cell(fila, 2).fill = FH
ws.cell(fila, 3, 'Costo por persona').font = HDR; ws.cell(fila, 3).fill = FH
ws.cell(fila, 5, 'Qué incluye').font = HDR; ws.cell(fila, 5).fill = FH
for j in (1, 2, 3, 5): ws.cell(fila, j).border = BOX
fila += 1
bases = [
 ('Aforo general', 5000, 'Asistentes de entrada general según la hoja del master.'),
 ('VIP', 1000, 'Asistentes VIP.'),
 ('Asistentes pagos (general + VIP)', 6000, 'La base más útil para decidir el precio de la entrada.'),
 ('Mastermind del martes', 246, 'Actividad aparte, no comparte la mayoría de los costos.'),
 ('Total de personas en el predio', 6108, 'Asistentes pagos + 100 de staff + 8 del equipo interno.'),
]
f_ini_bases = fila
for etiqueta, n, nota in bases:
    ws.cell(fila, 1, etiqueta).font = NEGRO
    c = ws.cell(fila, 2, n); c.font = AZUL; c.number_format = '#,##0'; c.fill = FIN
    c = ws.cell(fila, 3, f'=IFERROR($C${f_total}/B{fila},"")'); c.font = NEGRO; c.number_format = USD
    ws.cell(fila, 5, nota).font = SUB
    for j in (1, 2, 3): ws.cell(fila, j).border = BOX
    fila += 1
ws.cell(fila, 1, 'Las bases en amarillo son editables: cambiá el aforo y el costo por cabeza se recalcula.').font = SUB

fila += 2
ws.cell(fila, 1, 'ESTADO DE LOS RUBROS').font = Font(name=F, size=12, bold=True, color='1F3864')
fila += 1
for etiqueta, criterio, relleno, nota in [
    ('Contratado (hay contrato o anticipo)', 'Contratado', FVERD, 'Sede, merch de Colombia e intercoms.'),
    ('Cotizado (hay presupuesto formal)', 'Cotizado', None, 'Infraestructura, técnica, seguridad, médico, limpieza, residuos, seguro, WiFi, cintas, sillas.'),
    ('Sin cotizar (sólo estimado o nada)', 'Sin cotizar', FAMAR, 'Catering, vuelos, alojamiento, unifilas, DJ, escoltas, Master Mind, personal logístico.'),
]:
    ws.cell(fila, 1, etiqueta).font = NEGRO
    c = ws.cell(fila, 3, f"=SUMIF('COSTOS UNIFICADOS'!$D:$D,\"{criterio}\",'COSTOS UNIFICADOS'!$I:$I)")
    c.font = VERDE; c.number_format = USD0; c.border = BOX
    if relleno: c.fill = relleno
    ws.cell(fila, 5, nota).font = SUB
    fila += 1
ws.cell(fila, 1, 'Alternativas descartadas (no suman)').font = SUB
c = ws.cell(fila, 3, "=SUMIF('COSTOS UNIFICADOS'!$D:$D,\"Alternativa\",'COSTOS UNIFICADOS'!$I:$I)")
c.font = SUB; c.number_format = USD0

# ============================================================================
# 4. DECISIONES ABIERTAS
# ============================================================================
ws = hoja('DECISIONES', 'Decisiones abiertas que mueven el número',
          'Cada fila cambia el costo total. Ordenadas por cuánto pesan.')
COLS = [('Decisión', 34), ('Opción A', 34), ('Opción B', 34), ('Diferencia', 15), ('Qué hay que hacer', 56)]
encabezados(ws, 4, COLS)
DEC = [
 ('Sillas del público',
  'La Rural: 5.000 sillas imperio bordó por $42.500.000 (sin IVA, armado incluido)',
  'FDL Eventos: 5.500 sillas por $25.800.000 + IVA, sin armado ni facturación al exterior resuelta',
  '=(42500000-25800000*1.21)/TABLERO!$C$4',
  'Pedir a La Rural el costo del armado por separado. Si armar las de FDL cuesta menos que la diferencia, conviene FDL.'),
 ('Técnica',
  'Prina integral: $48.885.000 + IVA (sonido, luces, LED, video, estructura y staff)',
  'Armado por partes: VMG sólo LED $12.625.000 + IVA, más sonido e iluminación por separado',
  '', 'La cotización de Prina venció en junio. Pedir revalidación a Prina, Sound-Light y Dixi con el mismo pliego y comparar en una sola planilla.'),
 ('Catering',
  'AmbientHouse: viandas $28.500 + IVA por persona por día, base mínima 480',
  'Teist: propuesta del 26/06 sin cerrar. Azulado nunca envió.',
  '', 'Es el hueco más grande del presupuesto. Definir alcance (¿desayuno VIP para 1.000?) y pedir tres cotizaciones comparables esta semana.'),
 ('Vuelos y alojamiento del equipo',
  'Sin cotizar', 'Sin cotizar', '',
  'No hay ni un mail ni una línea en el sheet. Con 8 personas del equipo interno, es plata que hoy no está en ningún número.'),
 ('Facturación al exterior',
  'FDL Eventos y Vittal no confirmaron si pueden facturar a la empresa de EE.UU.',
  'Buscar proveedores que sí facturen, o resolver un circuito de pago local',
  '', 'Resolverlo antes de firmar: es el punto que puede trabar los dos contratos.'),
]
r = 5
for dec, a, b, formula, accion in DEC:
    ws.cell(r, 1, dec).font = BOLD
    ws.cell(r, 2, a).font = NEGRO
    ws.cell(r, 3, b).font = NEGRO
    c = ws.cell(r, 4, formula or None); c.font = NEGRO; c.number_format = USD
    if formula: c.fill = FAMAR
    ws.cell(r, 5, accion).font = NEGRO
    for j in range(1, 6):
        ws.cell(r, j).border = BOX
        ws.cell(r, j).alignment = Alignment(wrap_text=True, vertical='top')
    ws.row_dimensions[r].height = 56
    r += 1

del wb['Sheet']
wb.save('ARGENTINA_CMC2026_Costo_Total.xlsx')
print('OK · fila total en COSTOS UNIFICADOS:', fila_total)
