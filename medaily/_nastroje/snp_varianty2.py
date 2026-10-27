"""Cesta SNP – ďalších 5 návrhov stuhy."""
import math, random, sys
sys.path.insert(0, sys.path[0])
from stuhy import logo, text, uloz, KREM, ZLTA, TMZEL, SIRKA, POL, DLZKA
from snp_varianty import znacka, ZEL, CERV, BIELA, KM, F
import snp_varianty as sv


def profil_body(x0, x1, seed):
    random.seed(seed)
    n = int((x1 - x0) / 2.5)
    pts, y = [], 19
    for k in range(n + 1):
        x = x0 + k * (x1 - x0) / n
        # vyššie hory v strede (Nízke Tatry), nižšie na koncoch
        t = (x - x0) / (x1 - x0)
        base = 21 - 10 * math.exp(-((t - 0.45) / 0.18) ** 2) - 4 * math.exp(-((t - 0.8) / 0.1) ** 2)
        y = base + random.uniform(-1.6, 1.6)
        pts.append((x, max(4, min(22, y))))
    return pts


# 4 – Výškový profil: krémová, po dĺžke výškový profil trasy
def v4(prava=False):
    def X(x): return POL - x if prava else x
    a, b = sorted((X(150), X(445)))
    pts = profil_body(a, b, 3)
    if prava:
        pts = [(a + b - x, y) for x, y in pts]
        pts.sort()
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    vrch = min(pts, key=lambda p: p[1])
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="{KREM}"/>',
        f'<rect y="0" width="{POL}" height="1.5" fill="{ZEL}"/>', f'<rect y="{SIRKA-1.5}" width="{POL}" height="1.5" fill="{ZEL}"/>',
        f'<polygon points="{a},{SIRKA-1.5} {poly} {b},{SIRKA-1.5}" fill="#2f6a3c" opacity="0.85"/>',
        f'<polyline points="{poly}" fill="none" stroke="{CERV}" stroke-width="0.7"/>',
        f'<circle cx="{vrch[0]:.1f}" cy="{vrch[1]:.1f}" r="1" fill="{ZLTA}" stroke="{ZEL}" stroke-width="0.3"/>',
        text(vrch[0] + (12 if not prava else -12), max(4.2, vrch[1] - 0.2), "Ďumbier 2043 m", 3.2, ZEL, F, sirka_pism=0.2),
        logo(X(22), SIRKA/2, w=27, h=17),
        text(X(90), 12.2, "CESTA SNP", 7.6, ZEL, F, sirka_pism=1.0),
        text(X(90), 21.0, KM, 7.6, CERV, F, sirka_pism=1.0),
    ])


# 5 – Míľniky: tmavozelená ako pravítko, kilometrovník po celej dĺžke
def v5(prava=False):
    def X(x): return POL - x if prava else x
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="{ZEL}"/>']
    zac, kon = 150, 440
    for k in range(0, 78):
        x = zac + (kon - zac) * k / 77
        dl = 4.5 if k % 10 == 0 else (2.8 if k % 5 == 0 else 1.6)
        s.append(f'<rect x="{X(x)-0.15:.2f}" y="1.2" width="0.3" height="{dl}" fill="{ZLTA}"/>')
        s.append(f'<rect x="{X(x)-0.15:.2f}" y="{SIRKA-1.2-dl}" width="0.3" height="{dl}" fill="{ZLTA}"/>')
        if k % 10 == 0:
            s.append(text(X(x), 15.0, f"{k*10}", 3.6, KREM, F, sirka_pism=0.2))
    s.append(text(X(kon) + (0 if prava else 0), 15.0, "", 1, KREM, F))
    s += [f'<rect x="{X(22)-14}" y="{SIRKA/2-8.5}" width="28" height="17" rx="0.5" fill="{KREM}"/>', logo(X(22), SIRKA/2, w=27, h=17),
          text(X(92), 12.0, "CESTA SNP", 7.4, KREM, F, sirka_pism=1.0),
          text(X(92), 20.8, KM, 7.4, ZLTA, F, sirka_pism=1.0)]
    return "".join(s)


# 6 – Lesná silueta: zelený prechod, po celej dĺžke smrekový les a slnko
def v6(prava=False):
    def X(x): return POL - x if prava else x
    random.seed(9 + prava)
    s = ['<defs><linearGradient id="l6" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f8a4f"/><stop offset="1" stop-color="#0b3a24"/></linearGradient></defs>',
         f'<rect width="{POL}" height="{SIRKA}" fill="url(#l6)"/>',
         f'<circle cx="{X(130)}" cy="7" r="3.6" fill="{ZLTA}"/>']
    x = 0
    while x < POL:
        v = random.uniform(5, 10)
        for k in range(3):
            w = v * (0.16 + k * 0.08)
            yt = SIRKA - v + k * v * 0.24
            s.append(f'<polygon points="{x:.1f},{yt:.1f} {x+w:.1f},{yt+v*0.36:.1f} {x-w:.1f},{yt+v*0.36:.1f}" fill="#082c1b"/>')
        x += random.uniform(2.5, 5)
    s += [f'<rect x="{X(22)-14}" y="2" width="28" height="15" rx="0.5" fill="{KREM}"/>', logo(X(22), 9.5, w=24, h=14),
          text(X(190), 11.0, "CESTA SNP · " + KM, 7.2, KREM, F, sirka_pism=1.0),
          znacka(X(285), 9.2, 9, 6),
          text(X(355), 10.8, "DEVÍN – DUKLA · 2027", 4.6, ZLTA, F, sirka_pism=0.5),
          text(X(425), 10.6, "VYSLAPSIMEDAILU.SK", 3.4, KREM, F, sirka_pism=0.3)]
    return "".join(s)


# 7 – Stopy: khaki/olivová, po celej dĺžke stopy topánok
def v7(prava=False):
    def X(x): return POL - x if prava else x
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="#5a5a2a"/>',
         f'<rect y="1.4" width="{POL}" height="0.6" fill="{ZLTA}"/>', f'<rect y="{SIRKA-2}" width="{POL}" height="0.6" fill="{ZLTA}"/>']
    def stopa(x, y, uhol):
        return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({uhol})">'
                f'<ellipse cx="0" cy="-0.9" rx="1.6" ry="1.1" fill="{KREM}" opacity="0.55"/>'
                f'<ellipse cx="0" cy="1.3" rx="1.1" ry="0.8" fill="{KREM}" opacity="0.55"/></g>')
    for rng in ((44, 120), (250, 330), (360, 446)):
        x = rng[0]
        k = 0
        while x < rng[1]:
            s.append(stopa(X(x), 9 if k % 2 == 0 else 16, 90 if not prava else -90))
            x += 6
            k += 1
    s += [f'<rect x="{X(22)-14}" y="{SIRKA/2-8.5}" width="28" height="17" rx="0.5" fill="{KREM}"/>', logo(X(22), SIRKA/2, w=27, h=17),
          text(X(185), 15.8, "CESTA SNP", 8.0, KREM, F, sirka_pism=1.2),
          text(X(185 + (55 if not prava else -55)) if False else X(240), 15.8, "", 1, KREM, F),
          f'<rect x="{X(345)-13}" y="7" width="26" height="11" rx="1" fill="#5a5a2a"/>',
          text(X(345), 15.2, KM, 5.4, ZLTA, F, sirka_pism=0.5)]
    return "".join(s)


# 8 – Vintage odznak: hnedo-zelené bloky, okrúhly odznak SNP
def v8(prava=False):
    def X(x): return POL - x if prava else x
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="#1f4a32"/>',
         f'<rect y="0" width="{POL}" height="5" fill="#c9792b"/>', f'<rect y="{SIRKA-5}" width="{POL}" height="5" fill="#c9792b"/>',
         f'<rect y="5" width="{POL}" height="0.8" fill="{ZLTA}"/>', f'<rect y="{SIRKA-5.8}" width="{POL}" height="0.8" fill="{ZLTA}"/>']
    for cx in (X(70), X(330)):
        s.append(f'<circle cx="{cx}" cy="{SIRKA/2}" r="11" fill="{KREM}" stroke="#1f4a32" stroke-width="0.8"/>')
        s.append(f'<circle cx="{cx}" cy="{SIRKA/2}" r="9.3" fill="none" stroke="#c9792b" stroke-width="0.5"/>')
        s.append(f'<polygon points="{cx-6},{SIRKA/2+3.5} {cx-1.5},{SIRKA/2-3.5} {cx+1},{SIRKA/2} {cx+2.5},{SIRKA/2-1.8} {cx+6},{SIRKA/2+3.5}" fill="#1f4a32"/>')
        s.append(f'<circle cx="{cx+3.2}" cy="{SIRKA/2-4.2}" r="1.5" fill="{ZLTA}"/>')
        s.append(text(cx, SIRKA/2 + 7.3, "SNP", 3.2, "#1f4a32", F, sirka_pism=0.6))
    s += [f'<rect x="{X(24)-14}" y="{SIRKA/2-6.5}" width="28" height="13" rx="0.5" fill="{KREM}"/>', logo(X(24), SIRKA/2, w=22, h=12),
          text(X(170), 15.8, "CESTA SNP", 7.6, KREM, F, sirka_pism=1.2),
          text(X(246), 15.8, KM, 7.6, ZLTA, F, sirka_pism=0.8),
          text(X(405), 15.2, "VYSLAPSIMEDAILU.SK", 4.0, KREM, F, sirka_pism=0.3)]
    return "".join(s)


sv.VARIANTY = [("4 · Výškový profil", "Krémová, po dĺžke výškový profil trasy so zvýrazneným Ďumbierom.", v4),
               ("5 · Kilometrovník", "Tmavozelená ako pravítko – žlté dieliky a čísla 0 až 770 km po celej dĺžke.", v5),
               ("6 · Lesná silueta", "Zelený prechod, smrekový les po celej dĺžke, slnko a červená značka.", v6),
               ("7 · Stopy", "Olivová so stopami topánok, ktoré kráčajú po celej stuhe.", v7),
               ("8 · Vintage odznak", "Retro bloky zelenej a hrdzavej s okrúhlymi odznakmi SNP.", v8)]

if __name__ == "__main__":
    svg = sv.harok().replace("Cesta SNP – 3 návrhy stuhy", "Cesta SNP – ďalších 5 návrhov stuhy")
    uloz(svg, f"{sys.argv[1]}/cesta-snp-5-dalsich-navrhov.png")
