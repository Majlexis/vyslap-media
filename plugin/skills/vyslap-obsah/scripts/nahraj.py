#!/usr/bin/env python3
"""Nahrá hotové médiá do verejného repa Majlexis/vyslap-media a vypíše verejné odkazy pre Metricool.

Použitie:
    python3 nahraj.py <nazov-postu> subor1.png [subor2.png ...]
    napr. python3 nahraj.py 2026-11-03-vyhovorka vystup/01.png vystup/02.png

Súbory sa uložia do  <rok>/<mesiac>/<nazov-postu>/  a skript vypíše JSON:
    {"media": ["https://raw.githubusercontent.com/..."], "nahlad": "..."}
PNG sa pred nahraním skonvertujú na JPG (menšie, Metricool/IG ich berú bez problémov). MP4 a JPG idú bez zmeny.

Repo musí byť naklonované v REPO (ak nie je, skript ho naklonuje).
"""
import json, re, subprocess, sys, time, urllib.request
from pathlib import Path

REPO_URL = "https://github.com/Majlexis/vyslap-media"
REPO = Path("/home/claude/vyslap-media")
RAW = "https://raw.githubusercontent.com/Majlexis/vyslap-media/main/"


def git(*args, check=True):
    return subprocess.run(["git", "-C", str(REPO), *args], check=check, capture_output=True, text=True)


def priprav_repo():
    if not (REPO / ".git").exists():
        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, str(REPO)], check=True)
    git("fetch", "origin", "main")
    git("reset", "--hard", "origin/main")
    git("config", "user.name", "Vyšľap si medailu – Claude")
    git("config", "user.email", "claude@vyslapsimedailu.sk")


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    nazov = re.sub(r"[^a-z0-9-]+", "-", sys.argv[1].lower()).strip("-")
    subory = [Path(p) for p in sys.argv[2:]]
    priprav_repo()
    rok, mes = time.strftime("%Y"), time.strftime("%m")
    ciel = REPO / rok / mes / nazov
    ciel.mkdir(parents=True, exist_ok=True)
    rel = []
    for k, f in enumerate(subory, 1):
        if f.suffix.lower() == ".png":
            from PIL import Image
            out = ciel / f"{k:02d}.jpg"
            Image.open(f).convert("RGB").save(out, quality=92)
        else:
            out = ciel / f"{k:02d}{f.suffix.lower()}"
            out.write_bytes(f.read_bytes())
        rel.append(out.relative_to(REPO).as_posix())
    git("add", ".")
    if git("diff", "--cached", "--quiet", check=False).returncode != 0:
        git("commit", "-m", f"Médiá: {nazov}")
        r = git("push", "origin", "HEAD:main", check=False)
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr); sys.exit(2)
    urls = [RAW + p for p in rel]
    # počkať, kým budú odkazy verejne dostupné (raw cache)
    for u in urls:
        for _ in range(20):
            try:
                with urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=10) as resp:
                    if resp.status == 200:
                        break
            except Exception:
                pass
            time.sleep(3)
        else:
            print(f"POZOR: {u} zatiaľ nie je dostupný", file=sys.stderr)
    print(json.dumps({"media": urls}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
