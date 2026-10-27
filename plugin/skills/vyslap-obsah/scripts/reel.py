#!/usr/bin/env python3
"""Vyšľap si medailu – animovaný reel 1080x1920 v štýle „Krok za krokom“.

Použitie:
    python3 reel.py spec.json vystup.mp4

spec.json (šablóna "cesta"):
{
  "nadpis": "100 km za január.",          # hore, celý čas
  "pocitadlo": {"od": 0, "do": 100, "jednotka": "km"},   # voliteľné – rastie s cestou
  "podnadpis": "Svojím tempom.",          # objaví sa ku koncu kreslenia (žltý)
  "zaver": ["Novoročných 100.", "Predaj od 15. novembra."],   # krémový záver s logom
  "trvanie": 9                            # sekundy (7–15)
}
Výstup: MP4 H.264, 30 fps, bez zvuku (hudbu Alex pridá v Instagrame) + obal.jpg (titulná snímka).
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import CSS as _CSS_UNUSED, LOGO, KREM, ZELENA, ZLTA, WEB, FONTS, _b64, md  # noqa: E402

FPS = 30

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: 'VSM'; src: url('{reg}'); font-weight: 400; }}
@font-face {{ font-family: 'VSM'; src: url('{bold}'); font-weight: 700; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1920px; overflow:hidden; font-family:'VSM',Arial,sans-serif; }}
.scena {{ position:absolute; inset:0; }}
#zelena {{ background:{Z}; color:{K}; }}
#krem {{ background:{K}; color:{Z}; opacity:0; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }}
.nadpis {{ position:absolute; top:300px; left:0; right:0; text-align:center; font-weight:700; font-size:84px; letter-spacing:-.5px; }}
.pocet {{ position:absolute; top:430px; left:0; right:0; text-align:center; font-weight:700; font-size:150px; color:{Y}; font-variant-numeric:tabular-nums; }}
.pocet small {{ font-size:70px; margin-left:12px; }}
svg.cesta {{ position:absolute; left:90px; top:660px; width:900px; height:820px; overflow:visible; }}
.pod {{ position:absolute; top:1540px; left:0; right:0; text-align:center; font-weight:700; font-size:70px; color:{Y}; }}
.web {{ position:absolute; bottom:200px; left:0; right:0; text-align:center; font-weight:700; font-size:40px; }}
#krem .logo {{ width:300px; height:208px; }}
#krem .r {{ font-weight:700; font-size:80px; line-height:1.25; margin-top:10px; }}
#krem .r1 {{ margin-top:110px; }}
#krem .web {{ color:{Z}; }}
</style></head><body>
<div class="scena" id="zelena">
  <div class="nadpis" id="nadpis">{nadpis}</div>
  {pocet}
  <svg class="cesta" viewBox="0 0 900 820">
    <path id="p" d="M40 760 C 40 640, 200 640, 430 640 S 820 600, 800 470 S 520 380, 300 360 S 40 270, 120 150 S 520 120, 700 110 S 840 60, 860 40"
      fill="none" stroke="{Y}" stroke-width="20" stroke-linecap="round"/>
    <circle id="bod" r="24" fill="{K}" stroke="{Z}" stroke-width="0"/>
    <circle id="bod2" r="11" fill="{Z}"/>
  </svg>
  <div class="pod" id="pod">{pod}</div>
  <div class="web">{web}</div>
</div>
<div class="scena" id="krem">
  {logo}
  {zaver}
  <div class="web">{web}</div>
</div>
<script>
const T = {T};
const p = document.getElementById('p'), L = p.getTotalLength();
p.style.strokeDasharray = L;
const ease = x => x < .5 ? 4*x*x*x : 1 - Math.pow(-2*x + 2, 3) / 2;
const clamp = (x) => Math.max(0, Math.min(1, x));
const lin = (t, a, b) => clamp((t - a) / (b - a));
window.frame = (t) => {{
  const kresli0 = 0.7, kresli1 = T - 3.6, prechod = T - 2.6;
  document.getElementById('nadpis').style.opacity = lin(t, 0, .5);
  document.getElementById('nadpis').style.transform = `translateY(${{(1 - ease(lin(t, 0, .5))) * 30}}px)`;
  const pr = ease(lin(t, kresli0, kresli1));
  p.style.strokeDashoffset = L * (1 - pr);
  const pt = p.getPointAtLength(L * pr);
  const koniec = lin(t, kresli1, kresli1 + .35);
  for (const id of ['bod', 'bod2']) {{ const c = document.getElementById(id); c.setAttribute('cx', pt.x); c.setAttribute('cy', pt.y); }}
  document.getElementById('bod').setAttribute('r', 24 + 14 * koniec);
  document.getElementById('bod2').style.opacity = 1 - koniec;
  const pc = document.getElementById('pocet');
  if (pc) {{ const v = {od} + ({do_} - {od}) * pr; pc.firstChild.nodeValue = Math.round(v); pc.style.opacity = lin(t, kresli0, kresli0 + .3); }}
  const pod = document.getElementById('pod');
  pod.style.opacity = lin(t, kresli1 - 1.0, kresli1 - .5);
  const k = document.getElementById('krem');
  k.style.opacity = lin(t, prechod, prechod + .35);
  const lg = k.querySelector('.logo');
  const s = ease(lin(t, prechod + .2, prechod + .8));
  lg.style.transform = `scale(${{.6 + .4 * s}})`; lg.style.opacity = s;
  k.querySelectorAll('.r').forEach((el, i) => {{ const a = lin(t, prechod + .6 + i * .3, prechod + 1.0 + i * .3); el.style.opacity = a; el.style.transform = `translateY(${{(1 - a) * 24}}px)`; }});
}};
</script></body></html>"""


def build_html(spec: dict) -> str:
    pc = spec.get("pocitadlo")
    pocet = (f'<div class="pocet" id="pocet">0<small>{md(pc.get("jednotka", ""))}</small></div>' if pc else "")
    zaver = "".join(f'<div class="r r{i + 1}">{md(r)}</div>' for i, r in enumerate(spec.get("zaver", [])))
    logo = LOGO.replace('class="logo"', 'class="logo"')
    return HTML.format(
        reg=_b64(FONTS / "LiberationSans-Regular.ttf", "font/ttf"),
        bold=_b64(FONTS / "LiberationSans-Bold.ttf", "font/ttf"),
        Z=ZELENA, K=KREM, Y=ZLTA, web=WEB, logo=logo,
        nadpis=md(spec.get("nadpis", "")), pod=md(spec.get("podnadpis", "")),
        pocet=pocet, zaver=zaver, T=float(spec.get("trvanie", 9)),
        od=pc.get("od", 0) if pc else 0, do_=pc.get("do", 0) if pc else 0,
    )


def render_reel(spec_path: str, out_path: str) -> str:
    from playwright.sync_api import sync_playwright
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    T = float(spec.get("trvanie", 9))
    n = int(round(T * FPS))
    tmp = Path(tempfile.mkdtemp(prefix="reel_"))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.set_content(build_html(spec), wait_until="load")
        pg.evaluate("document.fonts.ready.then(() => 1)")
        for i in range(n):
            pg.evaluate(f"window.frame({i / FPS})")
            pg.screenshot(path=str(tmp / f"f{i:04d}.jpg"), type="jpeg", quality=92)
        # obal: snímka s celou cestou pred prechodom
        pg.evaluate(f"window.frame({T - 2.8})")
        out = Path(out_path); out.parent.mkdir(parents=True, exist_ok=True)
        pg.screenshot(path=str(out.with_name(out.stem + "_obal.jpg")), type="jpeg", quality=92)
        b.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "f%04d.jpg"),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(out)], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    return str(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(1)
    print(render_reel(sys.argv[1], sys.argv[2]))
