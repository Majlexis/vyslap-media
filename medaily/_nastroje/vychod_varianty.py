"""Východ slnka na vrchole – 5 návrhov stuhy (polovica od medaily po krk)."""
import math, random, sys
sys.path.insert(0, sys.path[0])
from stuhy import logo, text, uloz, KREM, ZLTA, TMZEL, SIRKA, POL

F = "Liberation Sans"
ZEL = "#0d4a35"
ORANZ = "#f26b2a"
NOC = "#14284a"


def logo_bez(x, y, w=24):
    h = w * 91 / 139
    return (f'<svg x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" viewBox="6 6 139 91">'
            f'<circle cx="118" cy="27" r="19" fill="{ZLTA}"/><path d="M9 93 63 29 83 53 51 93Z M56 93 83 61 108 93Z M85 58 99 42 142 94 108 93Z" fill="{TMZEL}"/></svg>')


def nazov(x, farba, velk=7.0):
    return (text(x, 12.0, "VÝCHOD SLNKA", velk, farba, F, sirka_pism=0.6) +
            text(x, 20.6, "NA VRCHOLE", velk, farba, F, sirka_pism=1.2))


def hory(x0, x1, zaklad, amp, farba, seed, krok=7, op=1):
    random.seed(seed)
    pts = [f"{x0},{SIRKA}"]
    x = x0
    while x <= x1 + krok:
        pts.append(f"{x:.1f},{zaklad - random.uniform(0.2, 1) * amp:.1f}")
        x += random.uniform(krok * 0.6, krok * 1.3)
    pts.append(f"{x1+krok},{SIRKA}")
    return f'<polygon points="{" ".join(pts)}" fill="{farba}" opacity="{op}"/>'


def slnko_pruhy(cx, cy, r, pruh="#f26b2a", pozadie=None):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{ZLTA}"/>'
    s += f'<path d="M{cx-r},{cy} A{r},{r} 0 0 0 {cx+r},{cy} Z" fill="#f9a13a"/>'
    if pozadie:
        for k, dy in enumerate((0.15, 0.4, 0.62, 0.8)):
            s += f'<rect x="{cx-r}" y="{cy+r*dy}" width="{2*r}" height="{r*(0.07+k*0.025)}" fill="{pozadie}"/>'
    return s


# 1 – Úsvit: farba stuhy prechádza od nočnej modrej pri krku po oranžovú pri medaile
def v1():
    random.seed(5)
    hv = []
    while len(hv) < 34:
        x, y = random.uniform(290, 447), random.uniform(2, 23)
        if x > 375 and 9.5 < y < 18.5:
            continue
        hv.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(0.25, 0.55):.2f}" fill="{KREM}" opacity="0.8"/>')
    hviezdy = "".join(hv)
    return "".join([
        '<defs><linearGradient id="g1" x1="0" y1="0" x2="450" y2="0" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{ZLTA}"/><stop offset="0.22" stop-color="#f9a13a"/><stop offset="0.45" stop-color="{ORANZ}"/>'
        f'<stop offset="0.68" stop-color="#8a3a5c"/><stop offset="1" stop-color="{NOC}"/></linearGradient></defs>',
        f'<rect width="{POL}" height="{SIRKA}" fill="url(#g1)"/>', hviezdy,
        slnko_pruhy(26, SIRKA/2, 8.5, pozadie="#fbd34a"),
        f'<rect x="50" y="{SIRKA/2-8.5}" width="28" height="17" rx="0.6" fill="{KREM}"/>', logo_bez(64, SIRKA/2, 22),
        nazov(175, ZEL, 7.4),
        text(300, 15.2, "· · ·", 6, KREM, F),
        text(410, 15.2, "VYSLAPSIMEDAILU.SK", 4.4, KREM, F, sirka_pism=0.4),
    ])


# 2 – Retro pruhy: tmavozelená, po celej dĺžke tri pruhy farieb východu slnka
def v2():
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="{ZEL}"/>',
        f'<rect y="1.6" width="{POL}" height="1.5" fill="{ZLTA}"/>', f'<rect y="3.6" width="{POL}" height="1.5" fill="#f9a13a"/>',
        f'<rect y="5.6" width="{POL}" height="1.5" fill="{ORANZ}"/>',
        f'<rect y="{SIRKA-3.1}" width="{POL}" height="1.5" fill="{ZLTA}"/>', f'<rect y="{SIRKA-5.1}" width="{POL}" height="1.5" fill="#f9a13a"/>',
        f'<rect y="{SIRKA-7.1}" width="{POL}" height="1.5" fill="{ORANZ}"/>',
        f'<rect x="10" y="0" width="34" height="{SIRKA}" fill="{ZEL}"/>', slnko_pruhy(27, SIRKA/2, 8, pozadie=ZEL),
        f'<rect x="56" y="{SIRKA/2-8.5}" width="28" height="17" rx="0.6" fill="{KREM}"/>', logo_bez(70, SIRKA/2, 22),
        f'<rect x="110" y="0" width="140" height="{SIRKA}" fill="{ZEL}"/>', nazov(180, KREM, 7.2),
        f'<rect x="270" y="0" width="34" height="{SIRKA}" fill="{ZEL}"/>', slnko_pruhy(287, SIRKA/2, 7, pozadie=ZEL),
        f'<rect x="355" y="0" width="92" height="{SIRKA}" fill="{ZEL}"/>',
        text(401, 15.2, "VYSLAPSIMEDAILU.SK", 4.4, ZLTA, F, sirka_pism=0.4),
    ])


# 3 – Pásma hôr: tyrkysová, po celej dĺžke vrstvy hôr a lúče slnka
def v3():
    luce = ""
    for cx in (26, 290):
        for k in range(9):
            a = math.radians(-180 + k * 22.5)
            luce += f'<line x1="{cx+9*math.cos(a):.1f}" y1="{14+9*math.sin(a):.1f}" x2="{cx+40*math.cos(a):.1f}" y2="{14+40*math.sin(a):.1f}" stroke="{ZLTA}" stroke-width="1.1" opacity="0.35"/>'
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="#1b6b78"/>', luce,
        f'<circle cx="26" cy="14" r="7" fill="{ZLTA}"/>', f'<circle cx="290" cy="14" r="5.5" fill="{ZLTA}"/>',
        hory(0, POL, 19, 4, "#3f9e9b", 31), hory(0, POL, 21.5, 3, "#16465f", 32, 6), hory(0, POL, 23.5, 2, ZEL, 33, 5),
        f'<rect x="52" y="3" width="28" height="13" rx="0.6" fill="{KREM}"/>', logo_bez(66, 9.5, 18),
        text(175, 10.5, "VÝCHOD SLNKA NA VRCHOLE", 6.4, KREM, F, sirka_pism=0.6),
        text(395, 10.4, "VYSLAPSIMEDAILU.SK", 4.2, KREM, F, sirka_pism=0.4),
    ])


# 4 – Lúče: oranžovo-žltá, za nápisom veľký slnečný vejár
def v4():
    luce = ""
    for cx, cy in ((175, 34), (380, 34)):
        for k in range(24):
            a = math.radians(-180 + k * 7.5)
            if k % 2 == 0:
                a2 = math.radians(-180 + (k + 1) * 7.5)
                luce += f'<polygon points="{cx},{cy} {cx+140*math.cos(a):.1f},{cy+140*math.sin(a):.1f} {cx+140*math.cos(a2):.1f},{cy+140*math.sin(a2):.1f}" fill="{ZLTA}" opacity="0.55"/>'
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="#f9a13a"/>', luce,
        f'<rect y="0" width="{POL}" height="1.6" fill="{ZEL}"/>', f'<rect y="{SIRKA-1.6}" width="{POL}" height="1.6" fill="{ZEL}"/>',
        f'<rect x="8" y="{SIRKA/2-8.5}" width="38" height="17" rx="0.6" fill="{ZEL}"/>', slnko_pruhy(27, SIRKA/2, 6.5, pozadie=ZEL),
        f'<rect x="56" y="{SIRKA/2-8.5}" width="28" height="17" rx="0.6" fill="{KREM}"/>', logo_bez(70, SIRKA/2, 22),
        nazov(175, ZEL, 7.4),
        text(300, 15.2, "VLASTNÝM TEMPOM", 4.6, ZEL, F, sirka_pism=0.6),
        text(410, 15.2, "VYSLAPSIMEDAILU.SK", 4.4, ZEL, F, sirka_pism=0.4),
    ])


# 5 – Krémová minimal: krémová, tenký pás východu slnka v strede a ikonky
def v5():
    ikona = lambda x: (f'<circle cx="{x}" cy="{SIRKA/2-0.5}" r="3.4" fill="{ORANZ}"/>'
                       f'<polygon points="{x-6},{SIRKA/2+4} {x-1},{SIRKA/2-2.5} {x+1.5},{SIRKA/2+0.5} {x+3},{SIRKA/2-1} {x+6},{SIRKA/2+4}" fill="{ZEL}"/>')
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="{KREM}"/>',
        '<defs><linearGradient id="g5" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f26b2a"/><stop offset="1" stop-color="#ffd45e"/></linearGradient></defs>',
        f'<rect y="1.2" width="{POL}" height="1.2" fill="url(#g5)"/>', f'<rect y="{SIRKA-2.4}" width="{POL}" height="1.2" fill="url(#g5)"/>',
        ikona(24), logo_bez(62, SIRKA/2, 24),
        nazov(170, ZEL, 7.4),
        ikona(262), ikona(300), ikona(338),
        text(410, 15.2, "VYSLAPSIMEDAILU.SK", 4.4, ORANZ, F, sirka_pism=0.4),
    ])


VARIANTY = [("1 · Úsvit", "Farba prechádza od nočnej modrej s hviezdami pri krku po zlaté slnko pri medaile.", v1),
            ("2 · Retro pruhy", "Tmavozelená s pruhmi žltá–oranžová po okrajoch a pruhovanými slnkami.", v2),
            ("3 · Pásma hôr", "Tyrkysová, po celej dĺžke vrstvy hôr a lúče vychádzajúceho slnka.", v3),
            ("4 · Lúče", "Oranžovo-žltá so slnečným vejárom, tmavozelené okraje a nápisy.", v4),
            ("5 · Krémová minimal", "Krémová, tenké pásy farieb úsvitu a ikonky slnka nad vrcholom.", v5)]


def harok():
    W, m = 2400, 80
    sk = (W - 2 * m) / POL
    hp = SIRKA * sk
    gap = 110
    y = 220
    H = y + 5 * (hp + gap) + 40
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}">',
         f'<rect width="{W}" height="{H}" fill="#fbfaf6"/>',
         text(m, 105, "Východ slnka na vrchole – 5 návrhov stuhy", 52, "#1c2a20", F, kotva="start", sirka_pism=0),
         f'<text x="{m}" y="160" font-family="{F}" font-size="26" fill="#6b776f">Polovica stuhy od medaily (vľavo) po krk (vpravo) · 25 × 900 mm · druhá polovica je zrkadlová</text>']
    for i, (n, popis, fn) in enumerate(VARIANTY):
        yy = y + i * (hp + gap)
        s.append(f'<text x="{m}" y="{yy+18}" font-family="{F}" font-weight="bold" font-size="28" fill="#1c2a20">{n}'
                 f'<tspan font-weight="normal" fill="#5b6a60" font-size="24">   {popis}</tspan></text>')
        tien = (f'<defs><linearGradient id="t{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.18"/>'
                f'<stop offset="0.15" stop-color="#000" stop-opacity="0"/><stop offset="0.85" stop-color="#000" stop-opacity="0"/>'
                f'<stop offset="1" stop-color="#000" stop-opacity="0.2"/></linearGradient>'
                f'<clipPath id="c{i}"><rect width="{POL}" height="{SIRKA}"/></clipPath></defs>')
        s.append(f'<svg x="{m}" y="{yy+34}" width="{W-2*m}" height="{hp}" viewBox="0 0 {POL} {SIRKA}">{tien}'
                 f'<g clip-path="url(#c{i})">{fn()}</g><rect width="{POL}" height="{SIRKA}" fill="url(#t{i})"/></svg>')
    s.append("</svg>")
    return "".join(s)


def polovica_retro(prava):
    """Variant 2 – Retro pruhy, polovica stuhy so zrkadlením pozícií (text ostáva rovno)."""
    def X(x): return POL - x if prava else x
    def blok(a, b): return f'<rect x="{min(X(a), X(b))}" y="0" width="{abs(b-a)}" height="{SIRKA}" fill="{ZEL}"/>'
    p = [f'<rect y="1.6" width="{POL}" height="1.5" fill="{ZLTA}"/>', f'<rect y="3.6" width="{POL}" height="1.5" fill="#f9a13a"/>',
         f'<rect y="5.6" width="{POL}" height="1.5" fill="{ORANZ}"/>',
         f'<rect y="{SIRKA-3.1}" width="{POL}" height="1.5" fill="{ZLTA}"/>', f'<rect y="{SIRKA-5.1}" width="{POL}" height="1.5" fill="#f9a13a"/>',
         f'<rect y="{SIRKA-7.1}" width="{POL}" height="1.5" fill="{ORANZ}"/>',
         blok(10, 44), slnko_pruhy(X(27), SIRKA/2, 8, pozadie=ZEL),
         f'<rect x="{X(70)-14}" y="{SIRKA/2-8.5}" width="28" height="17" rx="0.6" fill="{KREM}"/>', logo_bez(X(70), SIRKA/2, 22),
         blok(110, 250), text(X(180), 12.0, "VÝCHOD SLNKA", 7.2, KREM, F, sirka_pism=0.6),
         text(X(180), 20.6, "NA VRCHOLE", 7.2, KREM, F, sirka_pism=1.2),
         blok(270, 304), slnko_pruhy(X(287), SIRKA/2, 7, pozadie=ZEL),
         blok(355, 447), text(X(401), 15.2, "VYSLAPSIMEDAILU.SK", 4.4, ZLTA, F, sirka_pism=0.4)]
    return "".join(p)


def finalna(out):
    import stuhy as st
    svg, s = st.harok("Stuha – Východ slnka na vrchole", "Návrh stuhy · 25 × 900 mm · tmavozelená s retro pruhmi úsvitu",
                      ZEL, polovica_retro,
                      [("Zelená stuha", ZEL), ("Žltá", ZLTA), ("Svetlooranžová", "#f9a13a"), ("Oranžová", ORANZ)], ks="1 ks na medailu")
    uloz(svg, f"{out}/stuha-vychod-slnka-2027.png")
    from stuhy import DLZKA
    uloz(f'<svg xmlns="http://www.w3.org/2000/svg" width="9000" height="250" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>', f"{out}/stuha-vychod-slnka-2027-tlac.png")
    open(f"{out}/stuha-vychod-slnka-2027-tlac.svg", "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{DLZKA}mm" height="{SIRKA}mm" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>')


if __name__ == "__main__":
    if sys.argv[2:] == ["finalna"]:
        finalna(sys.argv[1])
    else:
        uloz(harok(), f"{sys.argv[1]}/vychod-slnka-5-navrhov.png")
