"""12 vrcholov za rok – 5 návrhov stuhy."""
import math, random, sys
sys.path.insert(0, sys.path[0])
from stuhy import logo, text, uloz, KREM, ZLTA, TMZEL, SIRKA, POL, DLZKA
import snp_varianty as sv

F, SER = "Liberation Sans", "DejaVu Serif"
ZEL = "#0b4a3f"
TYRK = "#3fb39a"
BRONZ = "#c9973a"
MES = ["JAN", "FEB", "MAR", "APR", "MÁJ", "JÚN", "JÚL", "AUG", "SEP", "OKT", "NOV", "DEC"]


def smrek(x, zem, v, farba, hore=False):
    s = ""
    for k in range(3):
        w = v * (0.18 + k * 0.09)
        yt = zem - v + k * v * 0.24
        s += f'<polygon points="{x:.1f},{yt:.1f} {x+w:.1f},{yt+v*0.36:.1f} {x-w:.1f},{yt+v*0.36:.1f}" fill="{farba}"/>'
    return s


def stit(cx, zem, v, farba=KREM, sneh=None):
    s = f'<polygon points="{cx-v*0.8},{zem} {cx},{zem-v} {cx+v*0.8},{zem}" fill="{farba}"/>'
    if sneh:
        s += f'<polygon points="{cx-v*0.25},{zem-v*0.69} {cx},{zem-v} {cx+v*0.25},{zem-v*0.69} {cx+v*0.08},{zem-v*0.6} {cx-v*0.08},{zem-v*0.66}" fill="{sneh}"/>'
    return s


def stitok_logo(x, y=None, w=27, h=17):
    y = SIRKA / 2 if y is None else y
    return f'<rect x="{x-w/2-1}" y="{y-h/2}" width="{w+2}" height="{h}" rx="0.5" fill="{KREM}"/>' + logo(x, y, w=w, h=h)


def nazov2(x, farba1, farba2, pismo=SER, velk=7.4):
    return (text(x, 12.0, "12 VRCHOLOV", velk, farba1, pismo, sirka_pism=0.8) +
            text(x, 20.8, "ZA ROK 2027", velk * 0.86, farba2, pismo, sirka_pism=1.2))


# 1 – Ako na medaile
def v1(prava=False):
    def X(x): return POL - x if prava else x
    random.seed(4 + prava)
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="{ZEL}"/>',
         f'<rect y="2.2" width="{POL}" height="0.9" fill="{ZLTA}"/>', f'<rect y="{SIRKA-3.1}" width="{POL}" height="0.9" fill="{ZLTA}"/>']
    for a, b in ((44, 100), (220, 330)):
        x = a
        while x < b:
            s.append(smrek(X(x), SIRKA - 4, random.uniform(7, 11), TYRK))
            x += random.uniform(9, 14)
    s += [stitok_logo(X(22)), nazov2(X(160), KREM, ZLTA),
          text(X(395), 15.2, "VYSLAPSIMEDAILU.SK", 4.2, ZLTA, F, sirka_pism=0.4)]
    return "".join(s)


# 2 – Kalendár: 12 mesiacov, ľavá polovica JAN–JÚN, pravá JÚL–DEC
def v2(prava=False):
    def X(x): return POL - x if prava else x
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="{ZEL}"/>',
         f'<rect y="1.2" width="{POL}" height="0.6" fill="{ZLTA}"/>', f'<rect y="{SIRKA-1.8}" width="{POL}" height="0.6" fill="{ZLTA}"/>',
         stitok_logo(X(22)), nazov2(X(98), KREM, ZLTA, F, 6.8)]
    mesiace = MES[6:][::-1] if prava else MES[:6]   # pravá polovica sa číta od krku k medaile: JÚL… pri krku
    if prava:
        mesiace = MES[6:]
        pozicie = [X(440 - k * 46) for k in range(6)]
    else:
        pozicie = [X(170 + k * 46) for k in range(6)]
    for m, x in zip(mesiace, pozicie):
        s.append(f'<rect x="{x-19}" y="4" width="38" height="17" rx="1" fill="none" stroke="{TYRK}" stroke-width="0.4"/>')
        s.append(stit(x - 8, 18.5, 9, KREM, sneh=None) + f'<circle cx="{x-3.5}" cy="9.6" r="1.6" fill="{ZLTA}"/>')
        s.append(text(x + 7.5, 15.4, m, 5.4, ZLTA, F, sirka_pism=0.3))
    return "".join(s)


# 3 – 12 bodiek: ako na medaile, bronzové bodky za každý vrchol
def v3(prava=False):
    def X(x): return POL - x if prava else x
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="#123f37"/>',
         sv.vrstevnice(TYRK, 8 + prava, hustota=7, op=0.25) if hasattr(sv, "vrstevnice") else ""]
    s += [stitok_logo(X(22)), nazov2(X(110), KREM, ZLTA)]
    for k in range(12):
        x = X(195 + k * 20)
        s.append(f'<circle cx="{x}" cy="{SIRKA/2}" r="2.6" fill="{BRONZ}" stroke="#7d5a1d" stroke-width="0.4"/>')
        s.append(f'<circle cx="{x-0.7}" cy="{SIRKA/2-0.8}" r="0.8" fill="#f2d48a"/>')
        s.append(text(x, SIRKA/2 + 7.6, str(k + 1), 2.8, KREM, F))
    s.append(text(X(437), 15.2, "2027", 4.4, ZLTA, F, sirka_pism=0.6))
    return "".join(s)


# 4 – Ročné obdobia: farba sa mení zima → jar → leto → jeseň
def v4(prava=False):
    def X(x): return POL - x if prava else x
    if prava:  # od krku (leto) k medaile (jeseň → zima)
        stops = [("0", "#e8932a"), ("0.5", "#c4572a"), ("1", "#2c5a8a")]
    else:      # od medaily (zima) ku krku (jar → leto)
        stops = [("0", "#2c5a8a"), ("0.5", "#3f8a4f"), ("1", "#e8b32a")]
    gid = f"o{int(prava)}"
    g = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    s = [f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="{POL}" y2="0" gradientUnits="userSpaceOnUse">{g}</linearGradient></defs>',
         f'<rect width="{POL}" height="{SIRKA}" fill="url(#{gid})"/>',
         f'<rect y="0" width="{POL}" height="1.4" fill="{ZEL}"/>', f'<rect y="{SIRKA-1.4}" width="{POL}" height="1.4" fill="{ZEL}"/>',
         stitok_logo(X(22)), nazov2(X(105), KREM, KREM, F, 7.0)]
    for k in range(6):
        x = X(185 + k * 44)
        s.append(stit(x, 19.5, 11, "#ffffff", sneh=None).replace('fill="#ffffff"', 'fill="#ffffff" opacity="0.85"'))
        s.append(text(x, 23.2, str((k + 7) if prava else (k + 1)), 3.0, KREM, F))
    return "".join(s)


# 5 – Hrebeň 12 štítov: tmavozelená, rad 12 štítov s vlajočkami a číslami
def v5(prava=False):
    def X(x): return POL - x if prava else x
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="{ZEL}"/>',
         f'<rect y="{SIRKA-2.2}" width="{POL}" height="2.2" fill="{ZLTA}"/>',
         stitok_logo(X(22), 11.5, 24, 15), nazov2(X(98), KREM, ZLTA, SER, 6.6)]
    for k in range(12):
        x = X(180 + k * 21.5)
        v = 12 + (3 if k % 3 == 1 else 0) - (2 if k % 4 == 3 else 0)
        s.append(stit(x, SIRKA - 2.2, v, "#7d8a86", sneh=KREM))
        s.append(f'<line x1="{x}" y1="{SIRKA-2.2-v}" x2="{x}" y2="{SIRKA-2.2-v-3.6}" stroke="{KREM}" stroke-width="0.3"/>')
        s.append(f'<polygon points="{x},{SIRKA-2.2-v-3.6} {x+2.4},{SIRKA-2.2-v-3} {x},{SIRKA-2.2-v-2.4}" fill="{ZLTA}"/>')
        s.append(text(x, SIRKA - 4, str(k + 1), 2.8, "#1c2a20", F))
    return "".join(s)


sv.VARIANTY = [("1 · Ako na medaile", "Tmavozelená so žltými pásmi a tyrkysovými smrekmi, nápis v pätkovom písme ako na medaile.", v1),
               ("2 · Kalendár", "12 mesiacov po celej stuhe – JAN až JÚN na jednej strane, JÚL až DEC na druhej, každý so štítom.", v2),
               ("3 · 12 bodiek", "Ako bronzové bodky na medaile – 12 bodiek s číslami, jedna za každý vrchol.", v3),
               ("4 · Ročné obdobia", "Farba sa mení po dĺžke: zima (modrá) → jar (zelená) → leto (žltá) → jeseň (oranžová), 12 štítov.", v4),
               ("5 · Hrebeň 12 štítov", "Rad 12 zasnežených štítov s vlajočkami a číslami 1 až 12.", v5)]

if __name__ == "__main__":
    svg = sv.harok().replace("Cesta SNP – 3 návrhy stuhy", "12 vrcholov za rok – 5 návrhov stuhy")
    uloz(svg, f"{sys.argv[1]}/12-vrcholov-5-navrhov.png")
