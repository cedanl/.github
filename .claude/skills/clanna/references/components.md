# clanna-componenten

Elk blok is een complete `<section>` die je tussen `<!-- SLIDES:START -->` en `<!-- SLIDES:END -->` plakt. Alle klassen staan al in `assets/frame.html`; verzin geen nieuwe CSS als een bestaand component past. Kleuren alleen via `var(--npuls-*)` / `var(--licht-*)`.

## Slide-varianten

| Klasse | Achtergrond | Tekst | `.hl` / kicker | Gebruik |
|---|---|---|---|---|
| `s-blauw` | blauw | wit | geel | titel, sterk statement |
| `s-geel` / `s-groen` / `s-oranje` / `s-roze` | verzadigd | zwart | blauw / roze / roze / blauw | hoofdvraag, advies, afsluiting |
| `s-lblauw` `s-lgroen` `s-lgeel` `s-lroze` `s-loranje` | licht | zwart | eigen kleur | inhoudsslides met kaarten |
| `s-wit` | wit | zwart | blauw | data, tabellen, grafieken |

Ritme: titel `s-blauw` → afwisselend licht en `s-wit` → één verzadigde slide per hoofdstuk/kernboodschap → afsluiting `s-roze` (logo). Nooit drie keer dezelfde variant achter elkaar. Zwart is nooit een achtergrond.

**Kaarten** op lichte slides: wit (`.card`) of een verzadigde kleur (`.card blauw|geel|roze|groen|oranje`). Op `s-wit`: lichte kaarten (`.card lblauw|lgroen|...`). `.card blauw` krijgt automatisch witte tekst; gebruik daarin `.ico geel` of `.ico roze`, en voor `ul.ticks` `style="color:var(--npuls-geel)"` op de `<i>`.

**Iconen** (`.ico <kleur>`, Font Awesome `fa-solid`): wissel de kleuren af binnen een rij. De icoonkleur bij elke achtergrond is al goed gezet.

## Kop (op elke inhoudsslide)

```html
<div class="slide-head">
  <span class="kicker">Aanleiding</span>
  <h2>Eén boodschap per slide, <span class="hl">met het kernwoord gemarkeerd</span></h2>
  <p class="sub">Eén à twee zinnen context. Optioneel.</p>
</div>
```

De `h2` is een **bewering**, geen onderwerp: "Het gat is in één jaar bijna dichtgelopen", niet "Resultaten".

## 1. Drie kaarten met icoon

```html
<section class="slide s-loranje">
  <!-- deco: zie Vormtaal -->
  <div class="slide-head">…</div>
  <div class="body">
    <div class="grid g3">
      <div class="card">
        <div class="ico oranje"><i class="fa-solid fa-clock"></i></div>
        <h3>Korte kop</h3>
        <p>Maximaal ~25 woorden.</p>
      </div>
      <!-- 2× meer, ico geel / blauw -->
    </div>
    <div class="card row groen" style="margin-top:clamp(12px,1.7vh,22px)">
      <div class="ico roze"><i class="fa-solid fa-bullseye"></i></div>
      <p><strong>Daarom:</strong> de conclusie in één zin.</p>
    </div>
  </div>
</section>
```

`g2` / `g3` / `g4` voor 2–8 kaarten. Bij `g4` maximaal ~18 woorden per kaart.

## 2. Statement + lijst | kaarten (split)

```html
<section class="slide s-roze">
  <div class="slide-head"><span class="kicker">Het probleem</span><h2>…</h2></div>
  <div class="body">
    <div class="split">
      <div>
        <p class="pull">Een uitspraak in Cooper Light, max ~30 woorden.</p>
        <ul class="ticks" style="margin-top:clamp(18px,2.4vh,28px)">
          <li><i class="fa-solid fa-circle"></i><span>Punt één.</span></li>
          <li><i class="fa-solid fa-circle"></i><span>Punt twee.</span></li>
        </ul>
      </div>
      <div class="grid">
        <div class="card blauw"><div class="ico geel"><i class="fa-solid fa-lock-open"></i></div><h3>…</h3><p>…</p></div>
        <div class="card"><div class="ico groen"><i class="fa-solid fa-server"></i></div><h3>…</h3><p>…</p></div>
      </div>
    </div>
  </div>
</section>
```

## 3. Tekst + Npuls-illustratie

```html
<section class="slide s-lblauw">
  <div class="slide-head"><span class="kicker">…</span><h2>…</h2></div>
  <div class="body">
    <div class="split">
      <div><ul class="ticks">…</ul></div>
      <img class="illu" src="public/npuls/powerpoint_illustrations/kennisdeling.svg" alt="">
    </div>
  </div>
</section>
```

Kies de illustratie uit `references/assets.md`. Geen `.deco` aan de kant van de illustratie.

## 4. Kerncijfers

```html
<div class="grid g4">
  <div class="card"><div class="stat"><span class="big-num" style="color:var(--npuls-blauw)">1,50</span><span class="cap">Hoogste gemiddelde</span></div></div>
  <div class="card"><div class="stat"><span class="big-num" style="color:var(--npuls-groen)">0</span><span class="cap">Afkeuringen</span></div></div>
  <!-- … -->
</div>
```

Op een verzadigde slide (`s-groen`, `s-geel`) staan de witte kaarten mooi; cijferkleur wisselen.

## 5. Stappen

```html
<div class="steps">
  <div class="step"><span class="num" style="background:var(--npuls-blauw);color:var(--npuls-wit)">1</span>
    <div><div class="step-t">Eerst uitdunnen</div><p>Eén zin uitleg.</p></div></div>
  <div class="step"><span class="num" style="background:var(--npuls-geel)">2</span>
    <div><div class="step-t">Dan blind beoordelen</div><p>…</p></div></div>
</div>
```

Max 5 stappen; combineer met `split` als er een beeld of statement naast moet.

## 6. Scorebalken

```html
<div class="bars">
  <div class="bar-row win"><div class="bar-name">kimi-k3 <span class="tag">toelichting</span></div>
    <div class="bar-track"><div class="bar-fill" style="--w:75%;background:var(--npuls-blauw)"></div></div><div class="bar-val">1,50</div></div>
  <div class="bar-row ref"><div class="bar-name">ijklat <span class="tag">referentie</span></div>
    <div class="bar-track"><div class="bar-fill" style="--w:71%;background:var(--npuls-roze)"></div></div><div class="bar-val">1,42</div></div>
</div>
<div class="legend">
  <span><i class="swatch" style="background:var(--npuls-blauw)"></i> aanbevolen</span>
  <span><i class="swatch" style="background:var(--npuls-oranje)"></i> afgeraden</span>
</div>
```

`--w` = waarde / maximum × 100%. Max 8 balken. Kleur betekent iets (legenda), niet decoratief. `badge` voor een label achter een naam: `<em class="badge">AI Hub</em>`.

## 7. Tabel

```html
<table>
  <thead><tr><th style="width:8%">#</th><th style="width:30%">Type</th><th>Wat het test</th></tr></thead>
  <tbody>
    <tr><td>N1</td><td>…</td><td>…</td></tr>
  </tbody>
</table>
```

Rijen worden witte pillen; zet de tabel op een lichte slide (`s-lgeel`, `s-lblauw`), niet op `s-wit`. Max 7 rijen.

## 8. Procesketen

```html
<div class="chain">
  <div class="node lblauw"><b>raw/</b><span>Ruwe notities</span></div>
  <div class="hop"><b>ingest</b><i class="fa-solid fa-arrow-right"></i></div>
  <div class="node lgeel"><b>staging/</b><span>Concepten, review</span></div>
  <div class="hop"><b>akkoord</b><i class="fa-solid fa-arrow-right"></i></div>
  <div class="node lgroen"><b>wiki/</b><span>Gedeeld</span></div>
</div>
```

## 9. Lijn- of staafgrafiek

Inline `<svg class="chart" viewBox="0 0 1000 420">` in een `<div class="chart-wrap">`. Assen: `<text class="ax">`, annotaties: `<text class="ann" style="fill:var(--npuls-blauw)">`. Lijnen met `style="stroke:var(--npuls-…)"`. Kerngetallen eronder:

```html
<div class="chart-foot">
  <span class="chip"><b style="color:var(--npuls-blauw)">1.503</b><span>Beste closed</span></span>
  <span class="src">Bron: …</span>
</div>
```

## 10. Peiling (Mentimeter)

```html
<section class="slide s-lgeel" data-menti="poll1">
  <div class="slide-head"><span class="kicker"><i class="fa-solid fa-hand-point-up"></i> &nbsp;Peiling</span><h2>…?</h2></div>
  <div class="body"><div class="menti-wrap">
    <div class="menti-frame" data-menti-slot="poll1">
      <div class="menti-placeholder">
        <div class="ico oranje"><i class="fa-solid fa-chart-simple"></i></div>
        <h3>Mentimeter nog niet gekoppeld</h3>
        <p>Zet de embed-URL in het <code>MENTI</code>-blok onderaan dit bestand.</p>
      </div>
    </div>
  </div></div>
</section>
```

Zet de URL in `const MENTI = { url: '…' }` (of `poll1: '…'`).

## 11. Hoofdvraag / statement (verzadigd)

```html
<section class="slide s-geel">
  <div class="body">
    <span class="kicker">De vraag</span>
    <h1 style="max-width:18ch">Welk model onderhoudt de wiki het beste?</h1>
    <p class="lede" style="margin-top:clamp(14px,2vh,24px);max-width:42ch">Eén zin in Cooper Light.</p>
  </div>
</section>
```

## Vormtaal (`.deco`)

Maximaal twee per slide, in een hoek (`tr`, `br`, `bl`, `tl`), aan de kant waar **geen** tekst staat. Op verzadigde slides vol (geen opacity), op lichte en witte slides zacht (`opacity=".15"`–`".3"`). Alleen kleuren die bij de achtergrond mogen (tabel hierboven).

```html
<!-- concentrische ringen, rechtsboven -->
<svg class="deco tr" width="400" height="400" viewBox="0 0 400 400" fill="none">
  <circle cx="290" cy="110" r="170" style="stroke:var(--npuls-oranje)" stroke-width="12" opacity=".25"/>
  <circle cx="290" cy="110" r="98" style="fill:var(--npuls-oranje)" opacity=".18"/>
</svg>

<!-- pulse-curve, linksonder -->
<svg class="deco bl" width="400" height="280" viewBox="0 0 400 280" fill="none">
  <path d="M-10 180 C 70 90, 140 250, 220 160 S 350 60, 420 140" style="stroke:var(--npuls-groen)" stroke-width="14" stroke-linecap="round" opacity=".35"/>
</svg>

<!-- boog, rechtsonder -->
<svg class="deco br" width="380" height="380" viewBox="0 0 380 380" fill="none">
  <path d="M40 340 A 300 300 0 0 1 340 40 L 340 340 Z" style="fill:var(--npuls-geel)" opacity=".25"/>
</svg>

<!-- starburst, rechtsboven -->
<svg class="deco tr" width="420" height="420" viewBox="0 0 480 480" fill="none">
  <path d="M240 20 L270 170 L400 100 L320 230 L460 250 L320 275 L400 400 L268 325 L240 470 L212 325 L80 400 L160 275 L20 250 L160 230 L80 100 L210 170 Z" style="fill:var(--npuls-blauw)" opacity=".14"/>
</svg>

<!-- chevrons, rechtsboven (verzadigde slide) -->
<svg class="deco tr" width="300" height="300" viewBox="0 0 300 300" fill="none">
  <path d="M60 30 L190 150 L60 270" style="stroke:var(--npuls-blauw)" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

Een `h2` die over de volle breedte loopt botst met een `tr`-deco: kies dan `br`/`bl`. `qa.mjs` meldt dit als "tekst ligt over decoratie".
