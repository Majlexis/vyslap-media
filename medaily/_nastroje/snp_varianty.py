"""Cesta SNP – 3 návrhy stuhy (polovica od medaily po krk)."""
import math, random, sys
sys.path.insert(0, sys.path[0])
from stuhy import logo, text, uloz, KREM, ZLTA, TMZEL, SIRKA, POL, DLZKA
from tatry_stuhy import vrstevnice

F = "Liberation Sans"
ZEL = "#0b4a2c"
CERV = "#d42a2a"
BIELA = "#f7f5ee"
KM = "770 KM"


def znacka(cx, cy, w=10, h=7):
    """Turistická značka: biela–červená–biela."""
    return (f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="{BIELA}"/>'
            f'<rect x="{cx-w/2}" y="{cy-h/6}" width="{w}" height="{h/3}" fill="{CERV}"/>')


def trasa(x0, x1, seed, farba=BIELA, hrubka=0.8, ciarkovane=False):
    random.seed(seed)
    d = f"M{x0},{SIRKA/2}"
    x, y = x0, SIRKA / 2
    while x < x1:
        nx = min(x1, x + random.uniform(8, 16))
        ny = SIRKA / 2 + random.uniform(-5, 5)
        d += f" Q{(x+nx)/2:.1f},{y + random.uniform(-4, 4):.1f} {nx:.1f},{ny:.1f}"
        x, y = nx, ny
    dash = ' stroke-dasharray="2.2 1.4"' if ciarkovane else ""
    return f'<path d="{d}" fill="none" stroke="{farba}" stroke-width="{hrubka}" stroke-linecap="round"{dash}/>'


def bod(cx, cy, popis, farba=ZLTA, popis_farba=KREM, nad=True):
    return (f'<circle cx="{cx}" cy="{cy}" r="1.7" fill="none" stroke="{farba}" stroke-width="0.7"/>'
            f'<circle cx="{cx}" cy="{cy}" r="0.6" fill="{farba}"/>'
            + text(cx, cy - 2.8 if nad else cy + 5, popis, 3.4, popis_farba, F, sirka_pism=0.3))


# 1 – Ako na medaile: zelená s vrstevnicami a dvoma žltými pásmi + červená značka
def v1(prava=False):
    def X(x): return POL - x if prava else x
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="{ZEL}"/>',
        vrstevnice(ZLTA, 3 + prava * 9, hustota=6, op=0.35),
        f'<rect y="2.2" width="{POL}" height="1.1" fill="{ZLTA}"/>', f'<rect y="{SIRKA-3.3}" width="{POL}" height="1.1" fill="{ZLTA}"/>',
        znacka(X(22), SIRKA/2, 13, 9),
        f'<rect x="{X(52)-13}" y="{SIRKA/2-8}" width="26" height="16" rx="0.5" fill="{KREM}"/>', logo(X(52), SIRKA/2, w=26, h=16),
        text(X(140), 15.8, "CESTA SNP", 8.6, KREM, F, sirka_pism=1.4),
        text(X(222), 15.8, KM, 8.6, ZLTA, F, sirka_pism=1.0),
        znacka(X(268), SIRKA/2, 10, 7),
        text(X(318), 15.4, "DEVÍN – DUKLA", 5.2, KREM, F, sirka_pism=0.6),
        text(X(408), 15.2, "VYSLAPSIMEDAILU.SK", 4.4, ZLTA, F, sirka_pism=0.4),
    ])


# 2 – Trasa: tmavozelená, po celej dĺžke vinie trasa od Devína (pri medaile) po Duklu (pri krku)
def v2(prava=False):
    def X(x): return POL - x if prava else x
    def seg(x0, x1, seed):
        a, b = sorted((X(x0), X(x1)))
        return trasa(a, b, seed, "#000", 1.8) + trasa(a, b, seed, KREM, 0.7, ciarkovane=True)
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="#123f2b"/>',
        vrstevnice("#2f6a3c", 5 + prava * 9, hustota=8, op=0.7),
        f'<rect x="{X(30)-13}" y="{SIRKA/2-8}" width="26" height="16" rx="0.5" fill="{KREM}"/>', logo(X(30), SIRKA/2, w=26, h=16),
        seg(62, 112, 7 + prava), seg(250, 300, 17 + prava), seg(358, 430, 27 + prava),
        bod(X(62), SIRKA/2, "DEVÍN", nad=True),
        text(X(150), 16, "CESTA SNP", 8.0, KREM, F, sirka_pism=1.2),
        text(X(212), 16, KM, 8.0, ZLTA, F, sirka_pism=0.8),
        text(X(329), 15.4, "2027", 5.6, ZLTA, F, sirka_pism=1.2),
        bod(X(430), SIRKA/2, "DUKLA", nad=False),
    ])


# 3 – Turistická značka: celá stuha ako červená značka SNP (biela–červená–biela)
def v3(prava=False):
    def X(x): return POL - x if prava else x
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="{BIELA}"/>',
        f'<rect y="7.6" width="{POL}" height="9.8" fill="{CERV}"/>',
        f'<rect y="0" width="{POL}" height="1.6" fill="{ZEL}"/>', f'<rect y="{SIRKA-1.6}" width="{POL}" height="1.6" fill="{ZEL}"/>',
        f'<rect x="{X(30)-15}" y="2.6" width="30" height="19.8" fill="{BIELA}"/>', logo(X(30), SIRKA/2, w=27, h=17),
        text(X(140), 15.9, "CESTA SNP", 8.4, BIELA, F, sirka_pism=1.6),
        text(X(222), 15.9, KM, 8.4, ZLTA, F, sirka_pism=1.0),
        text(X(310), 15.6, "DEVÍN – DUKLA · 2027", 5.0, BIELA, F, sirka_pism=0.5),
        text(X(408), 15.4, "VYSLAPSIMEDAILU.SK", 4.4, BIELA, F, sirka_pism=0.4),
    ])


VARIANTY = [("1 · Ako na medaile", "Zelená s vrstevnicami a žltými pásmi ako vizualizácia, pridaná červená turistická značka a Devín – Dukla.", v1),
            ("2 · Trasa", "Po celej dĺžke sa vinie čiarkovaná trasa od Devína (pri medaile) po Duklu (pri krku).", v2),
            ("3 · Turistická značka", "Celá stuha je červená značka SNP – biela, červená, biela – so zelenými okrajmi.", v3)]


def harok():
    W, m = 2400, 80
    sk = (W - 2 * m) / POL
    hp = SIRKA * sk
    gap = 110
    y = 220
    H = y + len(VARIANTY) * (hp + gap) + 40
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}">',
         f'<rect width="{W}" height="{H}" fill="#fbfaf6"/>',
         text(m, 105, "Cesta SNP – 3 návrhy stuhy", 52, "#1c2a20", F, kotva="start", sirka_pism=0),
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


def finalna(out, idx):
    import stuhy as st
    n, popis, fn = VARIANTY[idx]
    farby = {0: [("Zelená stuha", ZEL), ("Žltá", ZLTA), ("Červená značka", CERV), ("Krémová", KREM)],
             1: [("Zelená stuha", "#123f2b"), ("Vrstevnice", "#2f6a3c"), ("Žltá", ZLTA), ("Krémová", KREM)],
             2: [("Biela", BIELA), ("Červená značka", CERV), ("Zelené okraje", ZEL), ("Žltá", ZLTA)]}[idx]
    zak = {0: ZEL, 1: "#123f2b", 2: BIELA}[idx]
    svg, s = st.harok("Stuha – Cesta SNP", f"Návrh stuhy · 25 × 900 mm · variant {n}", zak,
                      lambda prava: fn(prava), farby, ks="1 ks na medailu")
    uloz(svg, f"{out}/stuha-cesta-snp-2027.png")
    uloz(f'<svg xmlns="http://www.w3.org/2000/svg" width="9000" height="250" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>', f"{out}/stuha-cesta-snp-2027-tlac.png")
    open(f"{out}/stuha-cesta-snp-2027-tlac.svg", "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{DLZKA}mm" height="{SIRKA}mm" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>')


if __name__ == "__main__":
    if len(sys.argv) > 2:
        finalna(sys.argv[1], int(sys.argv[2]) - 1)
    else:
        uloz(harok(), f"{sys.argv[1]}/cesta-snp-3-navrhy.png")
