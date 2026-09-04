const SP = process.env.DOCX_MODULES || '.';
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel,
  BorderStyle, LevelFormat, convertInchesToTwip,
} = require(SP === '.' ? 'docx' : SP + '/node_modules/docx');
const fs = require('fs');

const GOLD = 'C9A84C';
const INK = '1A1A1A';
const FONT = 'Calibri';

const p = (children, opts = {}) => new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { after: 200, line: 276 },
  ...opts,
  children,
});
const t = (text, opts = {}) => new TextRun({ text, font: FONT, size: 22, color: INK, ...opts });

const doc = new Document({
  creator: 'Aura Productions',
  title: 'Solicitud de cambio de sala — Cumbre de los Millonarios Conscientes',
  description: 'Carta a Espacio Riesco solicitando el cambio de Sala Expo Center a Gran Salon — Cumbre de los Millonarios Conscientes, 12 y 13 de septiembre de 2026',
  numbering: {
    config: [{
      reference: 'args',
      levels: [{
        level: 0,
        format: LevelFormat.DECIMAL,
        text: '%1.',
        alignment: AlignmentType.START,
        style: {
          paragraph: { indent: { left: convertInchesToTwip(0.35), hanging: convertInchesToTwip(0.25) } },
          run: { bold: true, color: GOLD, font: FONT, size: 22 },
        },
      }],
    }],
  },
  sections: [{
    properties: {
      page: { margin: { top: 1300, bottom: 1300, left: 1440, right: 1440 } },
    },
    children: [
      // ---------- Membrete ----------
      new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { after: 60 },
        children: [new TextRun({
          text: 'AURA PRODUCTIONS',
          font: FONT, size: 28, bold: true, color: GOLD, characterSpacing: 60,
        })],
      }),
      new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { after: 320 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: GOLD, space: 8 } },
        children: [new TextRun({
          text: 'Producción de eventos y experiencias  ·  hola@auraproductions.com.ar',
          font: FONT, size: 17, color: '7A7A7A',
        })],
      }),

      // ---------- Lugar y fecha ----------
      p([t('Santiago de Chile, 4 de septiembre de 2026')], { alignment: AlignmentType.RIGHT, spacing: { after: 360 } }),

      // ---------- Destinatario ----------
      p([t('Sres.')], { alignment: AlignmentType.LEFT, spacing: { after: 0 } }),
      p([t('Departamento Comercial', { bold: true })], { alignment: AlignmentType.LEFT, spacing: { after: 0 } }),
      p([t('Espacio Riesco', { bold: true })], { alignment: AlignmentType.LEFT, spacing: { after: 0 } }),
      p([t('Santiago de Chile')], { alignment: AlignmentType.LEFT, spacing: { after: 360 } }),

      // ---------- Referencia ----------
      p([
        t('REF.: ', { bold: true, color: GOLD }),
        t('Solicitud formal de cambio de sala — de Sala Expo Center (4.600 m²) a Gran Salón (1.600 m²) — Cumbre de los Millonarios Conscientes, 12 y 13 de septiembre de 2026.', { bold: true }),
      ], { alignment: AlignmentType.LEFT, spacing: { after: 320 } }),

      // ---------- Cuerpo ----------
      p([t('De nuestra mayor consideración:')], { alignment: AlignmentType.LEFT, spacing: { after: 240 } }),

      p([t('Por medio de la presente, y en representación de Aura Productions, productora responsable de la Cumbre de los Millonarios Conscientes, a realizarse los días 12 y 13 de septiembre de 2026 en sus instalaciones, nos dirigimos a ustedes con el objeto de solicitar formalmente el cambio de la sala oportunamente reservada, pasando de la Sala Expo Center (4.600 m²) al Gran Salón (1.600 m²).')]),

      p([t('Fundamentamos nuestro pedido en los siguientes puntos:')], { spacing: { after: 200 } }),

      p([
        t('Adecuación del espacio al aforo confirmado. ', { bold: true }),
        t('Al día de la fecha contamos con 1.600 personas confirmadas. El Gran Salón, con sus 1.600 m², ofrece la capacidad necesaria para recibirlas con comodidad y con los estándares de circulación, seguridad y servicio que exige un evento de estas características.'),
      ], { numbering: { reference: 'args', level: 0 }, spacing: { after: 160 } }),

      p([
        t('Calidad de la experiencia y percepción del evento. ', { bold: true }),
        t('Una sala de 4.600 m² ocupada por 1.600 asistentes genera una inevitable sensación de vacío que atenta contra la atmósfera del encuentro. Que la sala se vea llena no es un detalle estético: es parte central de la experiencia que comprometimos con nuestro público, nuestros sponsors y nuestros oradores, y condiciona además todo el registro audiovisual con el que comunicamos el evento.'),
      ], { numbering: { reference: 'args', level: 0 }, spacing: { after: 160 } }),

      p([
        t('Montaje ya recotizado y aprobado. ', { bold: true }),
        t('Contamos con la recotización de nuestro proveedor técnico y con el montaje aprobado para el Gran Salón. Por lo tanto, el cambio no implica demoras, retrabajos ni ajustes adicionales en la planificación operativa acordada.'),
      ], { numbering: { reference: 'args', level: 0 }, spacing: { after: 160 } }),

      p([
        t('Rentabilidad y sostenibilidad del proyecto. ', { bold: true }),
        t('El correcto dimensionamiento de la sala es determinante para la rentabilidad de esta edición. Que este evento cierre en positivo es, precisamente, la condición que nos habilita a proyectar las próximas ediciones junto a ustedes.'),
      ], { numbering: { reference: 'args', level: 0 }, spacing: { after: 320 } }),

      p([
        t('Proyección de crecimiento y compromiso a futuro. ', { bold: true }),
        t('Queremos ser transparentes respecto de nuestra visión: la Cumbre de los Millonarios Conscientes es un proyecto con un plan de escalamiento anual sostenido. En Argentina pasamos de 3.000 asistentes el año pasado a un aforo de 6.000 personas en la edición de este año, y nuestro objetivo es replicar esa misma curva de crecimiento en Chile. Bajo esa lógica, nuestra proyección para la edición 2027 es de entre 3.000 y 4.000 asistentes, volumen para el cual la Sala Expo Center resulta el espacio natural y al que aspiramos a llegar de la mano de ustedes.'),
      ]),

      p([t('En otras palabras, no buscamos reducir nuestra presencia en el predio, sino ordenarla en el tiempo: la sala adecuada este año y el Expo Center en 2027. Para que ese crecimiento sea posible, necesitamos que esta edición sea rentable.')]),

      p([t('Dada la proximidad de la fecha, quedamos a entera disposición para resolver de manera inmediata los aspectos contractuales, la eventual diferencia de tarifas y la readecuación del cronograma de montaje que el cambio requiera. Agradeceremos su confirmación a la mayor brevedad posible, a fin de dar aviso a nuestros proveedores y no afectar el cronograma de producción.')]),

      p([t('Agradecemos desde ya la atención dispensada y confiamos en contar con una respuesta favorable, en el marco de la relación de trabajo a largo plazo que deseamos construir con ustedes.')]),

      p([t('Sin otro particular, saludamos a ustedes muy atentamente.')], { spacing: { after: 700 } }),

      // ---------- Firma ----------
      new Paragraph({
        alignment: AlignmentType.LEFT,
        spacing: { after: 60 },
        border: { top: { style: BorderStyle.SINGLE, size: 6, color: 'B0B0B0', space: 6 } },
        indent: { right: convertInchesToTwip(3.6) },
        children: [t('[Nombre y apellido]', { bold: true })],
      }),
      p([t('[Cargo] — Aura Productions')], { alignment: AlignmentType.LEFT, spacing: { after: 0 } }),
      p([t('hola@auraproductions.com.ar  ·  [Teléfono]', { color: '7A7A7A', size: 19 })], { alignment: AlignmentType.LEFT }),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(process.argv[2], buf);
  console.log('escrito:', process.argv[2]);
});
