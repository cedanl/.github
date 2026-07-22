# Login / registratie

Lees dit bestand zodra je zelf besluit een login-, registratie- of wachtwoord-vergeten-flow te ontwerpen. Het inlogproces is de voordeur van een product — vaak het allereerste of meest herhaalde contactmoment. Google-onderzoek laat zien dat gebruikers binnen 0,05 seconde een eerste indruk vormen; struikelt de gebruiker bij de voordeur, dan eindigt de reis voordat hij begint. Denk niet in één "loginpagina" maar in een compleet proces: inloggen, registreren, wachtwoord vergeten, validatie, MFA, foutafhandeling, accessibility en beveiliging horen er allemaal bij.

## Anatomie van het proces

Behandel login niet als één scherm maar als een keten van subprocessen (UX Collective): inloggen, registreren, wachtwoord/e-mail vergeten, front-end validatie, server-side foutafhandeling, multi-factor-authenticatie (MFA), MFA-probleemherstel, notificaties, e-mail/sms-communicatie, beveiliging en toegankelijkheid. Ontwerp én test elk onderdeel — een populaire consumenten-app kan tientallen schermvarianten hebben in deze keten.

## Verminder wat de gebruiker moet onthouden en typen

- **Bied social login aan** (Google/Apple/Microsoft) als snelle route naast het eigen account — dit scheelt een nieuw wachtwoord aanmaken en onthouden. Volg de merkrichtlijnen van de betreffende provider voor de knop (bv. Google's Sign-In-brandingregels) in plaats van een eigen variant te verzinnen.
- **Sla wachtwoordbevestiging over.** Twee keer hetzelfde wachtwoord laten typen verlaagt de conversie: bij een mismatch krijgt de gebruiker een foutmelding zonder te weten waar het misging. Gebruik in plaats daarvan een "toon wachtwoord"-toggle waarmee de gebruiker zijn eigen invoer kan controleren.
- **Gebruik e-mail in plaats van een zelfgekozen gebruikersnaam** als primaire identificatie — gebruikers onthouden een e-mailadres beter dan een verzonnen gebruikersnaam.
- **Sta wachtwoordmanagers en autogenereer-functies expliciet toe.** Zorg dat het wachtwoordveld herkenbaar is voor de OS-wachtwoordmanager (correct `type`/`autocomplete`-attribuut), en dat automatisch gegenereerde sterke wachtwoorden ook daadwerkelijk voldoen aan de eigen complexiteitseisen — anders wijst het systeem zijn eigen aangeboden wachtwoord af.
- **Communiceer wachtwoordeisen vooraf, niet pas na een mislukte poging.** Toon de vereisten (lengte, tekens) zichtbaar bij het veld voordat de gebruiker begint te typen.
- **Overweeg passphrases in plaats van complexe tekencombinaties.** "Blauwe-Ochtend-Koffie-Wolk!" is makkelijker te onthouden dan "B$1uC@ffe3!" en vaak sterker door de lengte. Verplicht niet automatisch hoofdletter+cijfer+symbool-combinaties als het doel simpelweg een lang, uniek wachtwoord is.

## Passwordless: OTP en passkeys als alternatief voor het wachtwoord

- **Overweeg OTP (one-time password) of magic link als alternatief voor een vast wachtwoord** (NN/g). Voordeel: de gebruiker hoeft niets te onthouden of te typen. Nadeel: wachttijd op de code, en bij e-mail een appwissel met spamfilter-risico — bij sms/inline-suggestie op het toetsenbord is de kost het laagst.
- **Bied bij OTP de keuze tussen e-mail en sms**, zeker bij responsive sites die zowel desktop als mobiel bedienen: niet elke gebruiker ontvangt sms op het apparaat waarmee hij inlogt.
- **Overweeg passkeys (biometrische authenticatie, Face ID/Touch ID/vingerafdruk) als sterkste optie.** Geen onthouden, typen, of kopiëren nodig; veiliger dan wachtwoorden omdat de sleutel versleuteld lokaal op het apparaat staat in plaats van bij elke website. Beperking: overstappen naar een ander apparaat/ecosysteem vraagt een QR-code-scan met het apparaat waar de passkey wel op staat.
- **Forceer passwordless nooit volledig — bied altijd een keuze.** Ook na het aanmaken van een passwordless account: laat de gebruiker later alsnog een wachtwoord kunnen toevoegen én biometrische authenticatie kunnen inschakelen. Niet iedereen wil OTP/passkeys, en gebruikers die wachtwoorden al opslaan in hun browser/telefoon hebben liever autofill.

## MFA: verplicht, maar met opties

- **Maak MFA waar mogelijk optioneel**, en bied meerdere methoden (authenticator-app, sms-code, e-mailcode, hardware-sleutel, backupcodes) — niet iedereen heeft een mobiele telefoon, en in sommige organisaties (overheid, financiële instellingen) zijn telefoons soms verboden.
- **Bied "onthoud dit apparaat"** om MFA op vertrouwde apparaten over te slaan bij volgend bezoek, zodat dagelijks inloggen niet telkens dezelfde stap herhaalt.
- **Gebruik adaptieve MFA op basis van risico-inschatting** waar mogelijk, in plaats van bij elke login onderscheidloos dezelfde extra stap te forceren.

## Registratie: minimaliseer en groepeer

- **Vraag alleen essentiële informatie.** Elk extra verplicht veld is een drempel — zie ook `inputfield.md` voor per-veldregels.
- **Gebruik een multi-stap (wizard) formulier bij veel velden**, met een duidelijk label per stap, soepele navigatie tussen stappen, en een overzicht vóór definitief versturen — dat maakt een grote hoeveelheid informatie behapbaar in plaats van overweldigend.
- **Toon links naar privacybeleid en gebruiksvoorwaarden direct op de login-/registratiepagina**, met uitleg hoe gegevens gebruikt en bewaard worden.

## Wachtwoord vergeten: houd de flow kort

Het standaard 9-staps-patroon (vergeten → link klikken → e-mail openen → reset-link volgen → nieuw wachtwoord invoeren tegen een complexe validatie → bevestigen → terug naar login → opnieuw inloggen → eventueel weer MFA) verliest onderweg gebruikers: naar schatting doorloopt 10% van actieve gebruikers maandelijks deze flow, en van hen haakt ~75% halverwege af (UX Collective, verwijzend naar onderzoek van Jared Spool).

- **Stuur de gebruiker na "wachtwoord vergeten" direct naar een pagina om een nieuw wachtwoord in te stellen** — zonder opnieuw beveiligingsvragen te moeten beantwoorden of de gebruikersnaam opnieuw in te voeren.
- **Gebruik duidelijke, geruststellende taal** in de reset-e-mail ("Geen zorgen, we helpen je verder — klik hier om een nieuw wachtwoord in te stellen").
- **Bied een zichtbare "hulp nodig?"-link** op de loginpagina, die naar FAQ, live chat of contactmogelijkheid leidt, zodat de gebruiker niet gefrustreerd afhaakt.

## Foutafhandeling: inline, specifiek, naast het veld

- **Valideer inline waar mogelijk** — zodra een veld is afgerond, direct een indicator tonen in plaats van pas na volledige submit (NN/g). Moet de server valideren, zorg dan dat de foutmelding duidelijk, uitvoerbaar en makkelijk vindbaar is na herladen.
- **Toon succesvolle invoer bij complexe velden** (bv. wachtwoordsterkte-indicator die meebeweegt tijdens typen, beschikbaarheidscheck van een gebruikersnaam) — dat voorkomt gis- en hercontrolegedrag. Gebruik succesindicatoren spaarzaam: niet nodig bij elk simpel verplicht veld.
- **Houd de foutmelding direct naast/onder het betreffende veld** — nooit alleen een samenvatting bovenaan de pagina. Een samenvatting mag als aanvulling, nooit als enige foutindicatie: de gebruiker moet dan zelf het veld gaan zoeken en de melding onthouden tijdens het corrigeren.
- **Gebruik kleur mét icoon**, nooit kleur alleen — rood/oranje voor fout, groen/blauw voor succes, met voldoende contrast t.o.v. de rest van het formulier. Subtiele animatie op het icoon mag de aandacht trekken, maar animeer nooit de teksten zelf (leesbaarheid).
- **Gebruik modals/bevestigingsdialogen spaarzaam bij fouten** — ze onderbreken en verhogen cognitieve belasting doordat de gebruiker de instructie moet onthouden na het sluiten. Alleen geschikt bij simpele meldingen of wanneer doorgaan zonder correctie ook een optie is.
- **Valideer nooit voordat de gebruiker klaar is met typen in een veld.** Een foutmelding tonen terwijl de gebruiker nog bezig is, voelt bestraffend en voorbarig.
- **Gebruik geen tooltips als enige foutindicatie.** Alert-iconen zijn makkelijk over het hoofd te zien, vragen een extra hover/focus-actie, en gebruikers realiseren zich vaak niet dat er meer info achter schuilgaat.
- **Bied extra hulp bij herhaalde fouten** (3× of vaker dezelfde fout in één sessie) — dat wijst op een dieper ontwerpprobleem, niet op onoplettendheid van de gebruiker. Overweeg een directe link naar support.

## Toegankelijkheid

- **Contrast**: voldoende contrast tussen tekst/velden en achtergrond, in zowel licht- als donker-thema — verifieer met `scripts/contrast_checker.py` in plaats van op het oog te schatten. Meer dan 8% van gebruikers heeft een vorm van kleurenblindheid; vertrouw nooit op kleur alleen.
- **Semantische HTML**: gebruik echte `<button>`- en `<label>`-elementen, geen `<div>`'s die er alleen visueel als knop uitzien.
- **Toetsenbordnavigatie**: het volledige login-/registratieproces moet met alleen het toetsenbord doorlopen kunnen worden, met zichtbare, duidelijke focus-indicatoren (custom `:focus`-stijl, niet de standaard broweroutline verwijderen zonder vervanging).
- **Screenreader-compatibiliteit**: labels en foutmeldingen correct gekoppeld aan hun velden; test met een echte screenreader (VoiceOver, NVDA), niet alleen visueel.
- **Eenvoudige, heldere taal** in instructies en foutmeldingen — vermijd jargon; een leesbaarheidsscore die aansluit bij een breed publiek is een goede toets.
- **Alternatieve authenticatiemethoden aanbieden** (biometrisch, OTP, hardware-sleutel) voor gebruikers voor wie een van de opties niet werkt.
- **Test met echte gebruikers, inclusief mensen met een beperking** — NN/g: met 5 testgebruikers ontdek je al tot 85% van de bruikbaarheidsproblemen.

## Beveiliging (grenzen van UX-verantwoordelijkheid)

- **CAPTCHA spaarzaam en toegankelijk**: alleen bij registratie of na meerdere mislukte inlogpogingen, altijd met een toegankelijk alternatief voor gebruikers die de standaardvorm niet kunnen voltooien.
- **Rate limiting op inlogpogingen** ter bescherming tegen brute-force, zonder legitieme gebruikers na één of twee tikfouten al te blokkeren.
- **Sessiebeheer** (verloop, vernieuwing, veilige cookies) is een technisch vraagstuk, maar heeft directe UX-impact: onverwacht uitloggen midden in een taak is een van de meest frustrerende ervaringen — communiceer sessieverloop vooraf waar mogelijk.

## States

- **Leeg / voor invoer** — velden met zichtbare labels (zie `inputfield.md`), social-login-opties en primaire actie duidelijk onderscheiden van secundaire ("Wachtwoord vergeten?", "Account aanmaken").
- **Bezig met valideren/inloggen** — directe feedback (zie `loading.md`) zodra de gebruiker op inloggen/registreren klikt.
- **Inline fout** — melding direct naast/onder het veld, met kleur + icoon + tekst.
- **MFA vereist** — duidelijke uitleg van de gekozen methode, met een zichtbare "andere methode gebruiken"-optie.
- **Wachtwoord vergeten onderweg** — bevestiging dat een e-mail/sms is verstuurd, met tijdsindicatie en hulp-link.
- **Succesvol ingelogd/geregistreerd** — duidelijke overgang naar de volgende stap in de flow, geen onnodige tussenpagina's.

## Veelgemaakte fouten

- Wachtwoordbevestiging (tweemaal typen) verplicht stellen in plaats van een "toon wachtwoord"-toggle.
- Wachtwoordeisen pas tonen ná een mislukte poging in plaats van vooraf.
- Autogegenereerde wachtwoorden van de OS-wachtwoordmanager afwijzen omdat het invoerveld niet herkend wordt.
- Alleen een validatiesamenvatting bovenaan tonen zonder foutmelding bij het veld zelf.
- Fouten tonen vóórdat de gebruiker klaar is met typen in een veld.
- Tooltips als enige manier om een foutmelding te tonen.
- MFA verplicht stellen zonder alternatieve methoden voor gebruikers zonder (toegestane) mobiele telefoon.
- De volledige wachtwoord-vergeten-flow onnodig lang maken (beveiligingsvragen, gebruikersnaam opnieuw invoeren) waardoor gebruikers halverwege afhaken.
- Kleur als enige signaal voor fout/succes, zonder icoon of tekst.
- Geen keuze bieden tussen passwordless (OTP/passkey) en een traditioneel wachtwoord — gebruikers dwingen in één authenticatiemodel.

## Ter inspiratie (visueel, geen functionele richtlijn)

Voor visuele inspiratie (layout, illustraties, kleurgebruik) kan een galerij zoals collectui.com/designs/sign-up-ui-design-inspiration nuttig zijn. Behandel dit puur als stijlinspiratie — de flow-, validatie- en toegankelijkheidsregels hierboven (NN/g, UX Collective) wegen zwaarder dan een visuele trend: bij login/registratie zit het gros van de problemen in proces en foutafhandeling, niet in vormgeving.

## Bronnen

- UX Collective — [Building better logins: a UX and accessibility guide for developers](https://uxdesign.cc/building-better-logins-a-ux-and-accessibility-guide-for-developers-9bb356f0a132)
- NN/g — [Passwordless Accounts: One-Time Passwords (OTPs) and Passkeys](https://www.nngroup.com/articles/passwordless-accounts/)
- NN/g — [10 Design Guidelines for Reporting Errors in Forms](https://www.nngroup.com/articles/errors-forms-design-guidelines/)
- CollectUI — [Sign-up UI Design Inspiration](https://collectui.com/designs/sign-up-ui-design-inspiration) (visuele inspiratie)
