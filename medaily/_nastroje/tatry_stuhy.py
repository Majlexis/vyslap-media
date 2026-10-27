"""Návrhy stúh pre prémiovú kolekciu Tatry 2027 (5 medailí) – 3 varianty na výber."""
import math, random, sys
sys.path.insert(0, sys.path[0])
from stuhy import logo, text, uloz, KREM, DLZKA, SIRKA, POL

ORANZ = "#f05a14"
STRIEBRO = "#d9dcdf"
VRCHOLY = [  # názov (2 riadky), výška, farba stuhy, svetlejší tón vzoru
    ("Rysy", "", 2499, "#02403d", "#1a8f86"),
    ("Kriváň", "", 2495, "#a1250d", "#d9603a"),
    ("Slavkovský", "štít", 2452, "#0a325a", "#3f78b5"),
    ("Východná", "Vysoká", 2429, "#1e1e1e", "#5a5a5a"),
    ("Kôprovský", "štít", 2367, "#474018", "#b39b3a"),
]
F = "Liberation Sans"


def vrstevnice(farba, seed, hustota=7, op=0.55, od=0, do=POL):
    """Topografické vrstevnice po dĺžke stuhy (ako tkaný vzor na medailách)."""
    random.seed(seed)
    s = []
    for k in range(hustota):
        y0 = (k + 0.5) * SIRKA / hustota
        a, f1, f2, ph = random.uniform(0.8, 1.8), random.uniform(0.04, 0.09), random.uniform(0.11, 0.2), random.uniform(0, 6)
        bod = []
        x = od
        while x <= do:
            y = y0 + a * math.sin(x * f1 + ph) + 0.5 * math.sin(x * f2 + ph * 2)
            bod.append(f"{x:.1f},{y:.2f}")
            x += 2
        s.append(f'<polyline points="{" ".join(bod)}" fill="none" stroke="{farba}" stroke-width="0.35" opacity="{op}"/>')
    return "".join(s)


def slnko(x, y, r):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{ORANZ}"/>'


def hrebien(x0, x1, farba, vyska, seed, op=1):
    """Silueta hrebeňa po dĺžke stuhy (spodná časť)."""
    random.seed(seed)
    pts = [f"{x0},{SIRKA}"]
    x = x0
    while x < x1:
        pts.append(f"{x:.1f},{SIRKA - random.uniform(0.35, 1) * vyska:.1f}")
        x += random.uniform(4, 9)
    pts += [f"{x1},{SIRKA - vyska*0.4}", f"{x1},{SIRKA}"]
    return f'<polygon points="{" ".join(pts)}" fill="{farba}" opacity="{op}"/>'


def nazov(x, n1, n2, farba, velk=7.4):
    if n2:
        return text(x, 11.2, n1.upper(), velk * 0.92, farba, F, sirka_pism=0.8) + text(x, 20.6, n2.upper(), velk * 0.92, farba, F, sirka_pism=0.8)
    return text(x, 15.8, n1.upper(), velk * 1.25, farba, F, sirka_pism=2.2)


# ---------- varianty jednej polovice (x=0 pri medaile, x=450 pri krku) ----------
def var_a(i, v):
    """A – Farebná topografia: každá stuha vo farbe svojho vrcholu."""
    n1, n2, vys, zak, svet = v
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="{zak}"/>',
        vrstevnice(svet, i * 7 + 1, op=0.4),
        logo(30, SIRKA / 2, w=25, h=17),
        nazov(160, n1, n2, KREM),
        slnko(238, 8.5, 4.0), text(238, 20.2, f"{vys} m", 5.2, ORANZ, F, sirka_pism=0.3),
        text(320, 15.6, "TATRY 2027", 6.4, KREM, F, sirka_pism=1.4),
        text(415, 15.3, "VYSLAPSIMEDAILU.SK", 4.4, svet, F, sirka_pism=0.4),
    ])


def var_b(i, v):
    """B – Čierna prémiová: všetky čierne, farba vrcholu len v pásoch po okrajoch."""
    n1, n2, vys, zak, svet = v
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="#141414"/>',
        vrstevnice("#4a4a4a", i * 7 + 1, op=0.6),
        f'<rect y="0" width="{POL}" height="3.2" fill="{zak if i != 3 else STRIEBRO}"/>',
        f'<rect y="{SIRKA-3.2}" width="{POL}" height="3.2" fill="{zak if i != 3 else STRIEBRO}"/>',
        f'<rect y="3.6" width="{POL}" height="0.4" fill="{ORANZ}"/>',
        f'<rect y="{SIRKA-4}" width="{POL}" height="0.4" fill="{ORANZ}"/>',
        text(19, 15.5, f"{i+1}/5", 7, STRIEBRO, F, sirka_pism=0.3),
        logo(52, SIRKA / 2, w=25, h=15),
        nazov(160, n1, n2, STRIEBRO, 6.3) if n2 else nazov(160, n1, n2, STRIEBRO, 7.0),
        slnko(238, 9.6, 3.6), text(238, 19.4, f"{vys} m", 5, ORANZ, F, sirka_pism=0.3),
        text(320, 15.6, "TATRY 2027", 6.4, STRIEBRO, F, sirka_pism=1.4),
        text(415, 15.3, "VYSLAPSIMEDAILU.SK", 4.4, "#8a8a8a", F, sirka_pism=0.4),
    ])


def var_c(i, v):
    """C – Hrebeň: farba vrcholu, po celej dĺžke silueta tatranského hrebeňa a slnko."""
    n1, n2, vys, zak, svet = v
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="{zak}"/>',
        hrebien(0, POL, svet, 9, i * 11 + 3, op=0.55),
        hrebien(0, POL, "#000", 5, i * 11 + 4, op=0.25),
        text(19, 11, f"{i+1}/5", 6, KREM, F, sirka_pism=0.3),
        logo(52, 9.8, w=22, h=14),
        (text(160, 8.6, n1.upper(), 5.6, KREM, F, sirka_pism=0.8) + text(160, 15.2, n2.upper(), 5.6, KREM, F, sirka_pism=0.8)) if n2 else text(160, 12.6, n1.upper(), 8.6, KREM, F, sirka_pism=2.2),
        slnko(238, 8.5, 4.6),
        text(238 + 0, 16.6, "", 1, KREM, F),
        text(300, 11.6, f"{vys} m", 5.6, ORANZ, F, sirka_pism=0.4),
        text(360, 11.6, "TATRY 2027", 5.8, KREM, F, sirka_pism=1.2),
        text(420, 11.3, "VYSLAPSIMEDAILU.SK", 3.6, KREM, F, sirka_pism=0.3),
    ])


VARIANTY = {
    "a": ("A · Farebná topografia", "Každý vrchol má svoju farbu (ako na medailách), jemné vrstevnice, oranžové slnko a výška vrcholu.", var_a),
    "b": ("B · Čierna prémiová", "Všetkých 5 stúh čiernych so striebornými nápismi, farba vrcholu len v okrajových pásoch + oranžová linka.", var_b),
    "c": ("C · Tatranský hrebeň", "Farba vrcholu, po celej dĺžke silueta hrebeňa – vedľa seba tvoria jednu panorámu Tatier.", var_c),
}


def polovica_svg(fn, i, v, prava=False):
    vnutro = fn(i, v)
    tien = (f'<linearGradient id="t{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.2"/>'
            f'<stop offset="0.15" stop-color="#000" stop-opacity="0"/><stop offset="0.85" stop-color="#000" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0.22"/></linearGradient>')
    return f'<defs>{tien}</defs>{vnutro}<rect width="{POL}" height="{SIRKA}" fill="url(#t{i})"/>'


def harok(kluc):
    nazov_v, popis, fn = VARIANTY[kluc]
    W, m = 2400, 80
    sk = (W - 2 * m) / POL
    hp = SIRKA * sk
    gap = 95
    y = 250
    H = y + 5 * (hp + gap) + 60
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H:.0f}" viewBox="0 0 {W} {H:.0f}">',
         f'<rect width="{W}" height="{H}" fill="#fbfaf6"/>',
         text(m, 105, f"Tatry 2027 – stuhy, variant {nazov_v}", 52, "#1c2a20", F, kotva="start", sirka_pism=0),
         f'<text x="{m}" y="160" font-family="{F}" font-size="30" fill="#4a5a4f">{popis}</text>',
         f'<text x="{m}" y="205" font-family="{F}" font-size="24" fill="#6b776f">Polovica stuhy od medaily (vľavo) po krk (vpravo) · 25 × 900 mm · druhá polovica je zrkadlová</text>']
    for i, v in enumerate(VRCHOLY):
        yy = y + i * (hp + gap)
        s.append(f'<text x="{m}" y="{yy+18}" font-family="{F}" font-weight="bold" font-size="26" fill="#1c2a20">{i+1}/5  {v[0]} {v[1]}  ·  {v[2]} m</text>')
        s.append(f'<svg x="{m}" y="{yy+32}" width="{W-2*m}" height="{hp}" viewBox="0 0 {POL} {SIRKA}">{polovica_svg(fn, i, v)}</svg>')
    s.append("</svg>")
    return "".join(s)


# ---------- finálny variant A: celá stuha po vrcholoch (bez poradia 1/5) ----------
def polovica_a(i, v):
    n1, n2, vys, zak, svet = v
    def pol(prava):
        def X(x): return POL - x if prava else x
        return "".join([
            vrstevnice(svet, i * 7 + 1 + (50 if prava else 0), op=0.4),
            logo(X(30), SIRKA / 2, w=25, h=17),
            nazov(X(150), n1, n2, KREM),
            slnko(X(238), 8.5, 4.0), text(X(238), 20.2, f"{vys} m", 5.2, ORANZ, F, sirka_pism=0.3),
            text(X(320), 15.6, "TATRY 2027", 6.4, KREM, F, sirka_pism=1.4),
            text(X(415), 15.3, "VYSLAPSIMEDAILU.SK", 4.4, svet, F, sirka_pism=0.4),
        ])
    return pol


def finalne(out):
    import stuhy as st
    slugy = ["rysy", "krivan", "slavkovsky-stit", "vychodna-vysoka", "koprovsky-stit"]
    for i, (v, slug) in enumerate(zip(VRCHOLY, slugy)):
        meno = f"{v[0]} {v[1]}".strip()
        svg, s = st.harok(f"Stuha – Tatry 2027 · {meno}", f"Návrh stuhy · 25 × 900 mm · {v[2]} m n. m.",
                          v[3], polovica_a(i, v),
                          [("Stuha", v[3]), ("Vrstevnice", v[4]), ("Slnko", ORANZ), ("Krémová", KREM)],
                          ks="1 ks na medailu")
        uloz(svg, f"{out}/{slug}-stuha-nahlad.png")
        cela = f'<svg xmlns="http://www.w3.org/2000/svg" width="9000" height="250" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>'
        uloz(cela, f"{out}/{slug}-stuha-tlac.png")
        open(f"{out}/{slug}-stuha-tlac.svg", "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{DLZKA}mm" height="{SIRKA}mm" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>')


if __name__ == "__main__":
    out = sys.argv[1]
    if sys.argv[2:] == ["finalne"]:
        finalne(out); sys.exit()
    for k in (sys.argv[2:] or VARIANTY):
        uloz(harok(k), f"{out}/tatry-stuhy-variant-{k}.png")

