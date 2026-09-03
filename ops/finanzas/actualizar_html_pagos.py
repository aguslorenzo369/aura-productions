# -*- coding: utf-8 -*-
"""Vuelca el checklist centralizado de pagos de Argentina dentro del dashboard HTML.

Uso:  python3 actualizar_html_pagos.py <origen.html> <destino.html>

Qué hace
--------
1. Deja intactos los pagos de los otros 13 paises (su cronograma sigue valiendo).
2. Reemplaza las 7 filas de Argentina por las del checklist verificado
   (generar_checklist_pagos.py), que cierra contra el costo total del evento.
3. Mueve "Grafica URU" a Uruguay, que es de donde era.
4. Admite pagos sin fecha acordada (fecha_limite = null) en vez de inventar fechas.
5. Arregla el coloreado por urgencia y el chip de categoria, que en el HTML
   original nunca se aplicaban porque las clases del JS no existian en el CSS.
"""
import importlib.util, sys, os, re, json, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
spec = importlib.util.spec_from_file_location('chk', 'generar_checklist_pagos.py')
chk = importlib.util.module_from_spec(spec); sys.modules['chk'] = chk; spec.loader.exec_module(chk)

FILAS = chk.FILAS          # incluye el tramo 7 de conciliacion
TOTAL, PAGADO = chk.TOTAL, chk.PAGADO
FALTA = TOTAL - PAGADO

# ------------------------------------------------------------------ mapeos
CATEG = {
    'Sede':            'lugar',
    'Infraestructura': 'infraestructura',
    'Mobiliario':      'mobiliario',
    'Técnica':         'tecnica',
    'Servicios':       'servicios',
    'Merch':           'merch',
    'Catering':        'catering',
    'Producción':      'produccion',
    'Equipo':          'otro',
}

# Unicas fechas realmente acordadas. Todo lo demas va sin fecha, a proposito.
FECHAS = [
    ('cuota 1 de 2',   '2026-08-24'),
    ('factura 2601017', '2026-08-16'),
    ('factura 2601016', '2026-08-10'),
    ('Pañuelos',       '2026-09-13'),
    ('cuota 2 de 2',   '2026-09-23'),
    ('Gráfica Argentina', '2026-09-13'),
    ('Lanyards',       '2026-09-13'),
]
# Los ids de La Rural se conservan para no perder los links de factura ya cargados.
IDS_FIJOS = {'cuota 1 de 2': 36, 'cuota 2 de 2': 45}

VENCE_CORTO = {
    'urgente':           ('Urgente',           'urgente'),
    'a definir':         ('A definir',         'sinfecha'),
    'pedir':             ('Pedir presup.',     'sinfecha'),
    'antes del armado':  ('Antes del armado',  'sinfecha'),
    'antes del evento':  ('Antes del evento',  'sinfecha'),
    'contra el evento':  ('Contra el evento',  'sinfecha'),
    '—':                 ('A conciliar',       'sinfecha'),
}

def fecha_de(concepto):
    for clave, f in FECHAS:
        if clave in concepto:
            return clave, f
    return None, None

def construir_argentina():
    pagos, sig = [], 100
    for tramo, rubro, prov, conc, monto, vence, como, cont, tel, nota in FILAS:
        clave, fecha = fecha_de(conc)
        if fecha:
            venc_txt, urg = '', None          # la urgencia sale de la fecha
        else:
            venc_txt, urg = VENCE_CORTO.get(vence.lower(), (vence, 'sinfecha'))
        if clave in IDS_FIJOS:
            pid = IDS_FIJOS[clave]
        else:
            pid = sig; sig += 1
        contacto = ' · '.join(x for x in (cont, tel) if x and x != '—')
        pagos.append({
            'id': pid,
            'bloque': 2,
            'pais': 'Argentina',
            'categoria': CATEG.get(rubro, 'otro'),
            'proveedor': prov if prov != '—' else 'A definir',
            'concepto': conc,
            'monto_usd': round(monto, 2),
            'fecha_limite': fecha,
            'vence': venc_txt,
            'urgencia': urg,
            'tramo': tramo,
            'como': como if como != '—' else '',
            'contacto': contacto,
            'nota': nota,
        })
    return pagos

# ------------------------------------------------------------------ HTML
def main(origen, destino):
    html = open(origen, encoding='utf-8').read()
    m = re.search(r'(<script id="pagos-data" type="application/json">)(.*?)(</script>)', html, re.S)
    data = json.loads(m.group(2))

    resto, uru42 = [], None
    for p in data['pagos']:
        if p['pais'] != 'Argentina':
            resto.append(p)
        elif p.get('proveedor') == 'Gráfica URU':
            uru42 = dict(p, pais='Uruguay',
                         concepto='Gráfica Uruguay - saldo · Pago total (100%)')
    if uru42:
        resto.append(uru42)

    arg = construir_argentina()
    data['pagos'] = resto + arg
    data['lastSync'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    data['schemaVersion'] = 2

    nuevo = json.dumps(data, ensure_ascii=False, indent=2)
    html = html[:m.start(2)] + '\n' + nuevo + '\n' + html[m.end(2):]

    for viejo, nuevo_txt in PARCHES:
        if viejo not in html:
            raise SystemExit('NO ENCONTRADO:\n' + viejo[:160])
        html = html.replace(viejo, nuevo_txt, 1)

    open(destino, 'w', encoding='utf-8').write(html)

    tot = sum(p['monto_usd'] for p in data['pagos'])
    print('Argentina        {:>3} pagos  US$ {:>12,.2f}'.format(len(arg), sum(p['monto_usd'] for p in arg)))
    print('Falta desembolsar (checklist)  US$ {:>12,.2f}'.format(FALTA))
    print('Otros paises     {:>3} pagos  US$ {:>12,.2f}'.format(len(resto), sum(p['monto_usd'] for p in resto)))
    print('TOTAL            {:>3} pagos  US$ {:>12,.2f}'.format(len(data['pagos']), tot))
    print('->', destino)


# ------------------------------------------------------------------ parches al JS/CSS
PARCHES = [
# 1) paleta de categorias nuevas -------------------------------------------------
("""    --cat-neutral:#8e8e93;
    --cat-neutral-bg:#f2f2f4;""",
 """    --cat-infraestructura:#00857a;   /* teal — Infraestructura */
    --cat-infraestructura-bg:#dff3f1;
    --cat-mobiliario:#a2610a;        /* amber — Mobiliario */
    --cat-mobiliario-bg:#fbeeda;
    --cat-servicios:#0a84c1;         /* cyan — Servicios */
    --cat-servicios-bg:#e0f2fb;
    --cat-catering:#d6336c;          /* rose — Catering */
    --cat-catering-bg:#fce6ee;
    --cat-neutral:#8e8e93;
    --cat-neutral-bg:#f2f2f4;"""),

# 2) reglas de categoria + urgencia ----------------------------------------------
("""  .cat.tramites,.cat.trámites,.cat-tramites{background:var(--cat-tramites-bg);color:var(--cat-tramites)}""",
 """  .cat.tramites,.cat.trámites,.cat-tramites{background:var(--cat-tramites-bg);color:var(--cat-tramites)}
  .cat.infraestructura{background:var(--cat-infraestructura-bg);color:var(--cat-infraestructura)}
  .cat.mobiliario{background:var(--cat-mobiliario-bg);color:var(--cat-mobiliario)}
  .cat.servicios{background:var(--cat-servicios-bg);color:var(--cat-servicios)}
  .cat.catering{background:var(--cat-catering-bg);color:var(--cat-catering)}
  .cat.otro{background:var(--cat-neutral-bg);color:var(--cat-neutral)}"""),

# 3) semaforo real por urgencia ---------------------------------------------------
("""  .rel.ok,.pago-fecha.ok .rel{
    background:var(--ok-bg);
    color:var(--ok);
  }""",
 """  .rel.ok,.pago-fecha.ok .rel{
    background:var(--ok-bg);
    color:var(--ok);
  }
  /* Semaforo — las clases que realmente emite el JS */
  .pago-fecha.urgente .rel{background:var(--warn-bg);color:var(--warn)}
  .pago-fecha.enfecha .rel{background:var(--ok-bg);color:var(--ok)}
  .pago-fecha.sinfecha .rel{background:var(--cat-neutral-bg);color:var(--cat-neutral)}
  .pago.vencido{box-shadow:inset 3px 0 0 var(--danger)}
  .pago.urgente{box-shadow:inset 3px 0 0 var(--warn)}
  .pago.sinfecha{box-shadow:inset 3px 0 0 var(--cat-neutral)}
  .pago-desc .meta{font-size:.74rem;color:var(--txt-3);line-height:1.35}
  .pago-desc .meta b{font-weight:600;color:var(--txt-2)}"""),

# 4) filtro "sin fecha" -----------------------------------------------------------
("""    <button class="chip" data-filter="urgencia" data-val="enfecha">En fecha</button>""",
 """    <button class="chip" data-filter="urgencia" data-val="enfecha">En fecha</button>
    <button class="chip" data-filter="urgencia" data-val="sinfecha">Sin fecha acordada</button>"""),

# 5) categorias en el JS ----------------------------------------------------------
("""  produccion: { label: 'Producción', cls: 'produccion' },
  dinamica:   { label: 'Dinámica',   cls: 'dinamica' },
  tramites:   { label: 'Trámites',   cls: 'tramites' },
  otro:       { label: 'Otro',       cls: 'otro' }""",
 """  produccion: { label: 'Producción', cls: 'produccion' },
  dinamica:   { label: 'Dinámica',   cls: 'dinamica' },
  tramites:   { label: 'Trámites',   cls: 'tramites' },
  infraestructura: { label: 'Infraestructura', cls: 'infraestructura' },
  mobiliario: { label: 'Mobiliario', cls: 'mobiliario' },
  servicios:  { label: 'Servicios',  cls: 'servicios' },
  catering:   { label: 'Catering',   cls: 'catering' },
  otro:       { label: 'Otro',       cls: 'otro' }"""),

# 6) fuente de los datos ----------------------------------------------------------
("""// Data cargada desde Cronograma_Pagos_Cumbre.xlsx (Aleja) — 54 pagos · USD 417.765,32""",
 """// Argentina: CHECKLIST DE PAGOS · Argentina CMC 2026 (checklist centralizado, dólar $1.510).
// Resto de los países: Cronograma_Pagos_Cumbre.xlsx (Aleja).
// Los pagos sin fecha acordada van con fecha_limite = null: no se inventan fechas."""),

# 7) util null-safe ---------------------------------------------------------------
("""const daysDiff = (s) => Math.round((new Date(s + 'T00:00:00') - HOY) / 86400000);
const getUrgencia = (s) => {
  const d = daysDiff(s);
  if (d < 0) return 'vencido';
  if (d < 7) return 'urgente';
  return 'enfecha';
};""",
 """const daysDiff = (s) => s ? Math.round((new Date(s + 'T00:00:00') - HOY) / 86400000) : Infinity;
// Recibe el pago entero: hay pagos sin fecha acordada, y algunos traen la urgencia fijada a mano.
const getUrgencia = (p) => {
  if (p.urgencia) return p.urgencia;
  if (!p.fecha_limite) return 'sinfecha';
  const d = daysDiff(p.fecha_limite);
  if (d < 0) return 'vencido';
  if (d < 7) return 'urgente';
  return 'enfecha';
};
const RANGO_URG = { vencido:0, urgente:1, enfecha:2, sinfecha:3 };
const ordenPago = (a,b) =>
  (RANGO_URG[getUrgencia(a)] - RANGO_URG[getUrgencia(b)]) ||
  (daysDiff(a.fecha_limite) - daysDiff(b.fecha_limite)) ||
  (a.id - b.id);"""),

# 8) formateadores ----------------------------------------------------------------
("""const fmtRel = (s) => {
  const d = daysDiff(s);
  if (d < 0) return `hace ${Math.abs(d)}d`;
  if (d === 0) return 'HOY';
  if (d === 1) return 'mañana';
  return `en ${d}d`;
};""",
 """const fmtRel = (p) => {
  if (!p.fecha_limite) return getUrgencia(p) === 'urgente' ? 'ya' : 'sin fecha';
  const d = daysDiff(p.fecha_limite);
  if (d < 0) return `hace ${Math.abs(d)}d`;
  if (d === 0) return 'HOY';
  if (d === 1) return 'mañana';
  return `en ${d}d`;
};"""),

# 9) filtro ------------------------------------------------------------------------
("""    if (state.urgencia !== 'all' && getUrgencia(p.fecha_limite) !== state.urgencia) return false;""",
 """    if (state.urgencia !== 'all' && getUrgencia(p) !== state.urgencia) return false;"""),

# 10) cabecera ---------------------------------------------------------------------
("""  const urgentCount = list.filter(p => ['vencido','urgente'].includes(getUrgencia(p.fecha_limite))).length;
  const countries = new Set(list.map(p => p.pais)).size;
  const next = list.filter(p => daysDiff(p.fecha_limite) >= 0)
                   .sort((a,b) => daysDiff(a.fecha_limite) - daysDiff(b.fecha_limite))[0];""",
 """  const urgentCount = list.filter(p => ['vencido','urgente'].includes(getUrgencia(p))).length;
  const countries = new Set(list.map(p => p.pais)).size;
  const next = list.filter(p => p.fecha_limite && daysDiff(p.fecha_limite) >= 0)
                   .sort((a,b) => daysDiff(a.fecha_limite) - daysDiff(b.fecha_limite))[0];
  const sinFecha = list.filter(p => getUrgencia(p) === 'sinfecha').length;"""),

("""  if (next) partes.push(`próximo vencimiento: <b>${fmtDate(next.fecha_limite)}</b>`);""",
 """  if (next) partes.push(`próximo vencimiento: <b>${fmtDate(next.fecha_limite)}</b>`);
  if (sinFecha) partes.push(`<b>${sinFecha}</b> sin fecha acordada`);"""),

# 11) orden y conteo por pais --------------------------------------------------------
("""    const pagos = byPais[paisName].slice().sort((a,b) =>
      daysDiff(a.fecha_limite) - daysDiff(b.fecha_limite)
    );""",
 """    const pagos = byPais[paisName].slice().sort(ordenPago);"""),

("""    const urgentCount = pagos.filter(p => ['vencido','urgente'].includes(getUrgencia(p.fecha_limite))).length;""",
 """    const urgentCount = pagos.filter(p => ['vencido','urgente'].includes(getUrgencia(p))).length;"""),

# 11b) que el tablero no dependa de Firebase -------------------------------------
# Si el CDN de Firebase no carga, el `firebase.initializeApp` de arriba tiraba y
# se llevaba puesto al render(): la pagina quedaba en blanco. Ahora degrada.
("""firebase.initializeApp(firebaseConfig);
const fbDb = firebase.database();
const fbAuth = firebase.auth();""",
 """let fbDb = null, fbAuth = null;
try {
  firebase.initializeApp(firebaseConfig);
  fbDb = firebase.database();
  fbAuth = firebase.auth();
} catch (e) {
  console.warn('[pagos] Firebase no disponible, sigo sin sincronizar links:', e);
}"""),

("""function initFirebase() {
  setSyncStatus(null, 'Conectando...');""",
 """function initFirebase() {
  if (!fbAuth) { setSyncStatus('error', 'Sin sincronización'); return; }
  setSyncStatus(null, 'Conectando...');"""),

# 11c) bajada del banner, que describia solo la proyeccion de Aleja ---------------
("""    <div class="banner-sub">Cronograma proyectado desde 9-jul-2026 · Lugar: pago 10 días antes · Merch: pago 20 días antes · Ecuador: pago único</div>""",
 """    <div class="banner-sub">Argentina: checklist verificado contra contratos y facturas · dólar $1.510 · los pagos sin fecha acordada figuran como &laquo;sin fecha&raquo;<br>Resto de los países: cronograma proyectado (lugar 10 días antes · merch 20 días antes · Ecuador pago único)</div>"""),

# 12) fila del pago -------------------------------------------------------------------
("""      const urg = getUrgencia(p.fecha_limite);""",
 """      const urg = getUrgencia(p);"""),

("""        <div class="pago-fecha">
          <span class="sem ${urg}"></span>
          <span>${fmtDate(p.fecha_limite)}</span>
          <span class="rel">${fmtRel(p.fecha_limite)}</span>
        </div>
        <div class="pago-desc">
          <div class="prov">${p.proveedor}</div>
          <div class="concepto">${p.concepto}</div>
        </div>
        <div><span class="pago-cat ${cat.cls}">${cat.label}</span></div>""",
 """        <div class="pago-fecha ${urg}">
          <span>${p.fecha_limite ? fmtDate(p.fecha_limite) : (p.vence || 'A definir')}</span>
          <span class="rel">${fmtRel(p)}</span>
        </div>
        <div class="pago-desc">
          <div class="prov">${p.proveedor}</div>
          <div class="concepto">${p.concepto}</div>
          ${p.contacto ? `<div class="meta">${p.contacto}${p.como ? ' · <b>' + p.como + '</b>' : ''}</div>` : ''}
          ${p.nota ? `<div class="meta">${p.nota}</div>` : ''}
        </div>
        <div class="pago-cat"><span class="cat ${cat.cls}">${cat.label}</span></div>"""),
]

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
