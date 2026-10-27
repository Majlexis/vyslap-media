"""Návrhy stúh pre medaily Vyšľap si medailu – výstup PNG (rozložená stuha + detail)."""
import math, sys
import cairosvg

DLZKA, SIRKA = 900, 25        # mm
POL = DLZKA / 2
KREM, ZLTA, TMZEL = "#f6f3e9", "#ffca1b", "#063f2d"
MODRA = "#0f4a6e"


def logo(cx, cy, uhol=0, w=27, h=19):
    """Krémový štítok so skutočným logom (public/logo.svg z webu: tri hory + slnko)."""
    pad_x, pad_y = w * 0.14, h * 0.16
    return f'''<g transform="translate({cx},{cy})">
  <rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="0.6" fill="{KREM}"/>
  <svg x="{-w/2+pad_x}" y="{-h/2+pad_y}" width="{w-2*pad_x}" height="{h-2*pad_y}" viewBox="6 6 139 91" preserveAspectRatio="xMidYMid meet">
    <circle cx="118" cy="27" r="19" fill="{ZLTA}"/>
    <path d="M9 93 63 29 83 53 51 93Z M56 93 83 61 108 93Z M85 58 99 42 142 94 108 93Z" fill="{TMZEL}"/>
  </svg>
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


TYRKYS = "#46b9c8"


def vlnky_pas(x, sirka=10):
    """Pás s vlnkami hladiny naprieč stuhou."""
    s = [f'<line x1="{x-sirka/2}" y1="0" x2="{x-sirka/2}" y2="{SIRKA}" stroke="{ZLTA}" stroke-width="0.5"/>',
         f'<line x1="{x+sirka/2}" y1="0" x2="{x+sirka/2}" y2="{SIRKA}" stroke="{ZLTA}" stroke-width="0.5"/>']
    for dx in (-2.2, 0, 2.2):
        d = f"M{x+dx},0"
        for i in range(10):
            y = (i + 1) * SIRKA / 10
            d += f" Q{x+dx+(1.1 if i % 2 == 0 else -1.1)},{y - SIRKA/20} {x+dx},{y}"
        s.append(f'<path d="{d}" fill="none" stroke="{TYRKYS if dx else KREM}" stroke-width="0.55" stroke-linecap="round"/>')
    return "".join(s)


def kvapka(cx, cy, r, farba=KREM, vnutro=None):
    """Kvapka špičkou hore (ako tvar medaily)."""
    d = f"M{cx},{cy-r*1.45} C{cx+r*0.35},{cy-r*0.85} {cx+r},{cy-r*0.35} {cx+r},{cy+r*0.15} A{r},{r} 0 0 1 {cx-r},{cy+r*0.15} C{cx-r},{cy-r*0.35} {cx-r*0.35},{cy-r*0.85} {cx},{cy-r*1.45} Z"
    s = f'<path d="{d}" fill="{farba}"/>'
    if vnutro:
        s += (f'<svg x="{cx-r*0.78}" y="{cy-r*0.62}" width="{r*1.56}" height="{r*1.02}" viewBox="6 6 139 91">'
              f'<circle cx="118" cy="27" r="19" fill="{ZLTA}"/>'
              f'<path d="M9 93 63 29 83 53 51 93Z M56 93 83 61 108 93Z M85 58 99 42 142 94 108 93Z" fill="{vnutro}"/></svg>')
        s += f'<path d="M{cx-r*0.8},{cy+r*0.48} Q{cx-r*0.4},{cy+r*0.38} {cx},{cy+r*0.48} T{cx+r*0.8},{cy+r*0.48}" fill="none" stroke="{TYRKYS}" stroke-width="{r*0.12}" stroke-linecap="round"/>'
    return s


def polovica_plesa(prava):
    def X(x): return POL - x if prava else x
    p = [kvapka(X(17), SIRKA/2 + 1.6, 6.6, KREM, MODRA),
         vlnky_pas(X(38)),
         logo(X(63), SIRKA/2),
         vlnky_pas(X(88))]
    tx = X(172)
    p.append(text(tx, 11.0, "TATRANSKÉ", 8.4, KREM, "Liberation Sans", sirka_pism=0.9))
    p.append(text(tx, 21.0, "PLESÁ", 8.4, ZLTA, "Liberation Sans", sirka_pism=2.4))
    p += [vlnky_pas(X(256))]
    for i, x in enumerate((276, 286, 296, 306, 316)):
        p.append(kvapka(X(x), SIRKA/2 + 0.8, 2.4, TYRKYS if i != 2 else ZLTA))
    p += [vlnky_pas(X(336)),
          text(X(392), 15.6, "VYSLAPSIMEDAILU.SK", 5.2, KREM, "Liberation Sans", sirka_pism=0.5),
          vlnky_pas(X(444), 8)]
    return "".join(p)


BORDO, ZLATA, ZELEN_H = "#7a1628", "#d9b45a", "#2f6a3c"


def hrad(cx, zem, v, farba=KREM, vlajka=ZLTA):
    """Silueta hradu: stredná veža + dve bočné veže a hradby, v = výška v mm."""
    w = v * 1.5
    t = []
    def veza(x, sirka, vyska, strecha=False):
        y = zem - vyska
        d = f"M{x-sirka/2},{zem} L{x-sirka/2},{y}"
        z = sirka / 5
        for k in range(5):
            d += f" l{z/2},0 l0,{-z*0.6 if k % 2 == 0 else z*0.6} l{z/2},0"
        d += f" L{x+sirka/2},{zem} Z"
        r = f'<path d="{d}" fill="{farba}"/>'
        if strecha:
            r += f'<polygon points="{x-sirka*0.6},{y} {x+sirka*0.6},{y} {x},{y-sirka*1.1}" fill="{BORDO}" stroke="{farba}" stroke-width="{v*0.03}"/>'
            r += f'<line x1="{x}" y1="{y-sirka*1.1}" x2="{x}" y2="{y-sirka*1.6}" stroke="{farba}" stroke-width="{v*0.04}"/>'
            r += f'<polygon points="{x},{y-sirka*1.6} {x+sirka*0.6},{y-sirka*1.45} {x},{y-sirka*1.3}" fill="{vlajka}"/>'
        return r
    t.append(f'<rect x="{cx-w/2}" y="{zem-v*0.45}" width="{w}" height="{v*0.45}" fill="{farba}"/>')
    t.append(veza(cx - w*0.42, v*0.28, v*0.62))
    t.append(veza(cx + w*0.42, v*0.28, v*0.62))
    t.append(veza(cx, v*0.36, v*0.82, strecha=True))
    t.append(f'<path d="M{cx-v*0.08},{zem} l0,{-v*0.18} a{v*0.08},{v*0.08} 0 0 1 {v*0.16},0 l0,{v*0.18} Z" fill="{BORDO}"/>')
    return "".join(t)


def ornament(cx, cy, r, farba=ZLATA):
    return (f'<path d="M{cx},{cy-r} L{cx+r},{cy} L{cx},{cy+r} L{cx-r},{cy} Z" fill="none" stroke="{farba}" stroke-width="0.5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.3}" fill="{farba}"/>')


def polovica_hrady(prava):
    def X(x): return POL - x if prava else x
    hx = X(24)
    p = [  # vinetka: kopec, cesta, hrad a slnko
        f'<path d="M{hx-17},{SIRKA-2.2} Q{hx-6},{SIRKA-12} {hx+3},{SIRKA-9} Q{hx+11},{SIRKA-7} {hx+17},{SIRKA-2.2} Z" fill="{ZELEN_H}"/>',
        f'<path d="M{hx-2},{SIRKA-2.2} Q{hx+4},{SIRKA-5} {hx-1},{SIRKA-7.5}" fill="none" stroke="{ZLATA}" stroke-width="0.9" stroke-linecap="round"/>',
        f'<circle cx="{hx+9}" cy="7.4" r="3.2" fill="{ZLTA}"/>',
        hrad(hx - 1, SIRKA - 9.6, 9),
        logo(X(60), SIRKA / 2, w=25, h=17),
        ornament(X(86), SIRKA / 2, 2.6),
        text(X(160), 11.4, "HRADNÁ", 8.4, KREM, "DejaVu Serif", sirka_pism=1.0),
        text(X(160), 21.2, "VÝZVA", 8.4, ZLATA, "DejaVu Serif", sirka_pism=2.2),
        ornament(X(228), SIRKA / 2, 2.6),
        text(X(260), 15.4, "8 HRADOV", 5.6, ZLTA, "DejaVu Serif", sirka_pism=0.6),
    ]
    for k in range(8):
        p.append(hrad(X(300 + k * 10), 17.2, 5.8, KREM if k % 2 == 0 else ZLATA))
    p.append(f'<rect x="{min(X(295), X(375))}" y="17.6" width="80" height="0.5" fill="{ZLATA}"/>')
    p.append(text(X(415), 15.2, "VYSLAPSIMEDAILU.SK", 3.9, ZLATA, "DejaVu Serif", sirka_pism=0.2))
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


STUHY = {
    "novorocnych-100": ("Stuha – Novoročných 100", "Návrh stuhy · 25 × 900 mm · tmavozelená so zimným vzorom",
                        "#0b4a30", polovica_novorocnych,
                        [("Zelená stuha", "#0b4a30"), ("Žltá", ZLTA), ("Krémová", KREM), ("Logo hory", TMZEL)], None, "1 ks na medailu"),
    "valentinska-dvojica": ("Stuha – Valentínska dvojica", "Návrh stuhy · 25 × 900 mm · bordová so srdiečkami",
                            "#8a1a2b", polovica_valentinska,
                            [("Bordová stuha", "#8a1a2b"), ("Krémová", KREM), ("Žltá", ZLTA), ("Logo hory", TMZEL)], KREM,
                            "2 ks na pár (každá polovica medaily má svoju)"),
    "hradna-vyzva-2027": ("Stuha – Hradná výzva", "Návrh stuhy · 25 × 900 mm · bordová so zlatými linkami a hradmi",
                          BORDO, polovica_hrady,
                          [("Bordová stuha", BORDO), ("Zlatá", ZLATA), ("Krémová", KREM), ("Zelená kopec", ZELEN_H)], ZLATA, "1 ks na medailu"),
    "tatranske-plesa-2027": ("Stuha – Tatranské plesá", "Návrh stuhy · 25 × 900 mm · plesová modrá s vlnkami hladiny",
                             MODRA, polovica_plesa,
                             [("Modrá stuha", MODRA), ("Tyrkysová", TYRKYS), ("Žltá", ZLTA), ("Krémová", KREM)], ZLTA, "1 ks na medailu"),
}

if __name__ == "__main__":
    out = sys.argv[1]
    vyber = sys.argv[2:] or list(STUHY)
    for meno in vyber:
        nazov, podnazov, farba, pol, farby, okraje, ks = STUHY[meno]
        svg, s = harok(nazov, podnazov, farba, pol, farby, okraje=okraje, ks=ks)
        uloz(svg, f"{out}/stuha-{meno}.png")
        cela = f'<svg xmlns="http://www.w3.org/2000/svg" width="9000" height="250" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>'
        uloz(cela, f"{out}/stuha-{meno}-tlac.png")
        open(f"{out}/stuha-{meno}-tlac.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{DLZKA}mm" height="{SIRKA}mm" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>')
