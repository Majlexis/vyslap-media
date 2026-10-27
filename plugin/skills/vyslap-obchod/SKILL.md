---
name: vyslap-obchod
description: Obchodný prehľad pre Vyšľap si medailu – nové objednávky a tržby z webu, strážca medailí (predaje vs. objednané medaily a termín objednávky u výrobcu) a pripomienka odoslania splnených výziev. Použiť v dennom a týždennom súhrne a keď sa Alex pýta na predaje, objednávky, medaily alebo odosielanie.
---

# Vyšľap si medailu – obchod (objednávky, medaily, odosielanie)

## 0. ZLATÉ PRAVIDLÁ
- Databázu webu (Supabase projekt `ueiaaxutowouiepzjhag`) **iba čítaš**: len `SELECT`. Nikdy `INSERT/UPDATE/DELETE`, nič nemeníš ani nemažeš.
- Do správy **nikdy** nedávaj mená, e-maily, adresy ani Z-BOXy zákazníkov – len počty, sumy a názvy výziev.
- Počítaj len ostré objednávky: zaplatené od **15. 11. 2026** a bez testovacích e-mailov správcu (`alisalapa5@gmail.com`, `info@vyslapsimedailu.sk`).
- Pred 15. 11. 2026 obchodnú časť vynechaj (napíš len „predaj štartuje 15. 11.“).
- Nástroj: `execute_sql` (Supabase; načítaj cez ToolSearch „supabase execute_sql“). Názvy výziev ber z tabuľky `vyzvy` (`data->>'nazov'`).

Spoločný filter (vlož do každého dotazu):
```sql
p.zaplatene is not null
and p.zaplatene >= '2026-11-15'
and lower(coalesce(p.kupujuci_email, p.email)) not in ('alisalapa5@gmail.com','info@vyslapsimedailu.sk')
```
Stavy v `prihlasky.stav`: `zaplatene` → `splnene` (čaká na odoslanie medaily) → `odoslane`. Jeden riadok = jedna výzva (Valentínska dvojica = 1 riadok za pár). `suma_centy` = cena výzvy v centoch, `objednavka_id` = jeden košík, `kupujuci_email` vyplnený = darček.

## 1. Nové objednávky (denný súhrn – za včerajšok)
```sql
select v.data->>'nazov' as vyzva, count(*) as ks,
       count(*) filter (where p.kupujuci_email is not null) as darceky,
       round(sum(p.suma_centy)/100.0, 2) as eur, count(distinct p.objednavka_id) as kosiky
from prihlasky p join vyzvy v on v.slug = p.vyzva
where <spoločný filter>
  and p.zaplatene >= (date_trunc('day', now() at time zone 'Europe/Bratislava') - interval '1 day') at time zone 'Europe/Bratislava'
  and p.zaplatene <  date_trunc('day', now() at time zone 'Europe/Bratislava') at time zone 'Europe/Bratislava'
group by 1 order by 2 desc;
```
K tomu jeden riadok „od štartu predaja“: rovnaký dotaz bez dvoch podmienok na deň (spolu ks, €, darčeky).

## 2. Odoslanie medailí (denne)
```sql
select v.data->>'nazov' as vyzva, count(*) as caka,
       min(p.splnene) as najstarsie_splnene
from prihlasky p join vyzvy v on v.slug = p.vyzva
where <spoločný filter> and p.stav = 'splnene'
group by 1;
```
- Ak niečo čaká: „📦 X medailí čaká na odoslanie (najstaršia od <dátum>)“.
- Sľub zákazníkom: medaila **spravidla do 4 týždňov od splnenia**. Ak najstaršie čakanie > 14 dní → ⚠️, > 21 dní → 🔴 urgentné.
- Odosiela sa v administrácii webu (/admin → Vytvoriť zásielku v Packete).

## 3. Strážca medailí (týždenne + denne pri ⚠️)
1. Predané ks na výzvu: dotaz z bodu 1 bez denných podmienok, group by `p.vyzva`.
2. Objednané medaily: tabuľka v `medaily.md` (stĺpec „Objednané ks“).
3. Pre každú výzvu s predajmi vypočítaj:
   - **chýba** = predané − objednané (ak > 0 → treba doobjednať),
   - **rezerva** = objednané − predané,
   - **posledný deň objednávky u výrobcu** = deň, keď prví ľudia môžu výzvu splniť (pri Novoročných 100: najskôr cca 5. 1. 2027; pri Valentínskej: 7. 2. 2027; pri celoročných: 1. 1. 2027) **mínus dodacia lehota** výrobcu z `medaily.md` (ak nie je vyplnená, počítaj 4 týždne a napíš, že je to odhad).
4. Do správy:
   - 🔴 ak chýba medaila a do posledného dňa objednávky je ≤ 14 dní,
   - ⚠️ ak chýba medaila alebo rezerva < 10 % predajov,
   - ✅ inak (stačí jeden riadok „medaily v poriadku“).
5. Pri odhade počtu na objednávku zohľadni, že predaj ešte beží (Novoročných 100 do 15. 1., Valentínska do 14. 2.): odporuč objednať predané + rezervu podľa tempa predaja za posledných 7 dní × zostávajúce dni predaja a pripomeň minimálny odber výrobcu.
6. Keď Alex povie, že objednal/dostal medaily, aktualizuj `medaily.md` v repe (commit + push).

## 4. Týždenný prehľad (nedeľa)
- predaje za týždeň a od štartu: ks, €, darčeky, top výzva,
- porovnanie s minulým týždňom (↑/↓),
- strážca medailí (bod 3) celý,
- čakajúce odoslania (bod 2),
- ak bežala reklama: € reklamy / predané ks za týždeň = orientačná cena za predaj (porovnaj s maržou ~9 € na výzvu).
