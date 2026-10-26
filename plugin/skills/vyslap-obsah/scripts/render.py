#!/usr/bin/env python3
"""Vyšľap si medailu – generátor grafiky pre IG/FB v štýle publikovaných postov.

Použitie:
    python3 render.py spec.json out_dir

spec.json:
{
  "format": "carousel" | "post" | "story",   # carousel/post = 1080x1350, story = 1080x1920
  "slides": [ { "typ": "uvod", ... }, ... ]
}

Typy slidov (vzory v assets/vzory/):
  uvod    – krémový vrch s hlavičkou + zelený pás dole (vzor 01-uvod.png)
            riadky: ["Tvoja výzva.", "Tvoje tempo.", "Tvoja medaila."]  (povinné)
            zvyraznit: index riadku v žltom bloku (predvolene posledný; -1 = žiadny)
            podnadpis: "Choď von. Splň cieľ.\\nZískaj medailu."
            velke: "2027"   velke_popis: "ROK TVOJICH VÝZIEV"   dalej: "Posuň ďalej →"
  zoznam  – zelený panel, veľké žlté čísla 01/02 so zvislou čiarou (vzor 02-zoznam.png)
            nadpis (povinné), polozky: [{"nazov": "NOVOROČNÝCH 100", "text": "..."}] (max 3), poznamka
  kroky   – zelený panel, číslované kroky v boxoch (vzor 03-kroky.png)
            stitok: "02 / POHYB", nadpis (žltý), podnadpis (krémový),
            kroky: [{"nazov": "Vyber si výzvu.", "text": "..."}] (max 4)
  blok    – zelený panel so žltým blokom veľkými písmenami (vzor 04-blok.png)
            stitok, nadpis, blok: "KOVOVÁ\\nMEDAILA", text (tučný), maly (normálny)
  text    – zelený panel, nadpis + odseky
            stitok, nadpis, text: "..." alebo ["odsek", "odsek"]
  koniec  – krémový záver s dátumom v žltom a webom v zelenom boxe (vzor 05-koniec.png)
            nadpis (povinné), uvod, zvyraznenie: "15. novembra 2026", text, odkaz (predvolene web)
  fotka   – fotka v kruhu so žltým lemom, veľké písmo, šikmý žltý pás (vzor 06-fotka.png)
            maly: "Dnes stačí spraviť", velke: "PRVÝ", pas: "KROK.", obrazok: cesta (povinné)

Voliteľne na každom slide (striedmo – max 1 na slide, 1–2 na carousel):
  ikona: "medaila" | "darcek" | "topanka" | "hory" | "cesta" | "kalendar" | "srdce" | "vlocka"
         | "stromcek" | "pes" | "dvojica"  alebo jedno emoji, napr. "🎄"
  nalepka: true  -> nechá prázdne miesto na IG nálepku (anketa, odpočet, otázka, odkaz) – Alex ju vloží v aplikácii
  ikona_pozicia: "pravo-hore" (predvolené na paneli) | "pravo-dole" (predvolené pri uvod/koniec)

Značky v texte:
  **slovo**  -> akcentová farba (žltá na zelenej, zelená na krémovej)
  \\n         -> nový riadok
"""
import base64, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"

KREM, ZELENA, ZLTA = "#f6f3e9", "#063f2d", "#ffca1b"
WEB = "vyslapsimedailu.sk"


def md(t: str) -> str:
    t = html.escape(str(t))
    t = re.sub(r"\*\*(.+?)\*\*", r'<span class="ak">\1</span>', t)
    return t.replace("\n", "<br>")


def _b64(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def img_src(p: str, base: Path) -> str:
    path = Path(p)
    if not path.is_absolute():
        path = (base / path).resolve()
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return _b64(path, mime)


LOGO = (f'<svg class="logo" viewBox="0 0 116 76" xmlns="http://www.w3.org/2000/svg">'
        f'<circle cx="95" cy="16" r="16" fill="{ZLTA}"/>'
        f'<path d="M0 74 L46 20 L78 58 L64 74 Z" fill="{ZELENA}"/>'
        f'<path d="M38 74 L72 36 L114 74 Z" fill="{ZELENA}"/>'
        f'<path d="M54 74 L72 55 L90 74" fill="none" stroke="{KREM}" stroke-width="3.2"/>'
        f'</svg>')

# Malé kreslené ikony vo farbách značky (viewBox 0 0 120 120). Používať striedmo: max 1 na slide, 1–2 na carousel.
Z, Y, K = ZELENA, ZLTA, KREM
IKONY = {
  "medaila": f'<path d="M38 8h18l10 34H48z" fill="{Y}"/><path d="M82 8H64L54 42h18z" fill="{Y}" opacity=".75"/>'
             f'<circle cx="60" cy="78" r="34" fill="{Y}" stroke="{Z}" stroke-width="5"/><circle cx="60" cy="78" r="22" fill="none" stroke="{Z}" stroke-width="3" stroke-dasharray="4 5"/>'
             f'<path d="M60 64l5 10 11 2-8 8 2 11-10-5-10 5 2-11-8-8 11-2z" fill="{Z}"/>',
  "darcek": f'<rect x="18" y="52" width="84" height="56" rx="4" fill="{Y}" stroke="{Z}" stroke-width="5"/><rect x="12" y="36" width="96" height="20" rx="4" fill="{Y}" stroke="{Z}" stroke-width="5"/>'
            f'<path d="M60 36v72" stroke="{Z}" stroke-width="10"/><path d="M60 34c-8-16-32-22-32-8 0 9 18 8 32 8zM60 34c8-16 32-22 32-8 0 9-18 8-32 8z" fill="{Y}" stroke="{Z}" stroke-width="5" stroke-linejoin="round"/>',
  "topanka": f'<path d="M20 30h26l4 22c14 4 30 10 44 18 8 4 12 10 12 18v8H20z" fill="{Y}" stroke="{Z}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M20 86h86v12H20z" fill="{Z}"/><path d="M50 56l10-4M56 64l10-4M62 72l10-4" stroke="{Z}" stroke-width="4" stroke-linecap="round"/>',
  "hory":    f'<circle cx="88" cy="32" r="16" fill="{Y}"/><path d="M6 100L44 46l20 26 14-16 36 44z" fill="{Z}"/><path d="M44 46l-9 13 9-4 9 6z" fill="{K}"/>',
  "cesta":   f'<path d="M18 104c10-30 70-10 70-40S34 50 40 22" fill="none" stroke="{Y}" stroke-width="8" stroke-linecap="round"/><circle cx="18" cy="104" r="8" fill="{K}" stroke="{Z}" stroke-width="4"/>'
             f'<path d="M40 22V4l22 8-22 8" fill="{Y}" stroke="{Z}" stroke-width="3" stroke-linejoin="round"/>',
  "kalendar":f'<rect x="14" y="22" width="92" height="84" rx="8" fill="{K}" stroke="{Z}" stroke-width="5"/><path d="M14 30a8 8 0 0 1 8-8h76a8 8 0 0 1 8 8v16H14z" fill="{Y}" stroke="{Z}" stroke-width="5"/>'
             f'<path d="M36 12v20M84 12v20" stroke="{Z}" stroke-width="6" stroke-linecap="round"/><path d="M42 78l12 12 26-28" fill="none" stroke="{Z}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
  "srdce":   f'<path d="M60 104S14 76 14 44c0-16 12-26 25-26 10 0 17 6 21 13 4-7 11-13 21-13 13 0 25 10 25 26 0 32-46 60-46 60z" fill="{Y}" stroke="{Z}" stroke-width="5" stroke-linejoin="round"/>',
  "vlocka":  f'<g stroke="{Y}" stroke-width="7" stroke-linecap="round"><path d="M60 10v100M17 35l86 50M17 85l86-50"/>'
             f'<path d="M48 18l12 10 12-10M48 102l12-10 12 10M14 50l16 4-4-16M106 70l-16-4 4 16M14 70l16-4-4 16M106 50l-16 4 4-16"/></g>',
  "stromcek":f'<path d="M60 8L28 52h14L22 80h18L16 106h88L80 80h18L78 52h14z" fill="{Z}" stroke="{K}" stroke-width="3" stroke-linejoin="round"/>'
             f'<circle cx="60" cy="10" r="8" fill="{Y}"/><circle cx="46" cy="66" r="5" fill="{Y}"/><circle cx="72" cy="88" r="5" fill="{Y}"/><circle cx="68" cy="44" r="4" fill="{Y}"/>',
  "pes":     f'<path d="M30 40c-14-4-22 22-12 34l14-10zM90 40c14-4 22 22 12 34L88 64z" fill="{Z}"/><ellipse cx="60" cy="68" rx="32" ry="34" fill="{Y}" stroke="{Z}" stroke-width="5"/>'
             f'<circle cx="48" cy="62" r="5" fill="{Z}"/><circle cx="72" cy="62" r="5" fill="{Z}"/><ellipse cx="60" cy="78" rx="9" ry="7" fill="{Z}"/><path d="M52 90q8 8 16 0" fill="none" stroke="{Z}" stroke-width="4" stroke-linecap="round"/>',
  "dvojica": f'<circle cx="42" cy="34" r="14" fill="{Y}" stroke="{Z}" stroke-width="5"/><circle cx="80" cy="34" r="14" fill="{Y}" stroke="{Z}" stroke-width="5"/>'
             f'<path d="M20 104c0-26 10-42 22-42s22 16 22 42M58 104c0-26 10-42 22-42s22 16 22 42" fill="{Y}" stroke="{Z}" stroke-width="5" stroke-linejoin="round"/>',
}


def ikona_html(meno: str, trieda: str, na_zelenej: bool) -> str:
    if not meno:
        return ""
    if meno in IKONY:
        svg = IKONY[meno]
        if na_zelenej:  # na zelenom pozadí prehodiť zelenú a krémovú, aby bol vidieť obrys
            svg = svg.replace(Z, "@@").replace(K, Z).replace("@@", K)
        return f'<svg class="ikona {trieda}" viewBox="-6 -6 132 132" xmlns="http://www.w3.org/2000/svg">{svg}</svg>'
    return f'<div class="ikona emoji {trieda}">{html.escape(meno)}</div>'  # emoji


CSS = f"""
@font-face {{ font-family: 'VSM'; src: url('{_b64(FONTS / 'LiberationSans-Regular.ttf', 'font/ttf')}'); font-weight: 400; }}
@font-face {{ font-family: 'VSM'; src: url('{_b64(FONTS / 'LiberationSans-Bold.ttf', 'font/ttf')}'); font-weight: 700; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: var(--w); height: var(--h); }}
body {{ font-family: 'VSM', Arial, sans-serif; color: {ZELENA}; background: {KREM}; overflow: hidden; }}
.s {{ position: relative; width: var(--w); height: var(--h); display: flex; flex-direction: column; overflow: hidden; }}
b, strong {{ font-weight: 700; }}

/* hlavička a päta – rovnaké na každom slide */
.hlavicka {{ flex: none; height: 174px; display: flex; align-items: center; gap: 32px; padding: 0 72px 6px 76px; }}
.hlavicka .logo {{ width: 116px; height: 76px; flex: none; }}
.hlavicka span {{ font-weight: 700; font-size: 36px; letter-spacing: .3px; padding-top: 14px; }}
.pata {{ flex: none; height: 156px; display: flex; justify-content: space-between; align-items: center; padding: 0 106px 0 72px; font-size: 28px; }}
.pata .str {{ letter-spacing: .5px; }}

/* zelený panel */
.panel {{ flex: 1; min-height: 0; background: {ZELENA}; color: {KREM}; padding: 50px 72px 56px; display: flex; flex-direction: column; }}
.panel .ak {{ color: {ZLTA}; }}
.krem .ak {{ color: {ZELENA}; background: {ZLTA}; padding: 0 6px; }}
.stitok {{ color: {ZLTA}; font-weight: 700; font-size: 28px; letter-spacing: .5px; text-transform: uppercase; margin-top: 4px; margin-bottom: 26px; white-space: pre; }}
h1 {{ font-weight: 700; font-size: 84px; line-height: 1.24; letter-spacing: -.5px; }}
h1.zlty {{ color: {ZLTA}; font-size: 100px; line-height: 1.12; }}
h2.podnadpis {{ font-weight: 700; font-size: 80px; line-height: 1.2; color: {KREM}; margin-top: 6px; }}

/* uvod */
.t-uvod .vrch {{ flex: 1; padding: 46px 72px 0; display: flex; flex-direction: column; }}
.t-uvod .riadok {{ font-weight: 700; font-size: 92px; line-height: 1.2; letter-spacing: -.5px; }}
.t-uvod .riadok.zlty {{ background: {ZLTA}; margin: 0 -10px 0 -10px; padding: 0 10px; width: calc(100% + 20px); }}
.t-uvod .pod {{ font-weight: 700; font-size: 36px; line-height: 1.33; margin-top: 30px; padding-left: 4px; }}
.t-uvod .spodok {{ flex: none; height: 397px; background: {ZELENA}; color: {KREM}; padding: 24px 72px 30px 68px; display: flex; flex-direction: column; }}
.t-uvod .velke {{ color: {ZLTA}; font-weight: 700; font-size: 176px; line-height: 1; letter-spacing: -2px; }}
.t-uvod .velke-popis {{ font-weight: 700; font-size: 40px; letter-spacing: .3px; text-transform: uppercase; margin-top: 36px; padding-left: 8px; }}
.t-uvod .dalej {{ font-weight: 700; font-size: 26px; margin-top: auto; padding-left: 8px; }}

/* zoznam */
.t-zoznam h1 {{ margin-top: 6px; }}
.polozky {{ margin-top: auto; margin-bottom: auto; display: flex; flex-direction: column; gap: 90px; padding-top: 30px; }}
.polozka {{ display: flex; align-items: stretch; }}
.polozka .c {{ flex: none; width: 152px; color: {ZLTA}; font-weight: 700; font-size: 80px; line-height: 1; padding-top: 2px; }}
.polozka .ciara {{ flex: none; width: 2px; background: {ZLTA}; margin-right: 40px; }}
.polozka .nazov {{ font-weight: 700; font-size: 36px; text-transform: uppercase; letter-spacing: .5px; margin-top: 8px; }}
.polozka .txt {{ font-size: 34px; line-height: 1.38; margin-top: 10px; max-width: 470px; }}
.t-zoznam .poznamka {{ font-size: 34px; margin-top: 30px; }}

/* kroky */
.kroky {{ margin-top: auto; margin-bottom: auto; display: flex; flex-direction: column; gap: 30px; padding-top: 24px; }}
.krok {{ display: flex; min-height: 144px; }}
.krok .c {{ flex: none; width: 113px; background: {ZLTA}; color: {ZELENA}; font-weight: 700; font-size: 52px; display: flex; align-items: center; padding-left: 34px; }}
.krok .box {{ flex: 1; background: {KREM}; color: {ZELENA}; padding: 18px 34px; display: flex; flex-direction: column; justify-content: center; }}
.krok .nazov {{ font-weight: 700; font-size: 40px; line-height: 1.2; }}
.krok .txt {{ font-size: 30px; margin-top: 10px; line-height: 1.3; }}

/* blok */
.t-blok h1 {{ font-size: 78px; line-height: 1.33; }}
.t-blok .zblok {{ background: {ZLTA}; color: {ZELENA}; font-weight: 700; font-size: 88px; line-height: 1.04; text-transform: uppercase;
  padding: 44px 34px 46px; margin-top: auto; }}
.t-blok .tucny {{ font-weight: 700; font-size: 38px; line-height: 1.44; margin-top: 50px; }}
.t-blok .maly {{ font-size: 32px; line-height: 1.5; margin-top: 50px; }}
.t-blok .spacer {{ margin-top: auto; }}

/* text */
.t-text .odseky {{ margin-top: 54px; display: flex; flex-direction: column; gap: 30px; }}
.t-text .odseky p {{ font-size: 38px; line-height: 1.42; }}

/* koniec */
.t-koniec .vnutro {{ flex: 1; padding: 50px 72px 0; display: flex; flex-direction: column; }}
.t-koniec h1 {{ font-size: 84px; line-height: 1.24; }}
.t-koniec .uvod {{ font-size: 36px; margin-top: auto; }}
.t-koniec .zbox {{ background: {ZLTA}; font-weight: 700; font-size: 74px; margin: 50px -10px 0; padding: 14px 18px 18px; }}
.t-koniec .txt {{ font-size: 36px; line-height: 1.65; margin-top: 98px; }}
.t-koniec .gbox {{ background: {ZELENA}; color: {KREM}; font-weight: 700; font-size: 66px; margin: 34px -10px 0; padding: 14px 42px 22px; }}

/* fotka */
.t-fotka {{ padding: 0; }}
.t-fotka .maly {{ position: absolute; left: 72px; top: 104px; font-size: 38px; }}
.t-fotka .velke {{ position: absolute; left: 64px; top: 200px; font-weight: 700; font-size: 236px; line-height: 1; letter-spacing: 4px; text-transform: uppercase; z-index: 3; }}
.t-fotka .kruh {{ position: absolute; left: 231px; top: 395px; width: 770px; height: 770px; border-radius: 50%; border: 6px solid {ZLTA}; padding: 14px; z-index: 1; }}
.t-fotka .kruh div {{ width: 100%; height: 100%; border-radius: 50%; background-size: cover; background-position: center; }}
.t-fotka .pas {{ position: absolute; left: -40px; width: 1200px; top: 880px; height: 220px; background: {ZLTA}; transform: rotate(-3deg); z-index: 2;
  display: flex; align-items: center; padding-left: 108px; }}
.t-fotka .pas span {{ font-weight: 700; font-size: 170px; letter-spacing: 3px; text-transform: uppercase; transform: rotate(3deg); margin-top: 26px; }}
.t-fotka .spodna {{ position: absolute; left: 76px; bottom: 66px; display: flex; align-items: center; gap: 44px; z-index: 3; }}
.t-fotka .spodna .logo {{ width: 96px; height: 64px; }}
.t-fotka .spodna span {{ font-weight: 700; font-size: 36px; padding-top: 10px; }}

/* story – viac vzduchu hore/dole kvôli rozhraniu Instagramu */
.story .hlavicka {{ height: 330px; padding-top: 150px; }}
.story .pata {{ height: 300px; padding-bottom: 140px; }}
.story .t-uvod .spodok {{ height: 560px; }}
.story .t-uvod .riadok {{ font-size: 104px; }}
.story .t-uvod .pod {{ font-size: 44px; }}
.story .t-uvod .velke {{ font-size: 200px; }}
.story .t-uvod .velke-popis {{ font-size: 44px; }}
.story .t-uvod .dalej {{ font-size: 34px; }}
.t-uvod .spodok {{ position: relative; }}
.t-uvod .spodok .ikona {{ top: 40px; right: 72px; bottom: auto; width: 170px; height: 170px; }}
.story .panel {{ padding: 70px 72px 80px; }}
.story .stitok {{ font-size: 36px; margin-bottom: 34px; }}
.story h1 {{ font-size: 104px; line-height: 1.18; }}
.story h1.zlty {{ font-size: 120px; }}
.story h2.podnadpis {{ font-size: 92px; }}
.story .t-text .odseky p {{ font-size: 50px; }}
.story .t-blok .zblok {{ font-size: 120px; margin-top: 70px; }}
.story .t-blok .tucny {{ font-size: 48px; }}
.story .t-blok .maly {{ font-size: 40px; }}
.story .t-koniec h1 {{ font-size: 104px; }}
.story .t-koniec .uvod {{ font-size: 46px; }}
.story .t-koniec .zbox {{ font-size: 84px; }}
.story .t-koniec .txt {{ font-size: 46px; margin-top: 60px; }}
.story .t-koniec .gbox {{ font-size: 72px; }}
.story .krok .nazov {{ font-size: 48px; }}
.story .krok .txt {{ font-size: 36px; }}
.story .polozka .nazov {{ font-size: 44px; }}
.story .polozka .txt {{ font-size: 40px; max-width: 600px; }}
.nalepka {{ flex: none; height: 360px; }}
.story .ikona.pravo-hore {{ top: 400px; }}
/* ikona / emoji – malý vkusný doplnok */
.ikona {{ position: absolute; width: 150px; height: 150px; z-index: 4; }}
.ikona.emoji {{ font-family: 'Noto Color Emoji', sans-serif; font-size: 120px; line-height: 150px; text-align: center; }}
.ikona.pravo-hore {{ right: 72px; top: 222px; }}
.ikona.pravo-dole {{ right: 72px; bottom: 200px; }}
.ikona.pri-nadpise {{ position: static; display: inline-block; width: 1em; height: 1em; vertical-align: -0.12em; margin-left: .2em; }}
.ikona.emoji.pri-nadpise {{ font-size: .9em; line-height: 1; width: auto; height: auto; }}
.t-uvod .ikona.pravo-dole {{ bottom: 220px; right: 80px; width: 180px; height: 180px; }}
.story .ikona.pravo-hore {{ top: 380px; }}
.story .ikona.pravo-dole {{ bottom: 360px; }}
"""


def hlavicka() -> str:
    return f'<div class="hlavicka">{LOGO}<span>VYŠĽAP SI MEDAILU</span></div>'


def pata(i: int, n: int) -> str:
    str_ = f'<span class="str">{i + 1:02d} / {n:02d}</span>' if n > 1 else "<span></span>"
    return f'<div class="pata"><span>{WEB}</span>{str_}</div>'


def stitok(s: dict) -> str:
    if not s.get("stitok"):
        return ""
    t = html.escape(s["stitok"]).replace(" / ", "  /  ")
    return f'<div class="stitok">{t}</div>'


def slide_html(s: dict, i: int, n: int, base: Path) -> str:
    typ = s["typ"]
    nal = '<div class="nalepka"></div>' if s.get("nalepka") else ""
    if typ == "uvod":
        riadky = s["riadky"]
        zv = s.get("zvyraznit", len(riadky) - 1)
        r = "".join(f'<div class="riadok{" zlty" if k == zv else ""}">{md(x)}</div>' for k, x in enumerate(riadky))
        pod = f'<div class="pod">{md(s["podnadpis"])}</div>' if s.get("podnadpis") else ""
        velke = f'<div class="velke">{md(s["velke"])}</div>' if s.get("velke") else ""
        vp = f'<div class="velke-popis">{md(s["velke_popis"])}</div>' if s.get("velke_popis") else ""
        dalej = s.get("dalej", "Posuň ďalej →" if n > 1 else "")
        d = f'<div class="dalej">{md(dalej)}</div>' if dalej else ""
        # ikona pri úvode patrí do zeleného pásu vpravo hore, aby nikdy neprekryla text
        ik_uvod = ""
        if s.get("ikona") and s.get("ikona_pozicia", "pravo-dole") == "pravo-dole":
            ik_uvod = ikona_html(s["ikona"], "v-pase", True)
            s = {**s, "ikona": ""}
        telo = f'{hlavicka()}<div class="vrch krem">{r}{pod}</div><div class="spodok">{velke}{vp}{d}{ik_uvod}</div>'
    elif typ == "zoznam":
        pol = "".join(
            f'<div class="polozka"><div class="c">{k + 1:02d}</div><div class="ciara"></div>'
            f'<div><div class="nazov">{md(p["nazov"])}</div><div class="txt">{md(p.get("text", ""))}</div></div></div>'
            for k, p in enumerate(s["polozky"]))
        pozn = f'<div class="poznamka">{md(s["poznamka"])}</div>' if s.get("poznamka") else ""
        telo = f'{hlavicka()}<div class="panel">{stitok(s)}<h1>{md(s["nadpis"])}</h1><div class="polozky">{pol}</div>{pozn}</div>'
    elif typ == "kroky":
        kr = "".join(
            f'<div class="krok"><div class="c">{k + 1}</div><div class="box"><div class="nazov">{md(p["nazov"])}</div>'
            + (f'<div class="txt">{md(p["text"])}</div>' if p.get("text") else "") + "</div></div>"
            for k, p in enumerate(s["kroky"]))
        pod = f'<h2 class="podnadpis">{md(s["podnadpis"])}</h2>' if s.get("podnadpis") else ""
        telo = f'{hlavicka()}<div class="panel">{stitok(s)}<h1 class="zlty">{md(s["nadpis"])}</h1>{pod}<div class="kroky">{kr}</div></div>'
    elif typ == "blok":
        tucny = f'<div class="tucny">{md(s["text"])}</div>' if s.get("text") else ""
        maly = f'<div class="maly">{md(s["maly"])}</div>' if s.get("maly") else ""
        telo = (f'{hlavicka()}<div class="panel">{stitok(s)}<h1>{md(s["nadpis"])}</h1>'
                f'<div class="zblok">{md(s["blok"])}</div>{tucny}{maly}{nal}<div class="spacer"></div></div>')
    elif typ == "text":
        ods = s.get("text", [])
        ods = [ods] if isinstance(ods, str) else ods
        p = "".join(f"<p>{md(o)}</p>" for o in ods)
        telo = f'{hlavicka()}<div class="panel">{stitok(s)}<h1>{md(s["nadpis"])}</h1><div class="odseky">{p}</div>{nal}</div>'
    elif typ == "koniec":
        uvod = f'<div class="uvod">{md(s["uvod"])}</div>' if s.get("uvod") else '<div class="uvod"></div>'
        zb = f'<div class="zbox">{md(s["zvyraznenie"])}</div>' if s.get("zvyraznenie") else ""
        txt = f'<div class="txt">{md(s["text"])}</div>' if s.get("text") else ""
        gb = f'<div class="gbox">{md(s.get("odkaz", WEB))}</div>'
        telo = f'{hlavicka()}<div class="vnutro krem"><h1>{md(s["nadpis"])}</h1>{uvod}{zb}{txt}{nal}{gb}</div>'
    elif typ == "fotka":
        maly = f'<div class="maly">{md(s["maly"])}</div>' if s.get("maly") else ""
        velke = f'<div class="velke">{md(s["velke"])}</div>' if s.get("velke") else ""
        pas = f'<div class="pas"><span>{md(s["pas"])}</span></div>' if s.get("pas") else ""
        kruh = f'<div class="kruh"><div style="background-image:url(\'{img_src(s["obrazok"], base)}\')"></div></div>'
        sp = f'<div class="spodna">{LOGO}<span>{WEB}</span></div>'
        return f'<section class="s t-fotka">{maly}{velke}{kruh}{pas}{sp}</section>'
    else:
        raise ValueError(f"Neznámy typ slidu: {typ}")
    pozicia = s.get("ikona_pozicia", "pravo-dole" if typ == "uvod" else "pravo-hore")
    na_zelenej = not (typ == "koniec" or (typ == "uvod" and pozicia == "pravo-hore"))
    ik = ikona_html(s.get("ikona", ""), pozicia, na_zelenej)
    return f'<section class="s t-{typ}">{telo}{pata(i, n)}{ik}</section>'


def render(spec_path: str, out_dir: str) -> list:
    from playwright.sync_api import sync_playwright
    spec_file = Path(spec_path).resolve()
    spec = json.loads(spec_file.read_text(encoding="utf-8"))
    fmt = spec.get("format", "carousel")
    w, h = (1080, 1920) if fmt == "story" else (1080, 1350)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    slides = spec["slides"]
    n = len(slides) if fmt == "carousel" else 1
    vystup = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
        for i, s in enumerate(slides):
            ii = i if fmt == "carousel" else 0
            doc = (f'<!doctype html><html><head><meta charset="utf-8"><style>:root{{--w:{w}px;--h:{h}px}}{CSS}</style></head>'
                   f'<body class="{"story" if fmt == "story" else ""}">{slide_html(s, ii, n, spec_file.parent)}</body></html>')
            pg.set_content(doc, wait_until="load")
            pg.evaluate("document.fonts.ready.then(() => document.fonts.size)")
            pg.wait_for_timeout(120)
            # kontrola pretečenia: text nesmie ísť mimo slidu ani mimo panelu
            pretek = pg.evaluate("""() => {
                const bad = [];
                document.querySelectorAll('.panel, .vrch, .vnutro, .spodok').forEach(el => {
                    if (el.scrollHeight > el.clientHeight + 2) bad.push(el.className);
                });
                return bad;
            }""")
            if pretek:
                print(f"POZOR slide {i + 1}: text pretiekol v {pretek} – skráť text", file=sys.stderr)
            f = out / f"{i + 1:02d}.png"
            pg.screenshot(path=str(f), clip={"x": 0, "y": 0, "width": w, "height": h})
            vystup.append(str(f))
        b.close()
    vystup.append(nahlad(vystup, out / "nahlad.png"))
    return vystup


def nahlad(subory: list, ciel: Path) -> str:
    """Kontaktný list všetkých slidov vedľa seba – na rýchle schválenie."""
    from PIL import Image
    ims = [Image.open(f) for f in subory]
    sirka = 360
    vyska = round(ims[0].height * sirka / ims[0].width)
    medz = 24
    list_ = Image.new("RGB", (len(ims) * sirka + (len(ims) - 1) * medz, vyska), "white")
    for k, im in enumerate(ims):
        list_.paste(im.convert("RGB").resize((sirka, vyska)), (k * (sirka + medz), 0))
    list_.save(ciel)
    return str(ciel)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    for f in render(sys.argv[1], sys.argv[2]):
        print(f)
