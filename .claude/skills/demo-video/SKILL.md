---
name: demo-video
description: Neemt autonoom een geannoteerde demo video op van de lokale app met headless
  Playwright, genereert neppe maar realistische mock data, schrijft narration script en
  genereert TTS audio via piper-tts (piper-gpl1), en samenvoegt alles met FFmpeg. Upload
  naar GitHub CDN voor inline README-weergave. Gebruik wanneer iemand een demo video,
  annotated walkthrough of narrated demo van de app wil maken.
---

# Demo Video

Volledig autonome demo video pipeline. Leest de repo om de app op te starten en de
datastructuur te begrijpen, vult alle externe data met realistische nep-data (zodat de
video er live uitziet zonder echte API-calls), neemt per scene op met headless Chromium,
schrijft narration script, genereert TTS audio via piper-tts, en samenvoegt met FFmpeg.

Tussenproducten worden altijd bewaard zodat individuele stappen opnieuw kunnen worden
gedraaid zonder de hele pipeline opnieuw te doorlopen.

## Output structuur

```
demo-video/
├── scenes/
│   ├── record.mjs of record.py    # Gegenereerd opnamescript
│   ├── scene-01-*.webm            # Ruwe Playwright opnames per scene
│   ├── scene-01-*.mp4             # Geconverteerd per scene (met title overlay)
│   └── concat.txt                 # FFmpeg concat-lijst
├── narration.txt                  # Narration script
├── generate_audio.py              # Gegenereerd piper script
├── narration.wav                  # TTS audio (hoogste kwaliteit piper model)
├── voices/                        # Gedownloade piper stemmodellen
├── source_video.mp4               # Stitched video zonder audio
└── demo_final.mp4                 # Eindproduct (video + audio)
```

## Workflow

When the user invokes `/demo-video`:

### 1. Controleer dependencies

```bash
echo "=== Dependency check ===" && \
ffmpeg -version 2>/dev/null | head -1 || echo "MISSING: ffmpeg" && \
uv --version 2>/dev/null || echo "MISSING: uv" && \
python3 -c "import playwright; print('playwright ok')" 2>/dev/null || \
  echo "MISSING: playwright  →  pip install playwright" && \
python3 -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--no-sandbox'])
    b.close()
    print('chromium binary ok')
" 2>/dev/null || echo "MISSING: chromium binary  →  python3 -m playwright install chromium" && \
python3 -c "import piper; print('piper-tts ok')" 2>/dev/null || \
  echo "MISSING: piper-tts  →  uv add piper-tts" && \
gh auth status 2>/dev/null | head -1 || \
  echo "MISSING: gh auth  →  gh auth login  of  export GH_TOKEN=..."
```

Stop als een tool ontbreekt en rapporteer exact wat geïnstalleerd moet worden.
Ga niet verder zonder alle dependencies.

### 2. Begrijp de app

Lees de repo-documentatie om te bepalen:
- Hoe de app gestart wordt (start command, poort)
- Welke API-endpoints externe data ophalen (intercepteer deze met mock data)
- Wat de primaire user flows zijn
- In welke taal de app is (voor piper model keuze)

```bash
cat README.md 2>/dev/null | head -200
cat DEVELOPMENT.md 2>/dev/null | head -100
cat Makefile 2>/dev/null | grep -E "^(dev|start|run|serve):" | head -10
grep -r "fetch\|axios\|requests\.get\|/api/" src/ \
  --include="*.py" --include="*.ts" --include="*.js" -l 2>/dev/null | head -10
```

### 3. Start de app lokaal

```bash
mkdir -p demo-video/scenes demo-video/voices
<startcommando> > demo-video/app.log 2>&1 &
echo $! > demo-video/.app_pid
timeout 45 bash -c \
  'until curl -sf http://localhost:<poort> >/dev/null 2>&1; do sleep 1; done' \
  && echo "app ready" || (echo "FAILED — check demo-video/app.log"; exit 1)
```

### 4. Plan scènes en mock data

Op basis van stap 2: bepaal 3–6 scenes die de kernfunctionaliteit tonen. Bepaal per scene:
- Welke interacties plaatsvinden (clicks, type, scroll)
- Welke annotaties zinvol zijn (floating overlay voor context, ring+badge voor UI-elementen)
- Welke API-endpoints gemockt moeten worden

**Mock data principes:**
- Gebruik realistische maar neppe data — echte namen van instellingen, plausibele
  getallen, correcte datastructuren
- Lees de API response shape uit de broncode zodat de mock exact klopt
- Seed localStorage via `addInitScript` zodat onboarding/login flows overgeslagen worden
- Vul tekstvelden in met neppe maar geloofwaardige waarden die passen bij de app

### 5. Genereer en voer het opnamescript uit

**Voor JS/TS apps** — genereer `demo-video/scenes/record.mjs` met onderstaande structuur.
**Voor Python apps** — genereer `demo-video/scenes/record.py` (zie Python-variant onderaan).

#### JavaScript scaffold (`record.mjs`)

```javascript
import { chromium } from 'playwright';
import { execSync } from 'child_process';
import { existsSync, mkdirSync, renameSync } from 'fs';
import { join, resolve } from 'path';

const ROOT    = resolve(import.meta.dirname, '../..');
const RAW_DIR = resolve(import.meta.dirname, '../scenes');
const APP_URL = 'http://localhost:<poort>';
const VIEWPORT = { width: 1280, height: 720 };

// ── Mock data ────────────────────────────────────────────────────────────────
// Vul hier app-specifieke mock responses in op basis van de broncode (stap 2)
const MOCK_DATA = { /* ... */ };

// ── Helpers ──────────────────────────────────────────────────────────────────
function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

async function setupMocks(page) {
  // Intercepteer API-calls met neppe maar realistische data
  await page.route('**/api/<endpoint>', route =>
    route.fulfill({ status: 200, contentType: 'application/json',
                    body: JSON.stringify(MOCK_DATA) })
  );
  // Seed localStorage (onboarding overslaan)
  await page.addInitScript(({ data }) => {
    localStorage.setItem('app_settings', JSON.stringify(data));
    localStorage.setItem('app_onboarded', '1');
  }, { data: { instelling: 'Hogeschool Utrecht', rol: 'Beleidsmedewerker' } });
}

// Stijl 1: floating overlay (globale context-berichten)
async function showAnnotation(page, text, position = 'bottom-center', durationMs = 2500) {
  const posStyles = {
    'bottom-center': 'bottom:80px;left:50%;transform:translateX(-50%);',
    'top-center':    'top:80px;left:50%;transform:translateX(-50%);',
    'top-right':     'top:80px;right:24px;',
    'top-left':      'top:80px;left:24px;',
    'bottom-left':   'bottom:100px;left:24px;',
    'bottom-right':  'bottom:100px;right:24px;',
    'center':        'top:50%;left:50%;transform:translate(-50%,-50%);',
  };
  await page.evaluate(({ text, style }) => {
    const el = document.createElement('div');
    el.className = '__demo-annotation';
    el.textContent = text;
    el.setAttribute('style',
      `position:fixed;z-index:99999;pointer-events:none;` +
      `background:rgba(37,99,235,0.92);color:white;` +
      `padding:14px 28px;border-radius:14px;` +
      `font-size:17px;font-weight:700;font-family:Inter,system-ui,sans-serif;` +
      `box-shadow:0 6px 28px rgba(0,0,0,0.2);animation:fadeInAnnotation .3s ease;` + style
    );
    if (!document.querySelector('#__demo-anim-style')) {
      const s = document.createElement('style');
      s.id = '__demo-anim-style';
      s.textContent = '@keyframes fadeInAnnotation{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}';
      document.head.appendChild(s);
    }
    document.body.appendChild(el);
  }, { text, style: posStyles[position] || posStyles['bottom-center'] });
  await delay(durationMs);
  await page.evaluate(() =>
    document.querySelectorAll('.__demo-annotation').forEach(e => e.remove())
  );
}

// Stijl 2: element-anchored ring + badge (highlight specifieke UI-elementen)
async function annotate(page, selector, label, side = 'right', color = '#4F46E5') {
  await page.evaluate(({ selector, label, side, color }) => {
    document.querySelectorAll('.__ann').forEach(n => n.remove());
    const el = document.querySelector(selector);
    if (!el) { console.warn('ann: not found', selector); return; }
    const r = el.getBoundingClientRect(), pad = 8;
    if (!document.querySelector('#__ann-style')) {
      const s = document.createElement('style');
      s.id = '__ann-style';
      s.textContent = `@keyframes ann-pulse{0%,100%{box-shadow:0 0 0 0 ${color}55}50%{box-shadow:0 0 0 8px transparent}}`;
      document.head.appendChild(s);
    }
    const ring = document.createElement('div');
    ring.className = '__ann';
    ring.style.cssText = `position:fixed;pointer-events:none;z-index:2147483647;` +
      `left:${r.left-pad}px;top:${r.top-pad}px;` +
      `width:${r.width+pad*2}px;height:${r.height+pad*2}px;` +
      `border:3px solid ${color};border-radius:8px;animation:ann-pulse 1.6s ease infinite;`;
    document.body.appendChild(ring);
    const badge = document.createElement('div');
    badge.className = '__ann';
    badge.textContent = label;
    const bw = Math.max(label.length * 7.5 + 20, 120);
    const pos = { right:[r.right+14, r.top+r.height/2-13],
                  left:[r.left-bw-14, r.top+r.height/2-13],
                  above:[r.left, r.top-36], below:[r.left, r.bottom+8] }[side];
    badge.style.cssText = `position:fixed;pointer-events:none;z-index:2147483647;` +
      `left:${pos[0]}px;top:${pos[1]}px;background:${color};color:#fff;` +
      `padding:3px 10px;font:bold 12px/22px monospace;border-radius:3px;` +
      `white-space:nowrap;box-shadow:0 2px 10px rgba(0,0,0,.5);`;
    document.body.appendChild(badge);
  }, { selector, label, side, color });
}

function clearAnnotations(page) {
  return page.evaluate(() =>
    document.querySelectorAll('.__ann,.__demo-annotation').forEach(e => e.remove())
  );
}

// Scroll altijd via evaluate — nooit Playwright's eigen scroll (onbetrouwbaar headless)
async function scrollTo(page, selector) {
  await page.evaluate(sel => {
    const el = document.querySelector(sel);
    if (el) el.scrollIntoView({ block: 'center', behavior: 'smooth' });
  }, selector);
  await delay(600);
}

async function scrollBy(page, pixels) {
  await page.evaluate(px => window.scrollBy({ top: px, behavior: 'smooth' }), pixels);
  await delay(800);
}

async function recordScene(browser, name, sceneFn, opts = {}) {
  console.log(`  Recording: ${name}...`);
  const context = await browser.newContext({
    viewport: VIEWPORT,
    colorScheme: opts.colorScheme || 'light',
    recordVideo: { dir: RAW_DIR, size: VIEWPORT },
  });
  const page = await context.newPage();
  await setupMocks(page);
  await page.goto(APP_URL, { waitUntil: 'networkidle' });
  await delay(600);
  try {
    await sceneFn(page);
  } catch (err) {
    console.error(`  Error in ${name}:`, err.message);
  }
  await delay(500);
  const videoPath = await page.video().path();
  await context.close();
  const dest = join(RAW_DIR, `${name}.webm`);
  renameSync(videoPath, dest);
  console.log(`  Saved: ${dest}`);
  return dest;
}

// ── Scenes ───────────────────────────────────────────────────────────────────
// Voeg hier de app-specifieke scene functies toe (stap 4)

// ── Main ─────────────────────────────────────────────────────────────────────
async function main() {
  // Pre-flight check
  try {
    const res = await fetch(APP_URL, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
  } catch {
    console.error(`ERROR: app not running at ${APP_URL}`);
    process.exit(1);
  }

  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  // Scenes: [naam, sceneFunctie, opties]
  const scenes = [
    // ['scene-01-home', sceneHome],
    // ['scene-02-chat', sceneChat, { colorScheme: 'light' }],
  ];

  const videoPaths = [];
  for (const [name, fn, opts] of scenes) {
    videoPaths.push(await recordScene(browser, name, fn, opts || {}));
  }
  await browser.close();
  console.log('\nAlle scenes opgenomen.');
}

main().catch(err => { console.error('Fatal:', err); process.exit(1); });
```

#### Python scaffold (`record.py`)

Gebruik dit voor Python/Streamlit/FastAPI apps:

```python
#!/usr/bin/env python3
from __future__ import annotations
import shutil, subprocess, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT    = Path(__file__).parent.parent.parent
RAW_DIR = Path(__file__).parent
APP_URL = "http://localhost:<poort>"

def wait_for_app(url: str, timeout: int = 45) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=2); return
        except Exception:
            time.sleep(0.5)
    raise RuntimeError(f"App not ready after {timeout}s")

def ann(page, selector, label, side="right", color="#4F46E5"):
    page.evaluate("""({ selector, label, side, color }) => {
        document.querySelectorAll('.__ann').forEach(n => n.remove());
        const el = document.querySelector(selector);
        if (!el) return;
        const r = el.getBoundingClientRect(), pad = 8;
        const ring = document.createElement('div');
        ring.className = '__ann';
        ring.style.cssText = `position:fixed;pointer-events:none;z-index:2147483647;` +
          `left:${r.left-pad}px;top:${r.top-pad}px;` +
          `width:${r.width+pad*2}px;height:${r.height+pad*2}px;` +
          `border:3px solid ${color};border-radius:8px;`;
        document.body.appendChild(ring);
        const badge = document.createElement('div');
        badge.className = '__ann';
        badge.textContent = label;
        badge.style.cssText = `position:fixed;pointer-events:none;z-index:2147483647;` +
          `left:${r.right+14}px;top:${r.top+r.height/2-13}px;` +
          `background:${color};color:#fff;padding:3px 10px;` +
          `font:bold 12px/22px monospace;border-radius:3px;`;
        document.body.appendChild(badge);
    }""", {"selector": selector, "label": label, "side": side, "color": color})

def clear(page):
    page.evaluate("() => document.querySelectorAll('.__ann').forEach(n => n.remove())")

def scroll_to(page, selector):
    page.evaluate(
        "sel => { const el = document.querySelector(sel); if (el) el.scrollIntoView({block:'center',behavior:'smooth'}); }",
        selector)
    page.wait_for_timeout(600)

def main():
    wait_for_app(APP_URL)

    with sync_playwright() as pw:
        # Warmup zonder recording (zodat Streamlit/etc volledig geladen is)
        ctx_warm = pw.chromium.launch(args=["--no-sandbox"]).new_context(
            viewport={"width": 1280, "height": 800})
        p_warm = ctx_warm.new_page()
        p_warm.goto(APP_URL)
        p_warm.wait_for_timeout(3000)
        ctx_warm.browser.close()

        browser = pw.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
        ctx = browser.new_context(
            record_video_dir=str(RAW_DIR),
            record_video_size={"width": 1280, "height": 800},
            viewport={"width": 1280, "height": 800},
        )
        page = ctx.new_page()
        page.goto(APP_URL)
        page.wait_for_timeout(2000)

        # Voeg hier app-specifieke scene-stappen toe (stap 4)

        ctx.close()
        browser.close()

    # Hernoem WebM
    webms = list(RAW_DIR.glob("*.webm"))
    if webms:
        webms[0].rename(RAW_DIR / "scene-01.webm")
        print(f"Opgenomen: {RAW_DIR / 'scene-01.webm'}")

if __name__ == "__main__":
    main()
```

Voer het script uit:

```bash
node demo-video/scenes/record.mjs
# of voor Python apps:
uv run python demo-video/scenes/record.py
```

### 6. Stitch scenes met FFmpeg

Gebruik een Python script voor de conversie — dit geeft een betrouwbare font-fallback
als `drawtext` faalt (devcontainers zonder fontconfig):

```python
# Voer inline uit of sla op als demo-video/stitch.py
import subprocess, os
from pathlib import Path

SCENES_DIR = Path("demo-video/scenes")
OUTPUT     = Path("demo-video/source_video.mp4")

# Scene titels: pas aan op basis van de opgenomen scenes
SCENE_TITLES = {
    "scene-01": "1. Home",
    "scene-02": "2. Chat",
    # ...
}

mp4_paths = []
for webm in sorted(SCENES_DIR.glob("scene-*.webm")):
    name  = webm.stem
    title = SCENE_TITLES.get(name, name)
    mp4   = webm.with_suffix(".mp4")
    drawtext = (
        f"drawtext=text='{title}':fontsize=26:fontcolor=white:"
        f"box=1:boxcolor=black@0.55:boxborderw=14:x=36:y=36:"
        f"enable='lt(t\\,3.5)'"
    )
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(webm), "-vf", drawtext,
             "-c:v", "libx264", "-preset", "fast", "-crf", "23",
             "-pix_fmt", "yuv420p", "-an", str(mp4)],
            check=True, capture_output=True, timeout=120
        )
    except subprocess.CalledProcessError:
        # Fallback zonder title overlay (font niet beschikbaar)
        print(f"  Title overlay mislukt voor {name}, doorgaan zonder overlay...")
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(webm),
             "-c:v", "libx264", "-preset", "fast", "-crf", "23",
             "-pix_fmt", "yuv420p", "-an", str(mp4)],
            check=True, timeout=120
        )
    mp4_paths.append(mp4)
    print(f"  Geconverteerd: {mp4}")

# Concat
concat_file = SCENES_DIR / "concat.txt"
concat_file.write_text("\n".join(f"file '{p.resolve()}'" for p in mp4_paths))

subprocess.run(
    ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
     "-i", str(concat_file),
     "-c:v", "libx264", "-preset", "fast", "-crf", "22",
     "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUTPUT)],
    check=True, timeout=300
)
print(f"Stitched: {OUTPUT}")
```

```bash
python3 demo-video/stitch.py
```

### 7. Schrijf narration script

Analyseer de opgenomen scenes en schrijf een doorlopende narration tekst afgestemd op
de visuele flow. Sla op als `demo-video/narration.txt` — één doorlopende tekst zonder
timestamps.

De tekst moet:
- Synchroon lopen met de scènes — begin met de eerste scene, eindig met de laatste
- Elke annotatie in woorden benoemen zodat audio en beeld kloppen
- Natuurlijk klinken als gesproken Nederlands (of Engels, afhankelijk van de app)
- Ruwweg even lang zijn als de video (tel seconden per zin: ~2,5 woorden/sec gesproken NL)

### 8. Genereer TTS audio met piper-tts

Schrijf en voer `demo-video/generate_audio.py` uit. Gebruik de Python library direct
(niet de CLI) en altijd het hoogste kwaliteitsmodel voor de taal van de app:

| Taal | Hoogste kwaliteitsmodel |
|------|------------------------|
| Nederlands | `nl_NL-mls_5809-medium` |
| Engels | `en_US-ryan-high` |
| Duits | `de_DE-thorsten-high` |

```python
# demo-video/generate_audio.py
import wave
from pathlib import Path
from piper import PiperVoice
from piper.download import ensure_voice_exists, get_voices

DEMO_DIR   = Path("demo-video")
VOICES_DIR = DEMO_DIR / "voices"
VOICE      = "nl_NL-mls_5809-medium"  # pas aan op basis van app-taal

NARRATIE = (DEMO_DIR / "narration.txt").read_text()
VOICES_DIR.mkdir(exist_ok=True)

voices_info = get_voices(VOICES_DIR, update_voices=False)
ensure_voice_exists(VOICE, [VOICES_DIR], VOICES_DIR, voices_info)

voice = PiperVoice.load(str(VOICES_DIR / f"{VOICE}.onnx"))
with wave.open(str(DEMO_DIR / "narration.wav"), "wb") as wav:
    voice.synthesize_wav(NARRATIE, wav)

with wave.open(str(DEMO_DIR / "narration.wav"), "rb") as f:
    duration = f.getnframes() / f.getframerate()
print(f"Audio gegenereerd: narration.wav ({duration:.1f}s)")
```

```bash
uv run python demo-video/generate_audio.py
```

### 9. Samenvoegen video + audio

Voeg video en audio samen. Gebruik geen `-shortest` — als de narration iets korter is
dan de video loopt de video stil door (gewenst gedrag). Als de narration langer is,
wordt de audio afgekapt op de videoduur.

```bash
ffmpeg -y \
  -i demo-video/source_video.mp4 \
  -i demo-video/narration.wav \
  -c:v copy -c:a aac \
  -map 0:v:0 -map 1:a:0 \
  demo-video/demo_final.mp4

ls -lh demo-video/demo_final.mp4
```

### 10. Upload naar GitHub CDN

Committed video's spelen niet inline af in GitHub READMEs — gebruik GitHub Releases.
Controleer eerst of `gh auth` werkt (zie stap 1).

```bash
# Maak release aan als die nog niet bestaat
gh release create demo-videos \
  --title "Demo Videos" \
  --notes "Automated demo video uploads" 2>/dev/null || true

# Upload (overschrijf als al bestaat)
gh release upload demo-videos demo-video/demo_final.mp4 --clobber

# Haal URL op
VIDEO_URL=$(gh release view demo-videos --json assets \
  --jq '.assets[] | select(.name=="demo_final.mp4") | .browserDownloadUrl')

echo "Embed URL: $VIDEO_URL"
```

Stop de app:

```bash
kill "$(cat demo-video/.app_pid)" 2>/dev/null || true
```

### 11. Rapporteer

Toon de gebruiker:

```
Demo video klaar.

Embed in README.md:
<video src="<VIDEO_URL>" controls width="100%"></video>

Tussenproducten bewaard in demo-video/:
  scenes/record.*         — opnamescript (hergebruik bij re-record)
  scenes/scene-*.webm/mp4 — ruwe scenes  (re-run stap 6+ voor andere stitching)
  stitch.py               — stitch script (re-run stap 6+)
  narration.txt           — script aanpassen → re-run stap 8+9
  generate_audio.py       — audio script  → re-run stap 8+9
  narration.wav           — audio aanpassen → re-run stap 9
  source_video.mp4        — video zonder audio → re-run stap 9
  demo_final.mp4          — eindproduct
```

## Benodigde permissies

Voeg toe aan `.claude/settings.json` → `permissions.allow` voor prompt-vrije uitvoering:

```json
"Bash(ffmpeg:*)",
"Bash(node:*)",
"Bash(uv run python*)",
"Bash(python3:*)",
"Bash(gh release*)",
"Bash(curl:*)",
"Bash(kill:*)",
"Bash(timeout:*)"
```

## Important

- Stap 1 is verplicht — stop bij ontbrekende dependencies (inclusief chromium binary
  en `gh auth`), geen workarounds
- **Mock data**: gebruik altijd `page.route()` voor API-intercept en `addInitScript()`
  voor localStorage; lees de response shape uit de broncode zodat de mock exact klopt
- **Twee annotatiestijlen**: floating overlay voor globale context-berichten,
  element-anchored ring+badge voor specifieke UI-elementen — gebruik beide
- **Scroll altijd via `page.evaluate()`** met `scrollIntoView` of `scrollBy` — nooit
  Playwright's eigen scroll (onbetrouwbaar in headless)
- **`--no-sandbox` en `--disable-setuid-sandbox`** altijd meegeven aan chromium launch
  in devcontainer/CI-omgevingen
- **FFmpeg stitch via Python script** (niet shell loop) — geeft betrouwbare font-fallback
  als `drawtext` faalt door ontbrekende fontconfig
- **Geen `-shortest`** bij video+audio merge — laat video volledig doorlopen als narration
  iets korter is; audio wordt afgekapt aan videoduur als narration langer is
- **Piper**: gebruik de Python library direct (`from piper import PiperVoice`), altijd
  het hoogste kwaliteitsmodel voor de gedetecteerde taal (`piper-tts` op PyPI)
- **Upload via `gh release upload`**, nooit via git commit — committed bestanden spelen
  niet inline af in GitHub README `<video>` tags
- **Tussenproducten altijd bewaren** — elke stap kan los opnieuw worden gedraaid
- Alleen voor cedanl-repos
