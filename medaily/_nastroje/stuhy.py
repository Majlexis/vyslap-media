"""Návrhy stúh pre medaily Vyšľap si medailu – výstup PNG (rozložená stuha + detail)."""
import math, sys
import cairosvg

DLZKA, SIRKA = 900, 25        # mm
POL = DLZKA / 2
KREM, ZLTA, TMZEL = "#f6f3e9", "#ffca1b", "#063f2d"


def logo(cx, cy, uhol=0, w=27, h=19):
    """Krémový štítok s horami a slnkom (ako na medaile)."""
    return f'''<g transform="translate({cx},{cy})">
  <rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="0.6" fill="{KREM}"/>
  <circle cx="{w*0.2}" cy="{-h*0.12}" r="{h*0.17}" fill="{ZLTA}"/>
  <path d="M{-w*0.36},{h*0.3} L{-w*0.08},{-h*0.22} L{w*0.2},{h*0.3} Z" fill="{TMZEL}"/>
  <path d="M{-w*0.02},{h*0.3} L{w*0.14},{h*0.02} L{w*0.32},{h*0.3} Z" fill="{TMZEL}"/>
  <path d="M{-w*0.02},{h*0.3} L{w*0.14},{h*0.02}" stroke="{KREM}" stroke-width="0.6"/>
</g>'''


def vlocka(cx, cy, r, farba=KREM):
    s = []
    for i in range(8):
        a = math.radians(i * 45)
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{farba}" stroke-width="1.1" stroke-linecap="round"/>')
        for k in (0.55,):
            bx, by = cx + r * k * math.cos(a), cy + r * k * math.sin(a)
            for d in (-35, 35):
                b = a + math.radians(180 + d)
                s.append(f'<line x1="{bx:.2f}" y1="{by:.2f}" x2="{bx + r*0.32*math.cos(b+math.pi):.2f}" y2="{by + r*0.32*math.sin(b+math.pi):.2f}" stroke="{farba}" stroke-width="0.8" stroke-linecap="round"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.14}" fill="{ZLTA}"/>')
    return "".join(s)


def nordicky_pas(x):
    """Pás so zimným vzorom naprieč stuhou (široký ~9 mm)."""
    s = [f'<line x1="{x-4.5}" y1="0" x2="{x-4.5}" y2="{SIRKA}" stroke="{KREM}" stroke-width="0.5"/>',
         f'<line x1="{x+4.5}" y1="0" x2="{x+4.5}" y2="{SIRKA}" stroke="{KREM}" stroke-width="0.5"/>']
    n = 6
    for i in range(n):
        y = (i + 0.5) * SIRKA / n
        h = SIRKA / n / 2
        s.append(f'<path d="M{x-1.6},{y} L{x},{y-h*0.9} L{x+1.6},{y} L{x},{y+h*0.9} Z" fill="{ZLTA}"/>')
        s.append(f'<circle cx="{x-3.2}" cy="{y}" r="0.45" fill="{KREM}"/><circle cx="{x+3.2}" cy="{y}" r="0.45" fill="{KREM}"/>')
    return "".join(s)


def srdce(cx, cy, r, uhol, farba):
    return f'''<g transform="translate({cx},{cy}) rotate({uhol}) scale({r/10})">
<path d="M0,8 C-10,0 -10,-8 -5,-9 C-2,-9.5 0,-7 0,-5 C0,-7 2,-9.5 5,-9 C10,-8 10,0 0,8 Z" fill="{farba}"/></g>'''


def text(x, y, obsah, velkost, farba, pismo, kotva="middle", sirka_pism=0.6):
    return (f'<text x="{x}" y="{y}" font-family="{pismo}" font-weight="bold" font-size="{velkost}" '
            f'fill="{farba}" text-anchor="{kotva}" letter-spacing="{sirka_pism}">{obsah}</text>')


def polovica_novorocnych(prava):
    """Prvky jednej polovice; x od konca pri medaile (0) po stred pri krku (450)."""
    hore = 0
    def X(x): return POL - x if prava else x
    p = [vlocka(X(18), SIRKA/2, 8.5),
         nordicky_pas(X(40)),
         logo(X(66), SIRKA/2, hore),
         nordicky_pas(X(92))]
    # nápis – číta sa v smere zavesenia (zdola nahor vľavo, zhora nadol vpravo)
    tx = X(176)
    p.append(text(tx, 10.6, "NOVOROČNÝCH", 8.2, KREM, "Liberation Sans"))
    p.append(text(tx, 21.2, "100 KM", 9.6, ZLTA, "Liberation Sans"))
    p += [nordicky_pas(X(262)), vlocka(X(290), SIRKA/2, 7),
          nordicky_pas(X(318)),
          text(X(384), 15.6, "VYSLAPSIMEDAILU.SK", 5.2, KREM, "Liberation Sans", sirka_pism=0.5),
          nordicky_pas(X(444))]
    return "".join(p)


def polovica_valentinska(prava):
    hore = 0
    def X(x): return POL - x if prava else x
    p = [srdce(X(16), SIRKA/2, 8, hore, KREM),
         logo(X(46), SIRKA/2, hore)]
    for i, x in enumerate((72, 78, 84)):
        p.append(srdce(X(x), SIRKA/2, 2.2 + (i % 2) * 0.6, hore, ZLTA if i == 1 else KREM))
    tx = X(170)
    p.append(text(tx, 11.0, "VALENTÍNSKA", 8.0, KREM, "DejaVu Serif"))
    p.append(text(tx, 20.4, "DVOJICA", 8.0, KREM, "DejaVu Serif", sirka_pism=1.6))
    for i, x in enumerate((256, 262, 268)):
        p.append(srdce(X(x), SIRKA/2, 2.2 + (i % 2) * 0.6, hore, ZLTA if i == 1 else KREM))
    p += [srdce(X(300), SIRKA/2, 6, hore, KREM),
          text(X(384), 15.6, "VYSLAPSIMEDAILU.SK", 5.2, KREM, "DejaVu Serif", sirka_pism=0.4),
          srdce(X(438), SIRKA/2, 3, hore, ZLTA)]
    return "".join(p)


def stuha(farba, polovica, okraje=None):
    """Celá stuha 900×25 mm v súradniciach mm."""
    defs = f'''<defs>
<pattern id="tkanina" width="0.6" height="0.6" patternUnits="userSpaceOnUse">
  <rect width="0.6" height="0.3" fill="#000" opacity="0.05"/></pattern>
<pattern id="tkanina2" width="0.8" height="0.8" patternUnits="userSpaceOnUse">
  <rect width="0.35" height="0.8" fill="#fff" opacity="0.025"/></pattern>
<linearGradient id="tien" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#000" stop-opacity="0.18"/><stop offset="0.12" stop-color="#000" stop-opacity="0"/>
  <stop offset="0.5" stop-color="#fff" stop-opacity="0.04"/>
  <stop offset="0.88" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.2"/>
</linearGradient></defs>'''
    obsah = [f'<rect width="{DLZKA}" height="{SIRKA}" fill="{farba}"/>']
    if okraje:
        obsah += [f'<rect y="1.1" width="{DLZKA}" height="0.45" fill="{okraje}"/>',
                  f'<rect y="{SIRKA-1.55}" width="{DLZKA}" height="0.45" fill="{okraje}"/>']
    obsah.append(f'<g>{polovica(False)}</g>')
    obsah.append(f'<g transform="translate({POL},0)">{polovica(True)}</g>')
    obsah += [f'<rect width="{DLZKA}" height="{SIRKA}" fill="url(#tkanina)"/>',
              f'<rect width="{DLZKA}" height="{SIRKA}" fill="url(#tkanina2)"/>',
              f'<rect width="{DLZKA}" height="{SIRKA}" fill="url(#tien)"/>']
    return defs + "".join(obsah)


def harok(nazov, podnazov, farba, polovica, farby, okraje=None, ks="1 ks na medailu"):
    """Náhľadový hárok: rozložená stuha (2 polovice pod sebou) + detail + farby."""
    W = 2400
    m = 80
    sk = (W - 2 * m) / POL          # px na mm pre polovicu
    hp = SIRKA * sk                  # výška pásu
    s = stuha(farba, polovica, okraje)
    y1 = 230
    y2 = y1 + hp + 120
    # detail: úsek 0–230 mm zväčšený
    det_mm = 230
    dsk = (W - 2 * m) / det_mm
    yd = y2 + hp + 170
    hd = SIRKA * dsk
    yf = yd + hd + 120
    H = yf + 190
    f = "Liberation Sans"
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}">',
           f'<rect width="{W}" height="{H}" fill="#fbfaf6"/>',
           f'<text x="{m}" y="105" font-family="{f}" font-weight="bold" font-size="54" fill="#1c2a20">{nazov}</text>',
           f'<text x="{m}" y="160" font-family="{f}" font-size="30" fill="#4a5a4f">{podnazov}</text>',
           # ľavá polovica
           f'<text x="{m}" y="{y1-22}" font-family="{f}" font-weight="bold" font-size="24" fill="#1c2a20">ĽAVÁ POLOVICA  ·  medaila → krk</text>',
           f'<svg x="{m}" y="{y1}" width="{W-2*m}" height="{hp}" viewBox="0 0 {POL} {SIRKA}">{s}</svg>',
           f'<text x="{m}" y="{y2-22}" font-family="{f}" font-weight="bold" font-size="24" fill="#1c2a20">PRAVÁ POLOVICA  ·  krk → medaila</text>',
           f'<svg x="{m}" y="{y2}" width="{W-2*m}" height="{hp}" viewBox="{POL} 0 {POL} {SIRKA}">{s}</svg>',
           f'<text x="{W-m}" y="{y1+hp+38}" font-family="{f}" font-size="22" fill="#6b776f" text-anchor="end">↑ stred stuhy (krk)</text>',
           f'<text x="{m}" y="{y2+hp+38}" font-family="{f}" font-size="22" fill="#6b776f">↑ stred stuhy (krk)</text>',
           # detail
           f'<text x="{m}" y="{yd-22}" font-family="{f}" font-weight="bold" font-size="24" fill="#1c2a20">DETAIL  ·  koniec pri medaile, prvých {det_mm} mm</text>',
           f'<svg x="{m}" y="{yd}" width="{W-2*m}" height="{hd}" viewBox="0 0 {det_mm} {SIRKA}">{s}</svg>',
           ]
    # farby
    x = m
    svg.append(f'<text x="{m}" y="{yf-22}" font-family="{f}" font-weight="bold" font-size="24" fill="#1c2a20">FARBY</text>')
    for meno, hexa in farby:
        svg.append(f'<rect x="{x}" y="{yf}" width="64" height="64" rx="8" fill="{hexa}" stroke="#d8d4c8"/>')
        svg.append(f'<text x="{x+80}" y="{yf+28}" font-family="{f}" font-weight="bold" font-size="24" fill="#1c2a20">{meno}</text>')
        svg.append(f'<text x="{x+80}" y="{yf+58}" font-family="{f}" font-size="22" fill="#6b776f">{hexa}</text>')
        x += 400
    svg.append(f'<text x="{W-m}" y="{yf+28}" font-family="{f}" font-size="22" fill="#6b776f" text-anchor="end">Sublimačná potlač, obojstranne rovnaká</text>')
    svg.append(f'<text x="{W-m}" y="{yf+58}" font-family="{f}" font-size="22" fill="#6b776f" text-anchor="end">{ks} · rozmery upresní výrobca</text>')
    svg.append('</svg>')
    return "".join(svg), s


def uloz(svg, cesta):
    cairosvg.svg2png(bytestring=svg.encode(), write_to=cesta)


if __name__ == "__main__":
    out = sys.argv[1]
    zel = "#0b4a30"
    svg, s1 = harok("Stuha – Novoročných 100", "Návrh stuhy · 25 × 900 mm · tmavozelená so zimným vzorom",
                    zel, polovica_novorocnych,
                    [("Zelená stuha", zel), ("Žltá", ZLTA), ("Krémová", KREM), ("Logo hory", TMZEL)])
    uloz(svg, f"{out}/stuha-novorocnych-100.png")
    bord = "#8a1a2b"
    svg, s2 = harok("Stuha – Valentínska dvojica", "Návrh stuhy · 25 × 900 mm · bordová so srdiečkami",
                    bord, polovica_valentinska,
                    [("Bordová stuha", bord), ("Krémová", KREM), ("Žltá", ZLTA), ("Logo hory", TMZEL)],
                    okraje=KREM, ks="2 ks na pár (každá polovica medaily má svoju)")
    uloz(svg, f"{out}/stuha-valentinska-dvojica.png")
    # samotné stuhy bez popisov (súbor pre výrobcu)
    for meno, s in (("novorocnych-100", s1), ("valentinska-dvojica", s2)):
        cela = f'<svg xmlns="http://www.w3.org/2000/svg" width="9000" height="250" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>'
        uloz(cela, f"{out}/stuha-{meno}-tlac.png")
        open(f"{out}/stuha-{meno}-tlac.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{DLZKA}mm" height="{SIRKA}mm" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>')
