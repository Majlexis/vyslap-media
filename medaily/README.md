# Medaily a stuhy

Každá výzva má svoj priečinok:

| Súbor | Čo to je |
| --- | --- |
| `medaila.jpg` | vizualizácia medaily (rovnaká ako na webe) |
| `stuha-nahlad.png` | náhľad stuhy – rozložená stuha, detail, farby |
| `stuha-tlac.png`, `stuha-tlac.svg` | samotná stuha pre výrobcu (25 × 900 mm, rozmer upresní výrobca) |

| Výzva | Medaila | Stuha |
| --- | --- | --- |
| Novoročných 100 | ✅ finálna | ✅ finálna |
| Valentínska dvojica | ✅ finálna | ✅ finálna (2 ks na pár) |
| Hradná výzva 2027 | ✅ | – |
| Tatranské plesá 2027 | ✅ (dočasná, nová v návrhu) | ✅ finálna |
| Cesta SNP 2027 | ✅ | – |
| Východ slnka na vrchole 2027 | ✅ | – |
| 12 vrcholov za rok 2027 | ✅ | – |
| **Tatry 2027** (prémiová, 5 medailí) | | |
| ↳ Rysy | ✅ finálna | ✅ finálna |
| ↳ Kriváň | ✅ finálna | ✅ finálna |
| ↳ Slavkovský štít | ✅ finálna | ✅ finálna |
| ↳ Východná Vysoká | ✅ finálna | ✅ finálna |
| ↳ Kôprovský štít | ✅ finálna | ✅ finálna |

Tatry 2027 majú podpriečinok pre každý vrchol v `tatry-2027/`. Stuhy sú variant A „Farebná topografia“ (farba stuhy podľa medaily, vrstevnice, oranžové slnko s výškou) – skript `_nastroje/tatry_stuhy.py tatry finalne`.

Medaily sú vizualizácie, skutočná medaila sa môže v detailoch líšiť.

Stuhy sa generujú skriptom `_nastroje/stuhy.py` (`python3 stuhy.py vystupny_priecinok`, potrebuje `cairosvg`).
