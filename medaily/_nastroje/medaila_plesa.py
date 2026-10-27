"""Vizualizácia medaily Tatranské plesá 2027 – kvapka, staré striebro, pleso v smalte."""
import math, sys, random
import cairosvg

W, H = 1200, 1480
KREM, ZLTA, TMZEL, MODRA, TYRKYS = "#f6f3e9", "#ffca1b", "#063f2d", "#0f4a6e", "#46b9c8"
LOGO = ('<circle cx="118" cy="27" r="19" fill="{s}"/>'
        '<path d="M9 93 63 29 83 53 51 93Z M56 93 83 61 108 93Z M85 58 99 42 142 94 108 93Z" fill="{h}"/>')

cx, cy, r = 600, 1050, 330          # stred spodného polkruhu kvapky


def kvapka(r_, dx=0, dy=0):
    x, y = cx + dx, cy + dy
    return (f"M{x},{y-1.62*r_} C{x+0.38*r_},{y-1.08*r_} {x+r_},{y-0.62*r_} {x+r_},{y} "
            f"A{r_},{r_} 0 0 1 {x-r_},{y} C{x-r_},{y-0.62*r_} {x-0.38*r_},{y-1.08*r_} {x},{y-1.62*r_} Z")


def logo(x, y, w, slnko=ZLTA, hory=TMZEL):
    h = w * 91 / 139
    return f'<svg x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" viewBox="6 6 139 91">{LOGO.format(s=slnko, h=hory)}</svg>'


def stuha_pas(x1, y1, x2, y2, sirka, zrkadlo):
    """Jeden pás stuhy z (x1,y1) hore do (x2,y2) pri medaile."""
    dl = math.hypot(x2 - x1, y2 - y1)
    uhol = math.degrees(math.atan2(y2 - y1, x2 - x1))
    g = [f'<g transform="translate({x1},{y1}) rotate({uhol})">',
         f'<rect x="0" y="{-sirka/2}" width="{dl}" height="{sirka}" fill="{MODRA}"/>',
         f'<rect x="0" y="{-sirka/2+7}" width="{dl}" height="3" fill="{ZLTA}"/>',
         f'<rect x="0" y="{sirka/2-10}" width="{dl}" height="3" fill="{ZLTA}"/>']
    # vlnky
    def vlnky(px):
        s = ""
        for k, dx in enumerate((-12, 0, 12)):
            d = f"M{px+dx},{-sirka/2+12}"
            n = 8
            for i in range(n):
                yy = -sirka/2 + 12 + (i + 1) * (sirka - 24) / n
                d += f" Q{px+dx+(6 if i % 2 == 0 else -6)},{yy-(sirka-24)/n/2} {px+dx},{yy}"
            s += f'<path d="{d}" fill="none" stroke="{KREM if k == 1 else TYRKYS}" stroke-width="3" stroke-linecap="round"/>'
        return s
    # text – číta sa smerom k medaile
    tx = dl * 0.33
    g.append(f'<text x="{tx}" y="{-2}" font-family="Liberation Sans" font-weight="bold" font-size="30" fill="{KREM}" '
             f'text-anchor="middle" letter-spacing="3">TATRANSKÉ</text>')
    g.append(f'<text x="{tx}" y="{30}" font-family="Liberation Sans" font-weight="bold" font-size="30" fill="{ZLTA}" '
             f'text-anchor="middle" letter-spacing="9">PLESÁ</text>')
    g.append(vlnky(dl * 0.52))
    # štítok s logom
    lx = dl * 0.70
    g.append(f'<g transform="translate({lx},0) rotate({-uhol})">'
             f'<rect x="-62" y="-44" width="124" height="88" rx="3" fill="{KREM}"/>{logo(0, 0, 92)}</g>')
    g.append(vlnky(dl * 0.88))
    # tieň tkaniny
    g.append(f'<rect x="0" y="{-sirka/2}" width="{dl}" height="{sirka}" fill="url(#tienStuhy)"/>')
    g.append('</g>')
    return "".join(g)


def hory(zaklad, farby, odraz=False):
    """Hrebeň štítov – zoznam bodov (x, výška nad základňou)."""
    body = [(150, 0), (215, 120), (265, 85), (330, 230), (372, 175), (420, 300), (470, 210), (520, 255),
            (585, 150), (640, 215), (700, 120), (760, 175), (830, 70), (900, 110), (1050, 0)]
    znam = -1 if odraz else 1
    pts = " ".join(f"{x},{zaklad - znam*h}" for x, h in body)
    s = f'<polygon points="{pts}" fill="{farby[0]}"/>'
    # tieňované svahy (pravé strany štítov)
    for i in range(1, len(body) - 1):
        x0, h0 = body[i]
        x1, h1 = body[i + 1]
        if h1 < h0:
            p = f"{x0},{zaklad-znam*h0} {x1},{zaklad-znam*h1} {x0 + (x1-x0)*0.45},{zaklad - znam*h1*0.2}"
            s += f'<polygon points="{p}" fill="{farby[1]}"/>'
    if not odraz:
        # sneh na najvyšších štítoch
        for x, h in body:
            if h >= 200:
                sn = f"{x},{zaklad-h} {x+22},{zaklad-h+38} {x+10},{zaklad-h+32} {x},{zaklad-h+48} {x-10},{zaklad-h+30} {x-24},{zaklad-h+40}"
                s += f'<polygon points="{sn}" fill="#f4f4ef"/>'
        # skalné ryhy
        random.seed(3)
        for x, h in body:
            if h > 120:
                for k in range(3):
                    ox = random.uniform(-30, 30)
                    s += (f'<path d="M{x+ox*0.3},{zaklad-h+60+k*30} l{ox*0.6},{40+k*10}" stroke="#8d939a" '
                          f'stroke-width="2" opacity="0.6" fill="none"/>')
    return s


def smrek(x, y, v, farba):
    s = ""
    for k in range(4):
        w = v * (0.18 + k * 0.08)
        yt = y - v + k * v * 0.22
        s += f'<polygon points="{x},{yt} {x+w},{yt+v*0.32} {x-w},{yt+v*0.32}" fill="{farba}"/>'
    s += f'<rect x="{x-v*0.03}" y="{y-v*0.06}" width="{v*0.06}" height="{v*0.1}" fill="{farba}"/>'
    return s


def medaila():
    zaklad = 1010                       # línia brehu / hladiny
    ri = r - 34                         # vnútorný okraj
    sc = []
    # nebo – svetlé staré striebro
    sc.append(f'<rect x="0" y="0" width="{W}" height="{zaklad}" fill="url(#nebo)"/>')
    # slnko + lúče
    sx, sy = 640, 715
    for i in range(14):
        a = math.radians(-180 + i * 180 / 13)
        sc.append(f'<line x1="{sx+70*math.cos(a)}" y1="{sy+70*math.sin(a)}" x2="{sx+125*math.cos(a)}" '
                  f'y2="{sy+125*math.sin(a)}" stroke="#e9b10f" stroke-width="7" stroke-linecap="round" opacity="0.85"/>')
    sc.append(f'<circle cx="{sx}" cy="{sy}" r="62" fill="url(#slnko)"/>')
    # hory a ich odraz
    sc.append(hory(zaklad, ("url(#skala)", "#7c838b")))
    sc.append(f'<rect x="0" y="{zaklad}" width="{W}" height="{H}" fill="url(#voda)"/>')
    sc.append(f'<g opacity="0.22">{hory(zaklad, ("#d8e8ea", "#9fc9cf"), odraz=True)}</g>')
    sc.append(f'<ellipse cx="{sx}" cy="{zaklad+40}" rx="46" ry="9" fill="{ZLTA}" opacity="0.45"/>')
    # vlnky na hladine
    for i, (x, y, w) in enumerate([(420, 1050, 90), (640, 1075, 120), (520, 1105, 70), (760, 1110, 80)]):
        sc.append(f'<path d="M{x-w/2},{y} q{w/4},-7 {w/2},0 t{w/2},0" fill="none" stroke="#e8f7f8" stroke-width="3" opacity="0.7"/>')
    # breh s kosodrevinou a smrekmi
    sc.append(f'<path d="M200,{zaklad+4} Q300,{zaklad-22} 380,{zaklad+2} L380,{zaklad+12} L200,{zaklad+12} Z" fill="#2c5a3a"/>')
    sc.append(f'<path d="M800,{zaklad+4} Q900,{zaklad-26} 1000,{zaklad+2} L1000,{zaklad+12} L800,{zaklad+12} Z" fill="#2c5a3a"/>')
    for x, v in [(250, 120), (290, 160), (330, 110), (850, 150), (895, 190), (940, 125)]:
        sc.append(smrek(x, zaklad + 4, v, "#1d4a2e"))
    scena = "".join(sc)

    by = 1110
    m = [
        # tieň medaily
        f'<path d="{kvapka(r, 14, 22)}" fill="#000" opacity="0.13"/>',
        # očko a krúžok
        f'<rect x="{cx-58}" y="{cy-1.62*r-62}" width="116" height="80" rx="26" fill="none" stroke="url(#strieborna)" stroke-width="20"/>',
        # okraj
        f'<path d="{kvapka(r)}" fill="url(#strieborna)"/>',
        f'<path d="{kvapka(r-14)}" fill="url(#strieborna2)"/>',
        f'<path d="{kvapka(ri+6)}" fill="#5d636b"/>',
        f'<g clip-path="url(#vnutro)">{scena}</g>',
        f'<path d="{kvapka(ri)}" fill="none" stroke="#3d4248" stroke-width="3" opacity="0.6"/>',
        # odlesk okraja
        f'<path d="{kvapka(r-6)}" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.35" stroke-dasharray="380 2600" stroke-dashoffset="-160"/>',
        # banner
        f'<path d="M{cx-300},{by} L{cx+300},{by} L{cx+280},{by+44} L{cx+300},{by+88} L{cx-300},{by+88} L{cx-280},{by+44} Z" fill="#6b7279"/>',
        f'<rect x="{cx-265}" y="{by-8}" width="530" height="104" rx="6" fill="url(#strieborna)" stroke="#5b6168" stroke-width="3"/>',
        f'<text x="{cx}" y="{by+64}" font-family="Liberation Sans" font-weight="bold" font-size="41" fill="#2e3338" '
        f'text-anchor="middle" letter-spacing="3">TATRANSKÉ PLESÁ</text>',
        f'<rect x="{cx-78}" y="{by+112}" width="156" height="52" rx="26" fill="{ZLTA}" stroke="#b98a07" stroke-width="3"/>',
        f'<text x="{cx}" y="{by+151}" font-family="Liberation Sans" font-weight="bold" font-size="38" fill="{TMZEL}" '
        f'text-anchor="middle" letter-spacing="5">2027</text>',
        # logo dole
        f'<rect x="{cx-46}" y="{by+176}" width="92" height="58" rx="8" fill="#eef0f2" stroke="#7d848c" stroke-width="2"/>',
        logo(cx, by + 205, 70),
    ]
    return "".join(m)


def defs():
    return f'''<defs>
<clipPath id="vnutro"><path d="{kvapka(r-34)}"/></clipPath>
<linearGradient id="strieborna" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#f2f4f6"/><stop offset="0.3" stop-color="#b9bfc5"/><stop offset="0.55" stop-color="#e3e7ea"/>
  <stop offset="0.8" stop-color="#8e959c"/><stop offset="1" stop-color="#c9ced3"/></linearGradient>
<linearGradient id="strieborna2" x1="1" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#d9dde1"/><stop offset="0.5" stop-color="#9aa1a8"/><stop offset="1" stop-color="#e5e8eb"/></linearGradient>
<linearGradient id="nebo" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#c3c8cd"/><stop offset="1" stop-color="#eef0f1"/></linearGradient>
<linearGradient id="skala" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#c5cad0"/><stop offset="1" stop-color="#8f969d"/></linearGradient>
<linearGradient id="voda" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#5cc6d2"/><stop offset="0.5" stop-color="#2b9fb3"/><stop offset="1" stop-color="#16708a"/></linearGradient>
<radialGradient id="slnko" cx="0.4" cy="0.35" r="0.7">
  <stop offset="0" stop-color="#ffe27a"/><stop offset="0.6" stop-color="{ZLTA}"/><stop offset="1" stop-color="#e3a80c"/></radialGradient>
<linearGradient id="tienStuhy" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#000" stop-opacity="0.22"/><stop offset="0.15" stop-color="#000" stop-opacity="0"/>
  <stop offset="0.85" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.25"/></linearGradient>
<radialGradient id="pozadie" cx="0.5" cy="0.45" r="0.75">
  <stop offset="0" stop-color="#fbf8f0"/><stop offset="1" stop-color="#ebe4d3"/></radialGradient>
</defs>'''


def svg():
    top = cy - 1.62 * r - 40
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         defs(), f'<rect width="{W}" height="{H}" fill="url(#pozadie)"/>',
         # tiene stúh
         f'<g opacity="0.10">{stuha_pas(250, -60, cx-48+14, top+20, 150, False)}{stuha_pas(950, -60, cx+48+14, top+20, 150, True)}</g>',
         stuha_pas(230, -80, cx - 48, top, 150, False),
         stuha_pas(970, -80, cx + 48, top, 150, True),
         medaila(), '</svg>']
    return "".join(s).replace('href="#obluk"', 'xlink:href="#obluk"')


if __name__ == "__main__":
    out = sys.argv[1]
    t = svg()
    open(f"{out}/medaila-tatranske-plesa.svg", "w").write(t)
    cairosvg.svg2png(bytestring=t.encode(), write_to=f"{out}/medaila-tatranske-plesa.png")
