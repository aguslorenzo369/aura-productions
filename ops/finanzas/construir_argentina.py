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
from openpyxl.worksheet.datavalidation import DataValidation

HOY = datetime.date(2026, 9, 2)
TC_DEFECTO = 1530.0   # dolar operativo acordado con Agustina, 02/09/2026

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

def banda_bloque(ws, fila, texto, ncols):
    ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=ncols)
    c = ws.cell(fila, 1, f'  {texto}')
    c.font = Font(name=F, size=9, bold=True, color='1F3864'); c.fill = FBLOQ
    for j in range(1, ncols + 1): ws.cell(fila, j).fill = FBLOQ
    return fila + 1

# ============================================================================
# DATOS
# ============================================================================
# (bloque, rubro, proveedor, detalle, moneda, monto_sin_iva, iva, estado,
#  estimado_usd_sheet, fuente)
# estado: Contratado / Cotizado / Alternativa / Sin cotizar
ARS_, USD_ = 'ARS', 'USD'
# estado: Cerrado / Contratado / Cotizado / En revisión / En negociación / Bonificado / Alternativa / Sin cotizar
ITEMS = [
 # ---------------- SEDE ----------------
 ('Sede', 'Alquiler Pabellón Azul', 'La Rural (contrato CC-00957)',
  'Locación 2 días de evento + 1 día de montaje', USD_, 75000.0, 0.0, 'Contratado',
  70000.0, 'Contrato CC-00957 · hoja PAGOS del master (US$43.446 abonados el 27/04)'),
 ('Sede', 'Infraestructura y mobiliario de stands', 'La Rural — Jefatura de Infraestructura',
  'Definido: armado de los stands y su mobiliario. Stand de staff 100 m², stand de producción menos de 50 m², y el mobiliario del camarín de speakers. Falta pedirles los espejos.',
  USD_, 9270.0, 0.0, 'Cerrado', 0.0,
  'Definición de Agustina sobre el presupuesto de $66.494.708 del 17/08 · ver hoja AHORROS'),
 ('Sede', 'Sillas del público (5.500)', 'FDL Eventos',
  '4.500 sillas plásticas Munro reforzadas + 1.000 sillas hotel negro + flete. NO incluye armado.',
  ARS_, 25800000.0, 0.21, 'Cotizado', 16500.0,
  'Mail fdleventos@gmail.com 07/08/2026 · pendiente de resolver facturación al exterior'),
 ('Sede', 'Montaje, acomodación y desmontaje de sillas', 'En negociación',
  'Montaje previo, acomodación el sábado a la noche después de la dinámica y desmontaje el domingo.',
  ARS_, 900000.0, 0.0, 'En negociación', 0.0,
  'Negociación de Agustina · cerrar el número antes de firmar las sillas'),
 ('Sede', 'Replanteo de sillas (ingeniero)', 'Sin cotizar',
  'Replanteo del layout de sillas del pabellón. Confirmado que va aparte de la dirección técnica de La Rural.',
  USD_, 0.0, 0.0, 'Sin cotizar', 0.0, 'Pendiente de pedir presupuesto'),
 ('Sede', 'Conectividad WiFi', 'La Rural — Servicios de Conectividad',
  '2 redes privadas de 30 Mbps (técnica + staff/acreditación), del 2 al 4 de octubre',
  ARS_, 1466063.84, 0.21, 'Cotizado', 800.0,
  'Mail conectividad@larural.com.ar 05/08/2026 · presupuesto N.º 2, base IPC junio (el del 16/06 era $1.438.728)'),
 # ---------------- TÉCNICA ----------------
 ('Técnica', 'Producción técnica', 'Cerrado por Agustina',
  'Sonido, iluminación, video y LED. Cerrado en dólares.',
  USD_, 60000.0, 0.0, 'Cerrado', 34000.0,
  'Negociación de Agustina · reemplaza la cotización vencida de Prina'),
 ('Técnica', 'Entelado', 'Cerrado por Agustina',
  'Entelado del pabellón. Negociado a la mitad de lo que estaba cotizado.',
  ARS_, 24500000.0, 0.0, 'Cerrado', 0.0,
  'Negociación de Agustina · US$16.000 aprox. al dólar de referencia'),
 ('Técnica', 'Circuito cerrado (CCTV)', 'Cerrado por Agustina',
  'Circuito cerrado de cámaras para el pabellón.',
  USD_, 6209.0, 0.0, 'Cerrado', 0.0, 'Negociación de Agustina'),
 ('Técnica', 'Bonificado por el proveedor de técnica', 'Sin costo',
  '500 vallas y efectos especiales, sin cargo. Es lo que evita el gasto de vallado que estaba presupuestado.',
  USD_, 0.0, 0.0, 'Bonificado', 0.0, 'Negociación de Agustina'),
 # ---------------- SERVICIOS ----------------
 ('Servicios', 'Seguridad y vigilancia', 'Road Seguridad S.A.',
  '263 horas de vigilancia (armado, evento y desarme) + planos de evacuación $715.000 + supervisión general $795.000',
  ARS_, 7218928.96, 0.21, 'Cotizado', 0.0,
  'Mail presupuestos@roadseguridad.com.ar 12/08/2026 (versión V3, lista para firmar)'),
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
 ('Servicios', 'Baños químicos — ecobaños', 'Sin cotizar',
  'Decidido: ecobaños, no los químicos tradicionales. Más limpios, mejor a la vista y ecofriendly. Falta pedir presupuesto.',
  USD_, 0.0, 0.0, 'Sin cotizar', 0.0, 'Decisión de Agustina · pendiente de cotizar'),
 ('Servicios', 'Seguro de accidentes personales', 'Chanes Seguros',
  'Cobertura MIA (muerte, invalidez y asistencia médica) para 150 personas, exigida por La Rural',
  ARS_, 953151.93, 0.0, 'Cotizado', 400.0,
  'Mail nestor@chanesseguros.com.ar 13/07/2026 · premio único, cotizado para 15-19/07'),
 # ---------------- CATERING ----------------
 ('Catering', 'Catering VIP, staff y equipo', 'Grupo Ambient',
  'Número final por las dos propuestas juntas: 600 lunchbox para los VIP + desayuno, almuerzo y cena para 150 personas.',
  USD_, 13582.0, 0.0, 'Cerrado', 33820.0,
  'Cierre de Agustina con Grupo Ambient · reemplaza la estimación de $25.000.000'),
 ('Catering', 'Food trucks', 'Sin costo',
  'No los paga la producción.',
  USD_, 0.0, 0.0, 'Bonificado', 0.0, 'Confirmado por Agustina'),
 # ---------------- MERCH ----------------
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
 ('Merch', 'Gorras', 'Proveedor Colombia', 'Pagado 100% el 25/06',
  USD_, 1825.0, 0.0, 'Contratado', 5000.0, 'Hoja PAGOS del master'),
 ('Merch', 'Gráfica Argentina', 'Proveedor Colombia',
  'Contrato cerrado, saldo US$1.839 al 13/09',
  USD_, 2481.0, 0.0, 'Contratado', 0.0, 'Hoja PAGOS del master'),
 ('Merch', 'Marquetería y enmarcado', 'Sin cotizar',
  'Enmarcado de las certificaciones y los premios. Rubro nuevo, no estaba en ninguna planilla.',
  USD_, 0.0, 0.0, 'Sin cotizar', 0.0, 'Agregado por Agustina · pendiente de cotizar'),
 ('Merch', 'Resto de merch e impresos', 'Varios (merch desde Colombia)',
  'Contratos, cheques, escarapelas, bolsas, camisetas, mapas, diplomas, placas y manillas',
  USD_, 0.0, 0.0, 'Sin cotizar', 8689.0,
  'Estimado de la hoja Argentina del master; sin cotización argentina'),
 # ---------------- PRODUCCIÓN ----------------
 ('Producción', 'Unifilas', 'A definir', 'Estimado del sheet, sin cotización',
  USD_, 0.0, 0.0, 'Sin cotizar', 1200.0, 'Hoja Argentina del master'),
 ('Producción', 'Vallado (500 vallas)', 'Bonificado por técnica',
  'Las 500 vallas las regala el proveedor de técnica. Estaban presupuestadas en US$1.250.',
  USD_, 0.0, 0.0, 'Bonificado', 1250.0, 'Negociación de Agustina'),
 ('Producción', 'DJ', 'A definir', 'Estimado del sheet',
  USD_, 0.0, 0.0, 'Sin cotizar', 500.0, 'Hoja Argentina del master'),
 ('Producción', 'Escoltas (2)', 'A definir', 'Estimado del sheet',
  USD_, 0.0, 0.0, 'Sin cotizar', 1000.0, 'Hoja Argentina del master'),
 ('Producción', 'Master Mind Hit', 'A definir', 'Sala adicional',
  USD_, 0.0, 0.0, 'Sin cotizar', 3000.0, 'Hoja Argentina del master'),
 ('Producción', 'Personal logístico', 'A definir', 'La hoja del master lo tiene en US$0',
  USD_, 0.0, 0.0, 'Sin cotizar', 0.0, 'Hoja Argentina del master · valor en cero'),
 ('Producción', 'Intercoms', 'Proveedor Colombia',
  'Contrato US$560, sin abonar, 2 cuotas al 24/08 y 23/09',
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
        c = ws.cell(r, 9, f'=IF(D{r}="Bonificado",0,IF(H{r}="",N(J{r}),IF(E{r}="USD",H{r},H{r}/TABLERO!$C$4)))')
        c.font = NEGRO; c.number_format = USD
        c = ws.cell(r, 10, est or None); c.font = AZUL; c.number_format = USD
        c = ws.cell(r, 11, f'=IF(D{r}="Alternativa","",I{r}-N(J{r}))'); c.font = NEGRO; c.number_format = USD
        ws.cell(r, 12, fuente).font = SUB
        relleno = {'Cerrado': FVERD, 'Contratado': FVERD, 'Cotizado': None, 'En revisión': FAMAR,
                   'En negociación': FAMAR, 'Bonificado': FGRIS, 'Alternativa': FGRIS,
                   'Sin cotizar': FAMAR}[estado]
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
 ('Infraestructura de La Rural',
  'Presupuesto completo: $66.494.708 (US$43.461), con las 5.000 sillas y todo el mobiliario',
  'Sólo panelería + dirección técnica + guardias: $16.858.366 (US$11.019). El mobiliario se compra aparte.',
  '=(66494708.2-16858366.2)/TABLERO!$C$4',
  'Agustina marca ítem por ítem qué se queda. La hoja INFRAESTRUCTURA tiene las 28 líneas del presupuesto para filtrar.'),
 ('Montaje de las sillas',
  'La Rural con las sillas incluidas y armadas',
  'FDL Eventos + montaje/acomodación/desmontaje negociado en $900.000',
  '', 'Con FDL a $31.218.000 más $900.000 de montaje son US$20.992 contra US$27.778 de La Rural. Cerrar el número del montaje y firmar.'),
 ('Catering — cerrado', 'Grupo Ambient: US$13.582 por las dos propuestas',
  'La planilla tenía US$33.820 estimados',
  '=13582-33820', 'Cerrado. Es la mejor negociación del evento: US$20.238 por debajo de lo presupuestado.'),
 ('Rubros nuevos sin cotizar',
  'Ecobaños, marquetería de certificaciones y premios, replanteo de sillas con ingeniero',
  'Hoy entran en US$0',
  '', 'Pedir las tres cotizaciones esta semana. Son los últimos huecos que quedan además de vuelos y alojamiento.'),
 ('Vuelos y alojamiento del equipo',
  'Sin cotizar', 'Sin cotizar', '',
  'No hay ni un mail ni una línea en el sheet. Con 8 personas de equipo interno, es el hueco más grande que queda.'),
 ('Facturación al exterior',
  'FDL Eventos y Vittal no confirmaron si pueden facturar a la empresa de EE.UU.',
  'Buscar proveedores que sí facturen, o resolver un circuito de pago local',
  '', 'Resolverlo antes de firmar: puede trabar los dos contratos.'),
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

# ============================================================================
# 6. AHORROS — comparativa entre lo cotizado y lo que se cerró
# ============================================================================
# (rubro, referencia, ref_ars, ref_usd, cerrado, cer_ars, cer_usd, respaldo)
# ref_ars/cer_ars en None cuando el número está directamente en dólares.
AHORROS = [
 ('Infraestructura y mobiliario',
  'Grupo MET, cotización de mobiliario', 40000000.0, None,
  'Armado de stands + mobiliario, definido por Agustina', 14183100.0, 9270.0,
  'La cotización de Grupo MET no está en el correo: dato aportado por Agustina. En el correo sí está el presupuesto de La Rural del 17/08 por $66.494.708 (con las 5.000 sillas adentro).'),
 ('Sillas del público',
  'La Rural: 5.000 sillas imperio bordó, armado incluido', 42500000.0, None,
  'FDL Eventos 5.500 sillas + montaje, acomodación y desmontaje', 32118000.0, None,
  'Mail criccio@larural.com.ar 17/08 y mail fdleventos@gmail.com 07/08. El montaje ($900.000) está en negociación.'),
 ('Entelado',
  'Primera cotización recibida', 39000000.0, None,
  'Negociado a la mitad', 24500000.0, None,
  'Dato aportado por Agustina; la cotización inicial no está en el correo.'),
 ('Catering',
  'Primera propuesta de Grupo Ambient', 30000000.0, None,
  '600 lunchbox VIP + desayuno, almuerzo y cena para 150 personas', None, 13582.0,
  'Cierre informado por Agustina. En el correo está la propuesta de AmbientHouse del 16/06 a $28.500 + IVA por persona por día con base mínima de 480.'),
 ('Vallado del público',
  'Presupuestado en la hoja de Argentina', None, 1250.0,
  '500 vallas bonificadas por el proveedor de técnica', None, 0.0,
  'Negociación de Agustina. Además bonifican los efectos especiales, que no estaban valorizados.'),
]

ws = hoja('AHORROS', 'Lo cotizado contra lo que se cerró',
          'Cuánto se bajó rubro por rubro. La columna "Respaldo" dice si la referencia está documentada en el correo o si es un dato aportado.')
COLS = [('Rubro', 26), ('Referencia cotizada', 40), ('Ref. en pesos', 15), ('Ref. USD', 12),
        ('Lo que se cerró', 44), ('Cerrado en pesos', 15), ('Cerrado USD', 12),
        ('Ahorro USD', 13), ('Ahorro %', 10), ('Respaldo', 60)]
NC = len(COLS)
encabezados(ws, 4, COLS)
r = 5
filas_ah = []
for rubro, ref, ref_ars, ref_usd, cer, cer_ars, cer_usd, respaldo in AHORROS:
    ws.cell(r, 1, rubro).font = BOLD
    ws.cell(r, 2, ref).font = NEGRO
    c = ws.cell(r, 3, ref_ars); c.font = AZUL; c.number_format = ARS
    c = ws.cell(r, 4, ref_usd if ref_usd is not None else f'=C{r}/TABLERO!$C$4')
    c.font = AZUL if ref_usd is not None else NEGRO; c.number_format = USD
    ws.cell(r, 5, cer).font = NEGRO
    c = ws.cell(r, 6, cer_ars); c.font = AZUL; c.number_format = ARS
    c = ws.cell(r, 7, cer_usd if cer_usd is not None else f'=F{r}/TABLERO!$C$4')
    c.font = AZUL if cer_usd is not None else NEGRO; c.number_format = USD
    c = ws.cell(r, 8, f'=D{r}-G{r}'); c.font = BOLD; c.number_format = USD; c.fill = FVERD
    c = ws.cell(r, 9, f'=IFERROR(H{r}/D{r},"")'); c.font = NEGRO; c.number_format = PCT
    ws.cell(r, 10, respaldo).font = SUB
    for j in range(1, NC + 1):
        ws.cell(r, j).border = BOX
        ws.cell(r, j).alignment = Alignment(wrap_text=True, vertical='top')
    ws.row_dimensions[r].height = 46
    filas_ah.append(r)
    r += 1
ws.cell(r, 1, 'AHORRO TOTAL').font = Font(name=F, size=12, bold=True)
for col in (4, 7, 8):
    c = ws.cell(r, col, f'=SUM({L(col)}{filas_ah[0]}:{L(col)}{filas_ah[-1]})')
    c.font = Font(name=F, size=12, bold=True); c.number_format = USD; c.fill = FVERD; c.border = BOX
fila_ah_total = r

r += 2
ws.cell(r, 1, 'TÉCNICA — la comparación no es directa').font = Font(name=F, size=11, bold=True, color='C00000')
r += 1
for t in [
 'Se cerró con Grupo MET en US$60.000 (unos $91.800.000 al dólar de referencia), con todos los agregados que se fueron sumando después de la visita al predio.',
 'Las otras cotizaciones fueron sobre el pliego base, que según Agustina no cubría lo que necesita el pabellón. Por eso no se pueden restar sin más:',
 '   · Sound-Light (16/06): no se pudo abrir el PDF, el mail pesa 33 MB. En el mail del 19/06 se les dice que las otras cotizaciones son "prácticamente la mitad", así que estaba cerca de los $100.000.000.',
 '   · 2MG (24/06): $53.655.470, con descuento especial $45.000.000 + IVA. Con los adicionales de iluminación y estructura llega a unos $78.000.000.',
 '   · Prina (18/06): $48.885.000 + IVA = $59.150.850. Validez de 10 días, vencida.',
 '   · VMG (29/06): $12.625.000 + IVA, sólo las pantallas LED de 65 m².',
 'Para poder mostrar un ahorro defendible en técnica hace falta el PDF de Grupo MET y el alcance final, para compararlo contra el mismo alcance de los otros tres.',
]:
    ws.cell(r, 1, t).font = SUB
    r += 1

# ============================================================================
# 5. INFRAESTRUCTURA — las 28 líneas de La Rural, para marcar cuáles se quedan
# ============================================================================
INFRA = [
 ('PANELERÍA (montaje de estructuras)', [
   ('Oficina de producción — 25 m² (panelería + puerta + iluminación)', 1314575.00),
   ('Sala de staff — 100 m² (panelería + puerta + iluminación)',        5258300.00),
   ('Depósito 8×8 para las 2.500 barras — 64 m²',                       3365312.00)]),
 ('MOBILIARIO · oficina de producción', [
   ('Mesa redonda 1,60 ×2', 236000.0), ('Silla imperio bordó ×10', 85000.0),
   ('Sillón Valencia 2C ×2', 254000.0), ('Sillón BRNO ×2', 160000.0),
   ('Mesa ratona ×1', 118000.0), ('Perchero de pie ×1', 40000.0),
   ('Tacho de basura grande ×1', 56300.0)]),
 ('MOBILIARIO · sala de staff', [
   ('Mesa redonda 1,60 ×5', 590000.0), ('Silla imperio bordó ×40', 340000.0),
   ('Perchero de pie ×1', 40000.0), ('Tacho de basura grande ×1', 56300.0)]),
 ('MOBILIARIO · sala principal', [
   ('Silla imperio bordó ×5.000', 42500000.0), ('Mesa 1,80 × 0,90 ×40', 2500000.0),
   ('Mantel ×40', 900000.0), ('Mantel redondo ×8', 256000.0)]),
 ('MOBILIARIO · camarín de speakers', [
   ('Mesa redonda 1,60 ×1', 118000.0), ('Espejo ×1', 79500.0),
   ('Juego de living (sillones + mesa ratona)', 1103642.0),
   ('Perchero de pie ×1', 40000.0), ('Tacho de basura grande ×1', 56300.0)]),
 ('MOBILIARIO · escenario y técnica', [
   ('Mesa cocktail alta (escenario) ×1', 45000.0), ('Mesa alta para DJ ×1', 62300.0)]),
 ('GENERALES', [
   ('Dirección técnica de todo el evento + replanteo', 5149179.20),
   ('Guardia eléctrica × 2 días', 865800.0), ('Guardia técnica × 2 días', 905200.0)]),
]
PROVISIONAL = {1, 2, 3, 26, 27, 28}   # panelería + generales: el escenario que está cargado hoy

ws = hoja('INFRAESTRUCTURA', 'Presupuesto de infraestructura de La Rural, línea por línea',
          'Las 28 líneas del PDF del 17/08. Marcá SÍ o NO en la columna "¿Se queda?" y el subtotal se recalcula.')
COLS = [('#', 5), ('Bloque', 30), ('Ítem', 48), ('Precio (ARS)', 15), ('USD', 12),
        ('¿Se queda?', 12), ('Si se queda (ARS)', 17), ('Nota', 44)]
NC = len(COLS)
encabezados(ws, 4, COLS)
dv = DataValidation(type='list', formula1='"SÍ,NO"', allow_blank=True)
ws.add_data_validation(dv)
NOTAS = {
 3: 'Depósito para las 2.500 barras de la dinámica.',
 15: 'Reemplazadas por las 5.500 sillas de FDL Eventos.',
 21: 'El mobiliario "más fino" del camarín: candidato a contratárselo a La Rural.',
 26: 'Ojo: el replanteo de sillas va aparte, con ingeniero propio.',
}
r, n, filas_infra = 5, 0, []
for bloque, items in INFRA:
    r = banda_bloque(ws, r, bloque, NC)
    for desc, precio in items:
        n += 1
        ws.cell(r, 1, n).font = SUB
        ws.cell(r, 2, bloque.split('·')[-1].strip()).font = SUB
        ws.cell(r, 3, desc).font = AZUL
        c = ws.cell(r, 4, precio); c.font = AZUL; c.number_format = ARS
        c = ws.cell(r, 5, f'=D{r}/TABLERO!$C$4'); c.font = NEGRO; c.number_format = USD
        c = ws.cell(r, 6, 'SÍ' if n in PROVISIONAL else 'NO'); c.font = AZUL; c.fill = FIN
        dv.add(c)
        c = ws.cell(r, 7, f'=IF(F{r}="SÍ",D{r},0)'); c.font = NEGRO; c.number_format = ARS
        ws.cell(r, 8, NOTAS.get(n, '')).font = SUB
        for j in range(1, NC + 1): ws.cell(r, j).border = BOX
        filas_infra.append(r)
        r += 1
ini_i, fin_i = filas_infra[0], filas_infra[-1]
r += 1
for etiqueta, formula, relleno in [
    ('TOTAL del presupuesto de La Rural', f'=SUM(D{ini_i}:D{fin_i})', FGRIS),
    ('Lo que se queda (marcado SÍ)',      f'=SUM(G{ini_i}:G{fin_i})', FVERD),
    ('Lo que se saca (marcado NO)',       f'=D{r}-D{r+1}',            FAMAR)]:
    ws.cell(r, 3, etiqueta).font = BOLD
    c = ws.cell(r, 4, formula); c.font = BOLD; c.number_format = ARS; c.fill = relleno; c.border = BOX
    c = ws.cell(r, 5, f'=D{r}/TABLERO!$C$4'); c.font = BOLD; c.number_format = USD; c.fill = relleno; c.border = BOX
    r += 1
ws.cell(r + 1, 3, 'Lo marcado hoy es el escenario provisional cargado en COSTOS UNIFICADOS: panelería + dirección técnica + guardias. Cambiá los SÍ/NO y llevá el nuevo total a esa hoja.').font = SUB

del wb['Sheet']
wb.save('ARGENTINA_CMC2026_Costo_Total.xlsx')
print('OK · fila total en COSTOS UNIFICADOS:', fila_total)
