# Presupuesto Mastermind Circulo Interno - 70 pax - Medellin 20-22 oct 2026
# Estimaciones de mercado Medellin, segmento luxury. Sujeto a cotizacion formal.
TRM = 4000  # COP por USD (supuesto de trabajo)
PAX = 70

# (concepto, unidad, [esencial, signature, iconico]) en COP
# 'pp' = por persona (se multiplica x70), 'fijo' = monto total
L = [
 ("Alquiler sala principal (2 dias completos)","fijo",[ 8_000_000, 12_000_000, 18_000_000]),
 ("Estacion de hidratacion permanente 10-22h (2 dias)","pp",[   70_000,    95_000,   130_000]),
 ("Coctel de bienvenida sin alcohol (lun 20, 2h)","pp",[  110_000,   155_000,   225_000]),
 ("Almuerzo colombiano tipico (mie 21)","pp",[  105_000,   140_000,   195_000]),
 ("Cena de cierre en venue externo (jue 22)","pp",[  230_000,   320_000,   480_000]),
 ("Fiesta consciente (DJ, sonido, luces, facilitador, cacao)","fijo",[11_000_000, 18_000_000, 28_000_000]),
 ("Kit empresarial premium","pp",[  340_000,   480_000,   760_000]),
 ("Produccion AV sala (pantalla, sonido, micros, tecnico x2 dias)","fijo",[ 9_000_000, 14_000_000, 22_000_000]),
 ("Escenografia, branding, senaletica y carteles de mesa","fijo",[ 6_000_000, 10_000_000, 16_000_000]),
 ("Fotografia + video + edicion","fijo",[ 7_000_000, 12_000_000, 19_000_000]),
 ("Staff de produccion y anfitriones","fijo",[ 6_000_000,  9_000_000, 13_000_000]),
 ("Traslados internos (shuttle a cena y fiesta)","fijo",[ 3_500_000,  5_500_000,  8_500_000]),
]
ESC = ["ESENCIAL","SIGNATURE","ICONICO"]
IMPREV = 0.08
FEE = 0.15  # honorarios de produccion Aura

for i,name in enumerate(ESC):
    print("="*74); print(f"ESCENARIO {name}"); print("="*74)
    sub = 0
    for c,u,v in L:
        t = v[i]*PAX if u=="pp" else v[i]
        sub += t
        det = f"{v[i]:>11,} x{PAX}" if u=="pp" else f"{'':>11}    "
        print(f"  {c:<58} {det}  COP {t:>12,}")
    imp = round(sub*IMPREV); fee = round((sub+imp)*FEE); tot = sub+imp+fee
    print(f"  {'-'*70}")
    print(f"  {'Subtotal':<58} {'':>15}  COP {sub:>12,}")
    print(f"  {'Imprevistos 8%':<58} {'':>15}  COP {imp:>12,}")
    print(f"  {'Honorarios de produccion 15%':<58} {'':>15}  COP {fee:>12,}")
    print(f"  {'TOTAL':<58} {'':>15}  COP {tot:>12,}")
    print(f"  {'TOTAL USD (TRM 4.000)':<58} {'':>15}  USD {round(tot/TRM):>12,}")
    print(f"  {'COSTO POR PERSONA':<58} {'':>15}  USD {round(tot/TRM/PAX):>12,}\n")
