Pridaj na web meranie objednávok do Google Analytics 4 (udalosť `purchase`), aby som videl, koľko predajov priniesla reklama a odkiaľ (UTM). Komunikuj so mnou po slovensky a jednoducho, pracuj podľa CLAUDE.md.

AKO TO DNES FUNGUJE
- Platba ide cez Stripe Checkout (`lib/platby.ts`, funkcia `vytvorPlatbu`, `success_url` = `/ucet/platba?session_id={CHECKOUT_SESSION_ID}`).
- `app/ucet/platba/page.tsx` je serverová stránka: načíta session zo Stripe, ak `payment_status === 'paid'`, zavolá `potvrdPlatbu` a presmeruje na `/ucet?platba=ok` (inak `/ucet?platba=spracuva`).
- GA4 sa načítava v `components/Analytika.tsx` s Google Consent Mode (`analytics_storage` je „denied“, kým návštevník neklikne Súhlasím). `window.gtag` je globálne dostupné.

ČO TREBA SPRAVIŤ
1. V `app/ucet/platba/page.tsx`: keď je platba zaplatená, presmeruj na `/ucet?platba=ok&nakup=<session_id>` (session_id je od Stripe, nie je to citlivý údaj).
2. Na stránke `/ucet` (alebo v novom klientskom komponente, napr. `components/MeranieNakupu.tsx`, vloženom do `/ucet`): keď je v adrese `platba=ok` a `nakup`, zisti údaje o nákupe na serveri (serverová akcia alebo API route, ktorá cez `stripe().checkout.sessions.retrieve(id, { expand: ['line_items'] })` overí, že session patrí prihlásenému používateľovi a je zaplatená) a v prehliadači pošli:
   gtag('event', 'purchase', {
     transaction_id: <session_id alebo objednavka_id z metadata>,
     value: <amount_total / 100>,
     currency: 'EUR',
     shipping: <poštovné v eurách>,
     items: [ { item_id: <slug výzvy>, item_name: <názov výzvy>, price: <cena>, quantity: 1, item_category: 'výzva' alebo 'darček' } ]
   })
3. Ochrana pred duplicitou: udalosť pošli len raz na jednu objednávku (napr. ulož `transaction_id` do localStorage v try/catch) a po odoslaní odstráň `nakup` z adresy cez `router.replace('/ucet?platba=ok')`.
4. Ak `window.gtag` ešte nie je načítané, chvíľu počkaj (napr. pár pokusov po 500 ms); ak GA nie je nastavené (`NEXT_PUBLIC_GA_ID` chýba), nerob nič a nič nepokaz.
5. Nemeň nič na samotnej platbe, potvrdzovaní objednávok, e-mailoch ani cookie lište. Žiadne nové cookies. Žiadne osobné údaje (e-mail, meno, adresa) do GA neposielaj.
6. Voliteľne: pri kliknutí na „Pridať do košíka“ pošli `add_to_cart` a pri presmerovaní na Stripe `begin_checkout` (s rovnakými položkami), aby som videl, kde ľudia odpadajú.

KONTROLA
- `npx tsc --noEmit` a `npx next build` musia prejsť.
- Vysvetli mi krok za krokom, ako to overím: testovacia platba kartou 4242 4242 4242 4242, potom v GA4 Admin → DebugView alebo Reports → Realtime → udalosť `purchase` s hodnotou.
- Potom commit po slovensky („Meranie objednávok v GA4“) a push.

Pripomienka pre mňa: v GA4 si potom v Admin → Events označ `purchase` ako kľúčovú udalosť (Key event), ak sa tak neoznačí sama.
