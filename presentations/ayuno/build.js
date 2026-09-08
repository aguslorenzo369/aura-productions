const pptxgen = require('pptxgenjs')
const pres = new pptxgen()
pres.layout = 'LAYOUT_WIDE'            // 13.333 x 7.5
pres.title = 'Ayuno — Vaciar el cuerpo, expandir la conciencia'

const W = 13.333, M = 1.1, CW = W - M * 2

// Paleta: negro cálido + hueso + ámbar (luz de vela). Sin púrpura, sin saturación.
const INK    = '0B0A09'
const PANEL  = '13110F'
const BONE   = 'EDE6DA'
const BODY   = '9E958A'
const LABEL  = '8A8175'
const AMBER  = 'C8A45D'
const AMBERD = '7A6435'
const RING   = '2C261C'
const RINGF  = '1A1712'
const HAIR   = '242019'

const SERIF = 'Cambria'
const SANS  = 'Calibri'

const slideBase = () => { const s = pres.addSlide(); s.background = { color: INK }; return s }

// Motivo único del deck: el círculo — lo lleno que se vacía.
function ring (s, cx, cy, r, color, wgt) {
  s.addShape(pres.ShapeType.ellipse, {
    x: cx - r, y: cy - r, w: r * 2, h: r * 2,
    fill: { color: INK, transparency: 100 },
    line: { color, width: wgt || 0.75 },
  })
}
function disc (s, cx, cy, r, color) {
  s.addShape(pres.ShapeType.ellipse, { x: cx - r, y: cy - r, w: r * 2, h: r * 2, fill: { color }, line: { color, width: 0 } })
}

function eyebrow (s, text, y) {
  s.addText(text, { x: M, y: y || 0.86, w: 7, h: 0.24, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 9.5, bold: true, color: AMBER, charSpacing: 3.4, valign: 'middle' })
}
function title (s, text, opts) {
  s.addText(text, Object.assign({ x: M, y: 1.28, w: 10.4, h: 0.9, isTextBox: true, margin: 0, fontFace: SERIF, fontSize: 34, color: BONE, valign: 'top' }, opts))
}
function footer (s, n) {
  s.addText('AYUNO · VACIAR EL CUERPO, EXPANDIR LA CONCIENCIA', { x: M, y: 6.82, w: 8, h: 0.24, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 7.5, color: '55504A', charSpacing: 1.8, valign: 'middle' })
  s.addText(String(n).padStart(2, '0'), { x: W - M - 1, y: 6.82, w: 1, h: 0.24, isTextBox: true, margin: 0, align: 'right', fontFace: SANS, fontSize: 7.5, color: '55504A', charSpacing: 1.6, valign: 'middle' })
}

/* ===================== 01 · PORTADA ===================== */
{
  const s = slideBase()
  ring(s, 9.9, 3.75, 2.05, RING)
  ring(s, 9.9, 3.75, 2.6, RINGF, 0.5)
  disc(s, 9.9, 3.75, 1.35, '15120D')
  ring(s, 9.9, 3.75, 1.35, AMBERD, 0.75)

  s.addText('UNA PRÁCTICA DE VACÍO', { x: M, y: 2.62, w: 6, h: 0.26, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 9.5, bold: true, color: AMBER, charSpacing: 3.6, valign: 'middle' })
  s.addText('Ayuno', { x: M - 0.05, y: 3.0, w: 6, h: 1.15, isTextBox: true, margin: 0, fontFace: SERIF, fontSize: 68, color: BONE, valign: 'middle' })
  s.addText('Vaciar el cuerpo, expandir la conciencia', { x: M, y: 4.25, w: 6.4, h: 0.5, isTextBox: true, margin: 0, fontFace: SERIF, fontSize: 21, italic: true, color: AMBER, valign: 'middle' })
  s.addNotes('Portada. Abrir en silencio unos segundos antes de hablar: la lámina ya dice el tono.')
}

/* ===================== 02 · INTRODUCCIÓN ===================== */
{
  const s = slideBase()
  ring(s, 6.67, 3.5, 2.45, RINGF, 0.75)
  eyebrow(s, 'INTRODUCCIÓN')
  s.addText([
    { text: 'El ayuno no es ausencia, ', options: { italic: true } },
    { text: 'es pausa', options: { italic: true, color: AMBER } },
    { text: '.', options: { italic: true, breakLine: true } },
    { text: 'En el silencio del cuerpo, la energía se reorganiza', options: { italic: true, breakLine: true } },
    { text: 'y la conciencia se expande.', options: { italic: true } },
  ], {
    x: 1.6, y: 2.75, w: 10.13, h: 2.2, isTextBox: true, margin: 0, align: 'center',
    fontFace: SERIF, fontSize: 27, color: BONE, lineSpacingMultiple: 1.52, valign: 'top',
  })
  footer(s, 2)
  s.addNotes('Dejar respirar la frase. No agregar nada: es la tesis de toda la charla.')
}

/* ===================== 03 · QUÉ ES ===================== */
{
  const s = slideBase()
  ring(s, 11.9, 5.9, 2.3, RINGF, 0.75)
  eyebrow(s, 'DEFINICIÓN')
  title(s, '¿Qué es un ayuno prolongado?', { w: 9 })

  s.addText([
    { text: 'Dejar de comer durante más de 24 horas, el punto en el que el cuerpo ' },
    { text: 'cambia de fuente energética', options: { color: BONE, bold: true } },
    { text: ': de la glucosa a las grasas y las cetonas.' },
  ], { x: M, y: 2.66, w: 7.2, h: 1.1, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 14, color: BODY, lineSpacingMultiple: 1.55, valign: 'top' })

  s.addText([
    { text: 'El propósito: ' },
    { text: 'regeneración y claridad', options: { color: AMBER, italic: true } },
    { text: '.' },
  ], { x: M, y: 4.6, w: 7.2, h: 0.55, isTextBox: true, margin: 0, fontFace: SERIF, fontSize: 23, color: BONE, valign: 'top' })
  footer(s, 3)
  s.addNotes('Definición corta. El dato clave es el cambio de combustible, no las horas.')
}

/* ===================== 04 · ETAPAS FISIOLÓGICAS ===================== */
{
  const s = slideBase()
  eyebrow(s, 'ETAPAS FISIOLÓGICAS')
  title(s, 'El cuerpo se vacía por tramos.', { w: 9 })

  const stages = [
    ['12 – 24 h', 'Agota el glucógeno y entra en cetosis.', 0.60],
    ['24 – 48 h', 'Aumenta la producción de cetonas.', 0.41],
    ['48 – 72 h', 'Inicia la autofagia: reparación celular profunda.', 0.23],
    ['+ 72 h',    'Regeneración inmunológica y hormonal.', 0.085],
  ]
  const colW = CW / 4, R = 0.62, cy = 3.55
  stages.forEach((st, i) => {
    const x = M + i * colW, cx = x + R
    ring(s, cx, cy, R, RING, 0.75)
    disc(s, cx, cy, st[2], AMBER)
    s.addText(st[0], { x, y: cy + R + 0.34, w: colW - 0.55, h: 0.3, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 13, bold: true, color: BONE, charSpacing: 1.2, valign: 'middle' })
    s.addText(st[1], { x, y: cy + R + 0.72, w: colW - 0.55, h: 1.1, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 11.5, color: BODY, lineSpacingMultiple: 1.5, valign: 'top' })
  })
  footer(s, 4)
  s.addNotes('El círculo que se vacía reemplaza a las flechas: la escala es continua, no por bloques.')
}

/* ===================== 05 · RESPALDO CIENTÍFICO ===================== */
{
  const s = slideBase()
  eyebrow(s, 'RESPALDO CIENTÍFICO')
  title(s, 'Qué muestra la evidencia.', { w: 9 })

  const refs = [
    ['Yoshinori Ohsumi', 'Demostró el mecanismo de la autofagia. Premio Nobel de Medicina, 2016.'],
    ['Valter Longo', 'Observó regeneración inmune tras tres días de ayuno.'],
    ['Mark Mattson', 'Documentó protección cerebral y aumento del BDNF.'],
    ['Luigi Fontana', 'Registró mejoras metabólicas asociadas a longevidad.'],
  ]
  const cw = 5.1, gapX = CW - cw * 2, rows = [2.85, 4.62]
  refs.forEach((r, i) => {
    const x = M + (i % 2) * (cw + gapX), y = rows[Math.floor(i / 2)]
    disc(s, x + 0.045, y + 0.145, 0.045, AMBER)
    s.addText(r[0], { x: x + 0.3, y, w: cw - 0.3, h: 0.3, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 14.5, bold: true, color: BONE, valign: 'middle' })
    s.addText(r[1], { x: x + 0.3, y: y + 0.4, w: cw - 0.5, h: 0.9, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 11.5, color: BODY, lineSpacingMultiple: 1.5, valign: 'top' })
  })
  footer(s, 5)
  s.addNotes('Sin emojis: en la lámina que sostiene la autoridad, cada adorno resta.')
}

/* ===================== 06 · CASOS Y HALLAZGOS ===================== */
{
  const s = slideBase()
  eyebrow(s, 'CASOS Y HALLAZGOS')
  title(s, 'Qué pasó cuando se midió.', { w: 9 })

  const cases = [
    ['USC · 2014', 'Regeneración inmunológica', 'Pacientes que ayunaron 72 h antes de quimioterapia mostraron menos daño inmunológico y una recuperación más rápida.'],
    ['ITALIA · 2018', 'Control metabólico', 'Personas con resistencia a la insulina hicieron ayunos supervisados de 3 a 5 días y normalizaron glucosa y presión sin fármacos.'],
    ['ESTUDIO · 2019', 'Claridad mental', 'A las 36 h de ayuno, la dopamina y la noradrenalina aumentan: el cerebro entra en estado de alerta lúcida.'],
  ]
  const cw = 3.4, gap = (CW - cw * 3) / 2, top = 2.95
  cases.forEach((c, i) => {
    const x = M + i * (cw + gap)
    if (i > 0) s.addShape(pres.ShapeType.rect, { x: x - gap / 2, y: top, w: 0.008, h: 1.95, fill: { color: HAIR }, line: { color: HAIR, width: 0 } })
    s.addText(c[0], { x, y: top, w: cw, h: 0.26, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 9.5, bold: true, color: AMBER, charSpacing: 2.6, valign: 'middle' })
    s.addText(c[1], { x, y: top + 0.42, w: cw, h: 0.34, isTextBox: true, margin: 0, fontFace: SERIF, fontSize: 18, color: BONE, valign: 'middle' })
    s.addText(c[2], { x, y: top + 0.94, w: cw, h: 1.5, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 11.5, color: BODY, lineSpacingMultiple: 1.5, valign: 'top' })
  })
  footer(s, 6)
  s.addNotes('Tres hallazgos, uno por columna. Antes eran cajas ilegibles: ahora el texto es el protagonista.')
}

/* ===================== 07 · DIMENSIÓN ESPIRITUAL ===================== */
{
  const s = slideBase()
  ring(s, 10.7, 4.0, 2.15, RING, 0.75)
  ring(s, 10.7, 4.0, 2.75, RINGF, 0.5)
  eyebrow(s, 'DIMENSIÓN EMOCIONAL Y ESPIRITUAL')
  s.addText([
    { text: 'El ayuno limpia', options: { breakLine: true } },
    { text: 'más que el cuerpo', options: { color: AMBER } },
    { text: '.' },
  ], { x: M, y: 1.9, w: 6.4, h: 1.7, isTextBox: true, margin: 0, fontFace: SERIF, fontSize: 38, color: BONE, lineSpacingMultiple: 1.25, valign: 'top' })
  s.addText('En el vacío emergen memorias, emociones y comprensión. Es una práctica de humildad y entrega: no se trata de resistir, sino de soltar.', {
    x: M, y: 4.1, w: 5.9, h: 1.5, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 13, color: BODY, lineSpacingMultiple: 1.6, valign: 'top',
  })
  footer(s, 7)
  s.addNotes('Bisagra del deck: acá se pasa de la fisiología a la experiencia.')
}

/* ===================== 08 · PRÁCTICA (PAUSA) ===================== */
{
  const s = slideBase()
  ring(s, 6.67, 3.6, 1.5, RING, 0.75)
  ring(s, 6.67, 3.6, 2.15, RINGF, 0.5)
  ring(s, 6.67, 3.6, 2.8, RINGF, 0.5)
  s.addText('PRÁCTICA DE INTROSPECCIÓN', { x: 3.67, y: 1.5, w: 6, h: 0.26, isTextBox: true, margin: 0, align: 'center', fontFace: SANS, fontSize: 9.5, bold: true, color: AMBERD, charSpacing: 3.4, valign: 'middle' })
  s.addText('Cierra los ojos.\nRespira lento.', { x: 4.67, y: 3.0, w: 4, h: 1.3, isTextBox: true, margin: 0, align: 'center', fontFace: SERIF, fontSize: 26, italic: true, color: BONE, lineSpacingMultiple: 1.4, valign: 'middle' })
  s.addNotes('Silencio real de 30 a 60 segundos. No hablar sobre la lámina: dejarla hacer su trabajo.')
}

/* ===================== 09 · CÓMO SOSTENER EL PROCESO ===================== */
{
  const s = slideBase()
  eyebrow(s, 'CÓMO SOSTENER EL PROCESO')
  title(s, 'Sostener y volver.', { w: 9 })

  const items = [
    ['Durante', 'Hidratación, descanso y calma. Evitar estímulos intensos y esfuerzo físico exigente.'],
    ['Al romperlo', 'Con consciencia: caldos, probióticos y grasas buenas. Nunca una comida abundante.'],
    ['Después', 'La energía vuelve en pureza. Reintroducir alimentos de a poco, a lo largo del día.'],
  ]
  const cw = 3.4, gap = (CW - cw * 3) / 2, top = 3.0
  items.forEach((it, i) => {
    const x = M + i * (cw + gap)
    s.addShape(pres.ShapeType.rect, { x, y: top, w: cw, h: 2.2, fill: { color: PANEL }, line: { color: HAIR, width: 0.75 } })
    s.addText(it[0], { x: x + 0.4, y: top + 0.38, w: cw - 0.8, h: 0.3, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 10, bold: true, color: AMBER, charSpacing: 2.6, valign: 'middle' })
    s.addText(it[1], { x: x + 0.4, y: top + 0.82, w: cw - 0.8, h: 1.2, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 12, color: BODY, lineSpacingMultiple: 1.55, valign: 'top' })
  })
  footer(s, 9)
  s.addNotes('Lo práctico. La rotura del ayuno es donde más se equivoca la gente: insistir ahí.')
}

/* ===================== 10 · CUIDADOS (AGREGADA) ===================== */
{
  const s = slideBase()
  ring(s, 11.6, 2.0, 2.0, RINGF, 0.75)
  eyebrow(s, 'CUIDADOS')
  title(s, 'Cuándo no ayunar.', { w: 9 })
  s.addText('Un ayuno de más de 72 horas requiere supervisión profesional. No es una práctica para cualquier cuerpo ni para cualquier momento.', {
    x: M, y: 2.62, w: 6.6, h: 0.9, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 13, color: BODY, lineSpacingMultiple: 1.55, valign: 'top',
  })
  const contras = [
    'Embarazo y lactancia',
    'Diabetes tipo 1 o medicación hipoglucemiante',
    'Trastornos de la conducta alimentaria',
    'Bajo peso o desnutrición',
    'Insuficiencia renal o hepática',
    'Niños y adolescentes',
  ]
  contras.forEach((c, i) => {
    const x = M + (i % 2) * 5.7, y = 4.16 + Math.floor(i / 2) * 0.62
    disc(s, x + 0.045, y + 0.145, 0.045, AMBERD)
    s.addText(c, { x: x + 0.3, y, w: 5.2, h: 0.3, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 12.5, color: BONE, valign: 'middle' })
  })
  footer(s, 10)
  s.addNotes('LÁMINA AGREGADA. No estaba en el original: da responsabilidad y credibilidad. Sacala si el marco de la charla ya la cubre.')
}

/* ===================== 11 · INTEGRACIÓN DIARIA ===================== */
{
  const s = slideBase()
  ring(s, 2.6, 5.4, 2.4, RINGF, 0.75)
  eyebrow(s, 'INTEGRACIÓN DIARIA')
  s.addText([
    { text: 'Ayunar no es huir del alimento:', options: { breakLine: true } },
    { text: 'es redescubrir la saciedad interna', options: { color: AMBER } },
    { text: '.' },
  ], { x: M, y: 2.15, w: 10.4, h: 1.6, isTextBox: true, margin: 0, fontFace: SERIF, fontSize: 33, color: BONE, lineSpacingMultiple: 1.3, valign: 'top' })
  s.addText('Pequeñas pausas diarias recuerdan que el cuerpo es un templo de energía. No hace falta un ayuno largo para practicar el vacío.', {
    x: M, y: 4.25, w: 6.2, h: 1.2, isTextBox: true, margin: 0, fontFace: SANS, fontSize: 13, color: BODY, lineSpacingMultiple: 1.6, valign: 'top',
  })
  footer(s, 11)
  s.addNotes('Bajar la práctica a la vida cotidiana antes del cierre.')
}

/* ===================== 12 · CITA FINAL ===================== */
{
  const s = slideBase()
  ring(s, 6.67, 3.62, 2.55, RING, 0.75)
  ring(s, 6.67, 3.62, 3.25, RINGF, 0.5)
  s.addText('“', { x: 4.67, y: 1.35, w: 4, h: 0.9, isTextBox: true, margin: 0, align: 'center', fontFace: SERIF, fontSize: 86, color: RING, valign: 'middle' })
  s.addText([
    { text: 'Cuando dejas de alimentarte de materia,', options: { italic: true, breakLine: true } },
    { text: 'comienzas a ', options: { italic: true } },
    { text: 'nutrirte de energía', options: { italic: true, color: AMBER } },
    { text: '.', options: { italic: true } },
  ], {
    x: 1.6, y: 3.05, w: 10.13, h: 1.7, isTextBox: true, margin: 0, align: 'center',
    fontFace: SERIF, fontSize: 28, color: BONE, lineSpacingMultiple: 1.5, valign: 'top',
  })
  s.addText('GRACIAS', { x: 4.67, y: 5.35, w: 4, h: 0.26, isTextBox: true, margin: 0, align: 'center', fontFace: SANS, fontSize: 9.5, bold: true, color: AMBERD, charSpacing: 4, valign: 'middle' })
  s.addNotes('Cierre. Dejar la lámina en pantalla mientras se abren preguntas.')
}

pres.writeFile({ fileName: 'ayuno.pptx' }).then(f => console.log('escrito:', f))
