# Meebouwen en bijdragen

CEDA bouwt open source samen met data-analisten, onderzoekers en ontwikkelaars bij mbo-, hbo- en wo-instellingen. Meld gerust een fout, verbeter een analyse of deel een bewezen oplossing uit jouw instelling.

## Kies hoe je wilt bijdragen

### 1. Een fout melden of verbetering voorstellen

Loop je vast bij het draaien van een pakket of zie je een inhoudelijke verbetering?

1. Ga naar de betreffende repository op [github.com/cedanl](https://github.com/cedanl).
2. Controleer bij **Issues** of jouw punt al bekend is.
3. Open een nieuw issue met een korte beschrijving van wat je verwachtte, wat er gebeurde en in welke omgeving je werkte (bijvoorbeeld R- of Python-versie en besturingssysteem).

!!! warning "Deel nooit persoonsgegevens in een issue of pull request"
    Plak geen echte studentnummers, namen, ruwe foutregels uit bronsystemen of interne instellingsdata in GitHub. Gebruik altijd een fictief of synthetisch voorbeeld. Zie onze [Dataconventies](../standards/data-conventions.md#privacy-en-gevoelige-gegevens).

### 2. Code of documentatie bijdragen via een pull request

Wil je zelf een oplossing bouwen of documentatie aanvullen? Volg dan deze werkwijze:

1. **Lees de basisafspraken:** bekijk de [Ontwikkelprincipes](../standards/principles.md) en de stijlgids voor [Python](../standards/python-style.md) of [R](../standards/r-style.md).
2. **Start met demodata:** draai de pijplijn en de bijbehorende tests eerst lokaal met de synthetische voorbeelddata in `data/.../demo/`.
3. **Werk op een eigen branch of fork:** houd je wijziging klein en gericht op één onderwerp.
4. **Controleer opmaak en tests:**
   - **Python:** draai `uv run ruff check .`, `uv run ruff format --check .` en `uv run pytest`.
   - **R:** draai `air format --check .` en voer de `testthat`-suite uit.
5. **Open een pull request:** leg kort uit welk probleem je oplost en hoe een beoordelaar je wijziging kan testen.

### 3. Een eigen instellingstool inbrengen of lokaal valideren

Veel CEDA-oplossingen ontstaan bij één onderwijsinstelling. Samen maken we ze daarna bruikbaar voor de hele sector.

- **Bestaande oplossing testen in de praktijk:** beproef een CEDA-product op je eigen instellingsdata en deel je ervaringen via de [CEDA-community](https://edu.nl/twt84).
- **Eigen analyse of dashboard delen:** heb je een werkend script, model of rapport dat andere instellingen ook helpt? Neem contact op via [ceda@surf.nl](mailto:ceda@surf.nl) of met projectleider [Corneel den Hartogh](mailto:corneel.denhartogh@surf.nl).
