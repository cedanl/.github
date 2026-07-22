# Het ISGVO-model: volledige uitwerking

Lees dit bestand wanneer je door de lagen van een ontwerp heen werkt en de vragen per laag nodig hebt. Het korte overzicht staat al in SKILL.md — dit is de uitwerking met alle vragen en voorbeelden per laag.

De lagen bouwen op elkaar voort: je kunt geen goede visuele beslissingen nemen zonder eerst te weten wat je communiceert, hoe het georganiseerd is en hoe het gedraagt. Direct naar *V* springen vóór *I*, *S* en *G* helder zijn, is een veelvoorkomende oorzaak van zwak ontwerp.

## I — Inhoud

**Wat moet er getoond worden?**

- Wat is de kernboodschap of taak die deze UI moet communiceren?
- Wat is de informatiehiërarchie — wat is primair, secundair, ondersteunend?
- Welke data of content moet zichtbaar zijn in elke toestand (leeg, laden, fout, succes)?
- Wat kan worden weggelaten of uitgesteld zonder het doel van de gebruiker te schaden?

Goede inhoudsbeslissingen elimineren hele ontwerpproblemen. Als iets niet op het scherm hoeft, hoef je het ook niet te ontwerpen.

## S — Structuur

**Hoe is de informatie georganiseerd en hoe bewegen gebruikers erdoorheen?**

- **Gebruikersstromen**: welke paden nemen gebruikers? Wat komt ervoor, wat erna?
- **Navigatiemodel**: hoe oriënteren gebruikers zich en bewegen ze tussen secties?
- **Informatiearchitectuur**: hoe wordt content opgedeeld, gelabeld en gegroepeerd?
- **Narratieve opbouw**: onthult de interface informatie in een logische, progressieve volgorde?

Structuur is waar wireframes en flows leven. Zorg dat dit klopt vóór je aan visueel ontwerp begint.

## G — Gedrag

**Hoe reageert het systeem op de gebruiker?**

Interfaces zijn niet statisch — ze reageren. Gedragsontwerp wordt vaak onderbenut, maar het is wat een interface levend en betrouwbaar laat aanvoelen.

- **Micro-interacties**: knopklikken, formulierverzendingen, togglen — elke actie heeft een reactie nodig
- **Feedback en feedforward**: weet de gebruiker wat er is gebeurd? Wat *zal* er gebeuren?
- **Validatie**: wanneer en hoe worden fouten getoond? Inline? Bij verzending?
- **Laad- en lege toestanden**: het happy path is niet het enige pad
- **Hover-, focus- en actieve toestanden**: welke visuele verandering signaleert interactiviteit?

Een UI met geweldige inhoud en structuur maar zonder gedragsontwerp voelt kapot aan, ook al ziet het er goed uit.

## V — Verbeelding (Visueel ontwerp)

**Hoe ziet het eruit?**

Pas nadat I, S en G solide zijn, komt de visuele laag. Dit is geen decoratie — het is de uitdrukking van alle bovenliggende beslissingen.

- **Visuele hiërarchie**: bouw hiërarchie met lettergrootte en gewicht — kleur is het laatste middel, niet het eerste. Begin met ontwerpen in grijswaarden: als het zonder kleur niet werkt, repareert kleur het niet.
- **Witruimte**: witruimte is structuur, geen lege ruimte. Gebruik een consistente schaal (bijv. 4, 8, 12, 16, 24, 32, 48px). Bij twijfel: meer witruimte, niet minder. Kan witruimte of een achtergrondwisseling een rand vervangen? Dat kan doorgaans.
- **Typografie**: beperk tot 2–3 niveaus; elk niveau heeft een duidelijk doel. De-benadruk secundaire content door contrast te verminderen — maak het primaire niet alleen luider maar het secundaire ook stiller.
- **Kleur**: draag betekenis, niet alleen sfeer — primaire acties, destructieve acties en toestanden hebben consistente kleurlogica. Zet nooit grijze tekst op een gekleurde achtergrond.
- **Lege toestanden**: ontwerp ze altijd bewust — ze zijn vaak de *eerste* ervaring van de gebruiker.

## O — Omgeving

**In welke context wordt de interface gebruikt?**

De omgeving doordringt alle andere lagen. Een UI ontworpen zonder begrip van de omgeving zal in de praktijk falen.

- **Platform en apparaat**: web, iOS, Android, desktop? Volg platformconventies die gebruikers al kennen
- **Schermformaten**: mobile-first als standaard, tenzij de context anders zegt
- **Toegankelijkheid**: WCAG-contrastverhouding bodytekst ≥ 4,5:1, grote tekst ≥ 3:1. Zichtbare focustoestanden. Vertrouw niet alleen op kleur. Interactieve doelwitten minimaal 44×44px. Formuliervelden altijd zichtbare labels — geen placeholders als enige label. Gebruik `scripts/contrast_checker.py` om kleurcombinaties objectief te toetsen in plaats van op het oog te schatten.
- **Fysieke context**: wordt dit gebruikt aan een bureau, onderweg, in fel licht, met één hand?
- **Prestaties**: werkt de UI goed bij trage verbindingen? Prestaties zijn UX.
