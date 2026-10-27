"""12 vrcholov za rok – ďalších 5 návrhov stuhy."""
import math, random, sys
sys.path.insert(0, sys.path[0])
from stuhy import logo, text, uloz, KREM, ZLTA, TMZEL, SIRKA, POL
import snp_varianty as sv
from vrcholy12 import stit, stitok_logo, ZEL, TYRK, F, SER

ORANZ = "#f26b2a"
BIELA = "#f7f5ee"
ZELZ = "#1f8a4c"   # zelená turistická značka


def nazov(x, f1, f2, pismo=F, velk=7.2):
    return (text(x, 12.0, "12 VRCHOLOV", velk, f1, pismo, sirka_pism=0.8) +
            text(x, 20.8, "ZA ROK 2027", velk * 0.86, f2, pismo, sirka_pism=1.2))


def odznak12(cx, cy, r, poz=ZLTA, txt=ZEL):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{poz}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.84}" fill="none" stroke="{txt}" stroke-width="0.4"/>'
            + text(cx, cy + r * 0.42, "12", r * 1.15, txt, F, sirka_pism=0))


# 6 – Retro pruhy (ako Východ slnka): zelená, pruhy žltá–tyrkys, odznaky 12
def v6(prava=False):
    def X(x): return POL - x if prava else x
    def blok(a, b): return f'<rect x="{min(X(a), X(b))}" y="0" width="{abs(b-a)}" height="{SIRKA}" fill="{ZEL}"/>'
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="{ZEL}"/>',
        f'<rect y="1.6" width="{POL}" height="1.5" fill="{ZLTA}"/>', f'<rect y="3.6" width="{POL}" height="1.5" fill="{TYRK}"/>',
        f'<rect y="{SIRKA-3.1}" width="{POL}" height="1.5" fill="{ZLTA}"/>', f'<rect y="{SIRKA-5.1}" width="{POL}" height="1.5" fill="{TYRK}"/>',
        blok(8, 40), odznak12(X(24), SIRKA/2, 8.5),
        blok(50, 84), stitok_logo(X(67)),
        blok(110, 250), nazov(X(180), KREM, ZLTA),
        blok(275, 307), odznak12(X(291), SIRKA/2, 7.5),
        blok(350, 448), text(X(399), 15.2, "VYSLAPSIMEDAILU.SK", 4.4, ZLTA, F, sirka_pism=0.4),
    ])


# 7 – Zelená turistická značka: biela–zelená–biela
def v7(prava=False):
    def X(x): return POL - x if prava else x
    return "".join([
        f'<rect width="{POL}" height="{SIRKA}" fill="{BIELA}"/>',
        f'<rect y="7.6" width="{POL}" height="9.8" fill="{ZELZ}"/>',
        f'<rect y="0" width="{POL}" height="1.6" fill="{ZEL}"/>', f'<rect y="{SIRKA-1.6}" width="{POL}" height="1.6" fill="{ZEL}"/>',
        f'<rect x="{X(30)-15}" y="2.6" width="30" height="19.8" fill="{BIELA}"/>', logo(X(30), SIRKA/2, w=27, h=17),
        text(X(150), 15.9, "12 VRCHOLOV", 8.0, BIELA, F, sirka_pism=1.2),
        text(X(235), 15.9, "ZA ROK", 8.0, ZLTA, F, sirka_pism=1.0),
        text(X(310), 15.6, "2027", 6.0, BIELA, F, sirka_pism=1.0),
        text(X(400), 15.4, "VYSLAPSIMEDAILU.SK", 4.4, BIELA, F, sirka_pism=0.4),
    ])


# 8 – Veľká 12: krémová, obrovské obrysové čísla 12 a hory v nich
def v8(prava=False):
    def X(x): return POL - x if prava else x
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="{KREM}"/>',
         f'<rect y="0" width="{POL}" height="1.2" fill="{ZEL}"/>', f'<rect y="{SIRKA-1.2}" width="{POL}" height="1.2" fill="{ZEL}"/>']
    for cx in (X(68), X(330)):
        s.append(f'<text x="{cx}" y="24.6" font-family="{F}" font-weight="bold" font-size="29" fill="{ZLTA}" stroke="{ZEL}" stroke-width="0.6" text-anchor="middle" letter-spacing="-0.5">12</text>')
    s += [logo(X(24), SIRKA/2, w=27, h=17),
          text(X(140), 12.0, "VRCHOLOV", 6.8, ZEL, F, sirka_pism=0.8),
          text(X(140), 20.6, "ZA ROK", 6.8, ZEL, F, sirka_pism=1.6),
          text(X(235), 15.6, "2027", 6.6, ZEL, F, sirka_pism=1.6),
          text(X(420), 15.2, "VYSLAPSIMEDAILU.SK", 3.8, ZEL, F, sirka_pism=0.3)]
    return "".join(s)


# 9 – Mozaika trojuholníkov: geometrické hory po celej dĺžke
def v9(prava=False):
    def X(x): return POL - x if prava else x
    random.seed(12 + prava)
    farby = [ZEL, "#14614f", "#1f7a5c", TYRK, "#2f6a3c", "#0e5245"]
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="{ZEL}"/>']
    krok = 6.25
    for k in range(int(POL / krok) + 2):
        x = k * krok
        for r in range(2):
            y0 = r * SIRKA / 2
            h = SIRKA / 2
            c1, c2 = random.choice(farby), random.choice(farby)
            if random.random() < 0.06:
                c1 = ZLTA
            s.append(f'<polygon points="{x},{y0+h} {x+krok/2},{y0} {x+krok},{y0+h}" fill="{c1}"/>')
            s.append(f'<polygon points="{x+krok/2},{y0} {x+krok*1.5},{y0} {x+krok},{y0+h}" fill="{c2}"/>')
    s += [f'<rect x="{min(X(8), X(44))}" y="2.5" width="36" height="20" rx="1" fill="{KREM}"/>', logo(X(26), SIRKA/2, w=27, h=17),
          f'<rect x="{min(X(100), X(260))}" y="2.5" width="160" height="20" rx="1" fill="{ZEL}"/>', nazov(X(180), KREM, ZLTA),
          f'<rect x="{min(X(345), X(445))}" y="8" width="100" height="9" rx="1" fill="{ZEL}"/>',
          text(X(395), 14.8, "VYSLAPSIMEDAILU.SK", 4.2, ZLTA, F, sirka_pism=0.4)]
    return "".join(s)


# 10 – Nášivky: 12 okrúhlych nášiviek s horami v rôznych farbách
def v10(prava=False):
    def X(x): return POL - x if prava else x
    farby = [("#2c5a8a", KREM), ("#3f8a4f", KREM), ("#e8b32a", ZEL), ("#c4572a", KREM)]
    s = [f'<rect width="{POL}" height="{SIRKA}" fill="#123f37"/>',
         f'<rect y="1.2" width="{POL}" height="0.5" fill="{ZLTA}"/>', f'<rect y="{SIRKA-1.7}" width="{POL}" height="0.5" fill="{ZLTA}"/>',
         stitok_logo(X(22)), nazov(X(100), KREM, ZLTA, SER, 6.6)]
    for k in range(6):
        cx = X(182 + k * 42)
        poz, hor = farby[(k + (2 if prava else 0)) % 4]
        cislo = k + 7 if prava else k + 1
        s.append(f'<circle cx="{cx}" cy="{SIRKA/2}" r="9.5" fill="{poz}" stroke="{KREM}" stroke-width="0.6" stroke-dasharray="0.9 0.6"/>')
        s.append(f'<polygon points="{cx-6.5},{SIRKA/2+4} {cx-1.5},{SIRKA/2-4} {cx+1.2},{SIRKA/2} {cx+2.8},{SIRKA/2-2} {cx+6.5},{SIRKA/2+4}" fill="{hor}"/>')
        s.append(text(cx, SIRKA/2 + 8.0, str(cislo), 2.8, hor, F))
    return "".join(s)


sv.VARIANTY = [("6 · Retro pruhy", "Ako stuha Východu slnka – zelená, pruhy žltá a tyrkysová, okrúhle odznaky s číslom 12.", v6),
               ("7 · Zelená značka", "Ako stuha SNP, ale v zelenej turistickej značke – biela, zelená, biela.", v7),
               ("8 · Veľká 12", "Krémová so zelenými okrajmi a veľkými žltými číslami 12.", v8),
               ("9 · Mozaika", "Geometrická mozaika trojuholníkov v odtieňoch zelenej a tyrkysovej, sem-tam žltý.", v9),
               ("10 · Nášivky", "12 okrúhlych nášiviek s horami, každá v inej farbe (6 na každej strane).", v10)]

if __name__ == "__main__":
    svg = sv.harok().replace("Cesta SNP – 3 návrhy stuhy", "12 vrcholov za rok – ďalších 5 návrhov")
    uloz(svg, f"{sys.argv[1]}/12-vrcholov-dalsich-5.png")


def finalna(out):
    import stuhy as st
    from stuhy import DLZKA
    svg, s = st.harok("Stuha – 12 vrcholov za rok", "Návrh stuhy · 25 × 900 mm · variant Veľká 12", KREM, v8,
                      [("Krémová stuha", KREM), ("Zelená", ZEL), ("Žltá", ZLTA)], ks="1 ks na medailu")
    uloz(svg, f"{out}/stuha-12-vrcholov-2027.png")
    uloz(f'<svg xmlns="http://www.w3.org/2000/svg" width="9000" height="250" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>', f"{out}/stuha-12-vrcholov-2027-tlac.png")
    open(f"{out}/stuha-12-vrcholov-2027-tlac.svg", "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{DLZKA}mm" height="{SIRKA}mm" viewBox="0 0 {DLZKA} {SIRKA}">{s}</svg>')
