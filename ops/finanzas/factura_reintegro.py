# -*- coding: utf-8 -*-
"""
Genera la factura de reintegro de gastos en el formato estandar de CMC 2026.

Reproduce exactamente el layout de la factura 2601020 (Carlos Calderon - Camerinos Panama):
encabezado con la persona y el pais, numero de factura y fecha, entidad facturadora,
detalle numerado de comprobantes, subtotal, cargo bancario y total a reintegrar,
y los datos de la cuenta receptora.

Uso:
    python factura_reintegro.py ejemplo.json salida.pdf
    python factura_reintegro.py --demo            # genera demo_2601020.pdf

El JSON de entrada es el que va a producir el agente de WhatsApp a partir de la hoja
GASTOS EQUIPO del consolidado. Ver ESQUEMA al final del archivo.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# --- geometria tomada de la factura 2601020 (puntos, origen abajo-izquierda) ---
MARGEN_IZQ = 56.69291
MARGEN_DER = 538.5827
ANCHO = A4[0]


@dataclass
class Factura:
    numero: str
    fecha: str                      # dd/mm/aaaa
    beneficiario: str
    rol_y_evento: str               # p.ej. "Staff - CMC 2026"
    pais: str
    concepto: str                   # p.ej. "Compras Camerinos (Panama) CC"
    moneda: str = "USD"
    items: list = field(default_factory=list)   # [{"detalle": str, "monto": float}]
    cargo_bancario: float = 0.0
    cargo_bancario_detalle: str = ""
    emisor_nombre: str = "IIDAI LLC"
    emisor_lineas: list = field(default_factory=lambda: [
        "EIN 88-3419107",
        "MBR 1401 BRICKELL AVE",
        "STE 330 MIAMI,",
        "FL 33131. United States",
    ])
    cuenta: dict = field(default_factory=dict)
    nota_pie: str = ("Moneda: Dolares estadounidenses (USD). Incluye comision de recepcion "
                     "para que el beneficiario perciba el monto neto completo.")

    @property
    def subtotal(self) -> float:
        return round(sum(i["monto"] for i in self.items), 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.cargo_bancario, 2)


def _der(c, texto, y, x_der=MARGEN_DER):
    """Escribe alineado a la derecha del cuadro, como en el original."""
    c.drawRightString(x_der, y, texto)


def render(f: Factura, salida: str) -> str:
    c = canvas.Canvas(salida, pagesize=A4)
    c.setTitle(f"Factura {f.numero} - {f.beneficiario}")

    # --- encabezado izquierdo: persona ---
    y = 771.0236
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGEN_IZQ, y, f.beneficiario.upper())
    c.setFont("Helvetica", 9)
    c.drawString(MARGEN_IZQ, 756.8504, f.rol_y_evento)
    c.drawString(MARGEN_IZQ, 742.6772, f.pais)

    # --- encabezado derecho: numero y fecha ---
    c.setFont("Helvetica-Bold", 11)
    _der(c, f"FACTURA/INVOICE: {f.numero}", 771.0236)
    c.setFont("Helvetica", 9)
    _der(c, f"Fecha/Date: {f.fecha}", 754.0157)
    _der(c, "REINTEGRO DE GASTOS / EXPENSE REIMBURSEMENT", 737.0079)

    # --- entidad facturadora ---
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGEN_IZQ, 708.6614, f.emisor_nombre)
    c.setFont("Helvetica", 9)
    y = 694.4882
    for linea in f.emisor_lineas:
        c.drawString(MARGEN_IZQ, y, linea)
        y -= 14.1732

    # --- concepto ---
    y_concepto = 617.9528
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGEN_IZQ, y_concepto, f"CONCEPT - {f.concepto}")
    _der(c, f.moneda, y_concepto, 538.5827)
    c.line(MARGEN_IZQ, 612.2835, MARGEN_DER, 612.2835)

    # --- detalle ---
    c.setFont("Helvetica", 8.8)
    y = 595.2756
    for n, item in enumerate(f.items, 1):
        c.drawString(MARGEN_IZQ, y, f"{n}. {item['detalle']}")
        _der(c, f"{item['monto']:,.2f}", y)
        y -= 14.1732
    y_linea = y - 5.5
    c.line(340.1575, y_linea, MARGEN_DER, y_linea)

    # --- totales ---
    c.setFont("Helvetica", 9.5)
    y = y_linea - 17.0
    c.drawString(MARGEN_IZQ, y, f"Subtotal compras ({len(f.items)} comprobantes)")
    _der(c, f"{f.subtotal:,.2f}", y)
    if f.cargo_bancario:
        y -= 17.0079
        c.drawString(MARGEN_IZQ, y, f.cargo_bancario_detalle or "Cargo por recepcion de transferencia internacional")
        _der(c, f"{f.cargo_bancario:,.2f}", y)
    y -= 19.8425
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(MARGEN_IZQ, y, "TOTAL A REINTEGRAR")
    _der(c, f"{f.moneda} {f.total:,.2f}", y)
    y_sep = y - 28.3465
    c.line(MARGEN_IZQ, y_sep, MARGEN_DER, y_sep)

    # --- cuenta receptora ---
    y = y_sep - 22.6772
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGEN_IZQ, y, "Datos cuenta receptora:")
    c.setFont("Helvetica", 9)
    y -= 14.7402
    for etiqueta, valor in f.cuenta.items():
        c.drawString(MARGEN_IZQ, y, f"{etiqueta}: {valor}")
        y -= 14.7402

    # --- nota ---
    y -= 8
    c.setFont("Helvetica-Oblique", 8.5)
    c.drawString(MARGEN_IZQ, y, f.nota_pie)

    c.showPage()
    c.save()
    return salida


DEMO = Factura(
    numero="2601020",
    fecha="11/08/2026",
    beneficiario="Carlos Andres Calderon Arbelaez",
    rol_y_evento="Staff - CMC 2026",
    pais="Panama",
    concepto="Compras Camerinos (Panama) CC",
    items=[
        {"detalle": "Riba Smith - Camerinos Speakers / Staff", "monto": 133.81},
        {"detalle": "Price Smart - Agua", "monto": 22.47},
        {"detalle": "REY - Camerinos Speakers / Staff", "monto": 26.12},
        {"detalle": "REY - Pastillas herbales garganta", "monto": 3.43},
        {"detalle": "Farmacias Arrocha - Kleenex y shot jengibre", "monto": 3.57},
        {"detalle": "Novey - Agua", "monto": 8.50},
        {"detalle": "Novey - Agua", "monto": 4.25},
        {"detalle": "Starbucks - Camerinos Speakers", "monto": 20.17},
        {"detalle": "Starbucks - Camerinos Speakers", "monto": 12.72},
        {"detalle": "UltraCom - Folders", "monto": 4.49},
        {"detalle": "Adamski Gonzalez - Palosanto", "monto": 15.00},
        {"detalle": "Daniela Gerena (Gerena Group) - Impresiones (Fact. N 0000000181)", "monto": 43.00},
    ],
    cargo_bancario=37.45,
    cargo_bancario_detalle="Cargo por recepcion de transferencia internacional (Banco General, Panama)",
    cuenta={
        "Titular/Holder": "CARLOS ANDRES CALDERON ARBELAEZ",
        "Banco/Bank": "BANCO GENERAL, S.A. - PANAMA",
        "SWIFT": "BAGEPAPA",
        "Tipo de cuenta": "Cuenta de ahorros",
        "Numero de cuenta": "0410983865724",
        "Banco intermediario": "CITIBANK, N.A. - NEW YORK",
        "SWIFT ": "CITIUS33 - ABA: 021000089",
    },
)


def main(argv):
    if len(argv) > 1 and argv[1] == "--demo":
        salida = argv[2] if len(argv) > 2 else "demo_2601020.pdf"
        print(render(DEMO, salida))
        return 0
    if len(argv) < 3:
        print(__doc__)
        return 1
    datos = json.load(open(argv[1], encoding="utf-8"))
    print(render(Factura(**datos), argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

# ESQUEMA del JSON de entrada
# {
#   "numero": "2601021",
#   "fecha": "08/09/2026",
#   "beneficiario": "Nombre Apellido",
#   "rol_y_evento": "Staff - CMC 2026",
#   "pais": "Chile",
#   "concepto": "Compras Camerinos (Chile) NA",
#   "moneda": "USD",
#   "items": [{"detalle": "Comercio - concepto", "monto": 12.34}],
#   "cargo_bancario": 0,
#   "cargo_bancario_detalle": "",
#   "cuenta": {"Titular/Holder": "...", "Banco/Bank": "...", "SWIFT": "..."}
# }
