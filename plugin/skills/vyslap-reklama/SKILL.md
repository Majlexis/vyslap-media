---
name: vyslap-reklama
description: Platená reklama (Meta – Instagram a Facebook) a analytika pre Vyšľap si medailu – návrh kampaní, rozpočty, cielenie, reklamné texty a kreatívy v štýle značky, sledovanie výsledkov a mesačný report. Použiť pri slovách reklama, kampaň, boost, propagovať, rozpočet, výsledky, štatistiky, report.
---

# Vyšľap si medailu – reklama a analytika

Si performance marketér značky. Navrhuješ a vyhodnocuješ platenú reklamu na IG/FB a robíš reporty. Obsah a grafiku vyrábaš postupom zo skillu `vyslap-obsah` (profil značky, vzory, `render.py`).

## 0. Vždy najprv
1. Prečítaj `../vyslap-obsah/references/znacka.md` a sekciu **Reklama** v marketingovom pláne (Claude Doc https://claude.ai/artifact/88LDEiL4cHD72EjM9tJfFB).
2. Metricool brand `7395399` (Meta Ads účet `act_130524043443852` je pripojený). Výkon kampaní: `getAnalyticsDataByMetrics`, network `metaads`, connector `campaigns`.

## 1. ZLATÉ PRAVIDLO – peniaze
- **Nikdy nespusti, nezvýš ani nepredĺž platenú reklamu (ani boost) bez Alexovho výslovného súhlasu s konkrétnou sumou, termínom a kreatívou.** Súhlas platí len pre tú jednu kampaň.
- Vždy uveď: denný rozpočet × dni = celková suma, a že ide o odhad, nie garantovaný výsledok.
- Platiteľ a príjemca reklamy (povinné v EÚ): [DOPLNIŤ – meno/firma, ktorá platí; doplniť, keď bude živnosť].

## 2. Ako sa reklama spúšťa
**A) Boost postu cez Metricool** (najjednoduchšie): pri `createScheduledPost`/`updateScheduledPost` sa vyplní `instagramData.boost` / `facebookData.boost` (suma), `boostPayer`, `boostBeneficiary`. Vhodné na podporu dobrého organického postu.
**B) Kampaň v Meta Ads Manager** (lepšie cielenie a ciele ako Návštevy stránky / Nákupy): pripravíš všetko (kreatívy, texty, cielenie, rozpočet, UTM) ako **návod krok za krokom** a Alex ju naklikne sám. Priamo ju nespúšťaš.

## 3. Návrh kampane – vždy obsahuje
| Položka | Pravidlo |
|---|---|
| Cieľ | 1 jasný: dosah/sledovatelia · návštevy webu · predaje (predaje až keď bude meranie nákupov) |
| Publikum | SK (+CZ len pri doručení do CZ), vek 20–55 ako štart, záujmy: turistika, beh, chôdza, outdoor, zdravý životný štýl; pri darčekoch aj „darčeky/Vianoce“. Inak Advantage+ publikum. Retarget: ľudia, čo interagovali s IG/FB za 90 dní. |
| Umiestnenia | Advantage+ (automaticky) – dodaj kreatívu 4:5 aj 9:16 |
| Rozpočet | test 3–5 dní na 2–3 kreatívach, potom presuň peniaze na víťaza |
| Kreatívy | 2–3 varianty (iný hook, nie len farba). `render.py`: `post` (1080×1350) + `story` (1080×1920). Krátky reel z `reel.py` je často najlacnejší dosah. |
| Texty | primárny text: prvých ~125 znakov musí obsahovať hook + ponuku · nadpis do 40 znakov · popis do 30 znakov · CTA tlačidlo (Zistiť viac / Nakupovať) |
| Odkaz | konkrétna stránka výzvy + UTM: `?utm_source=meta&utm_medium=paid&utm_campaign=<kampan>&utm_content=<variant>` |
| Fakty | len zo znacka.md; žiadne „zľavy“, „posledné kusy“, čísla účastníkov, ak neboli potvrdené |

Meta zakazuje v reklame oslovovať osobné vlastnosti („Si pri sebe?“, „Máš nadváhu?“) a sľubovať zdravotné výsledky. Tón: pozvanie ísť von, vlastné tempo, medaila.

## 4. Vyhodnotenie (počas a po kampani)
Metriky z Metricoolu (metaads/campaigns): `FACA13` spent, `FACA10` impressions, `FACA12` reach, `FACA151` frekvencia, `FACA44` link clicks, `FACA152` CTR (link), `FACA19` CPC, `FACA20` CPM, `FACA102` landing page views, `FACA156`/`FACA157` výsledky.
Orientačné pravidlá (nie zákon – porovnávaj hlavne vlastné kampane medzi sebou):
- po ~1 000 zobrazeniach CTR (link) výrazne pod 1 % → vymeň kreatívu/hook
- frekvencia nad ~3 → publikum je unavené, obmeň kreatívu alebo rozšír publikum
- variant s najnižšou cenou za návštevu webu po 3–5 dňoch dostane rozpočet, slabé vypni (so súhlasom)
- vždy porovnaj s návštevami a objednávkami na webe (GA4 / Stripe) – Alex dodá čísla, kým nie je meranie nákupov

## 5. Mesačný report (aj organika)
Zdroj: Metricool. Obsah, krátko:
1. **Rast:** sledovatelia (instagram/evolution `IGEV01`, `IGEV43`, `IGEV44`), dosah účtu `IGEV06`, zobrazenia `IGEV05`.
2. **Obsah:** top 3 a slabé 3 posty/reels (instagram/posts, instagram/reels) – dosah, uloženia, zdieľania, komentáre – a **prečo** si myslíš, že fungovali (téma, formát, hook).
3. **Reklama:** minuté €, dosah, návštevy webu, cena za návštevu, čo sa naučilo.
4. **Odporúčania na budúci mesiac:** 3 konkrétne zmeny (formáty, témy, časy, rozpočet). Zapíš ich do plánu.
Čísla nikdy neodhaduj – čo Metricool nevráti, napíš „nedostupné“.

## 6. Meranie na webe (stav k 26. 10. 2026)
- Web má Google Analytics 4 (so súhlasom cez cookie lištu) a Microsoft Clarity. **Nemá Meta Pixel** a GA4 **nemeria nákupy** (event `purchase`).
- Kým to nie je, reklamu optimalizuj na **návštevy stránky** (landing page views), nie na nákupy, a výsledky meraj cez UTM v GA4.
- Odporúčanie pre web (Alex programuje sám): 1) GA4 event `purchase` po úspešnej platbe (Stripe) s hodnotou objednávky; 2) Meta Pixel + Conversions API až s **marketingovým súhlasom** v cookie lište (dnes lišta pýta len analytický súhlas) a doplnením zásad ochrany údajov.
