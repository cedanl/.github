---
icon: lucide/terminal
---

# Entire CLI — Handleiding

Entire is een Git-natieve tool die AI-sessies (prompts, tool calls, transcripts) vastlegt naast je commits. Elke wijziging is herleidbaar naar de prompt die hem veroorzaakte. De CLI is open source ([entireio/cli](https://github.com/entireio/cli), MIT-licentie, Go).

Voor de governance-regels zie de [werkafspraak Entire](../werkafspraken/entire.md).

## Hoe het werkt

Entire installeert Git-hooks in je repository die sessiedata vastleggen terwijl je werkt. Bij een `git commit` wordt een **checkpoint** aangemaakt — een snapshot van de volledige sessiecontext (prompts, tool-calls, gewijzigde bestanden, transcripts).

Checkpoint-data wordt apart van je code opgeslagen, zodat je git-historie schoon blijft. Alleen het ID van het checkpoint verschijnt als `Entire-Checkpoint`-trailer in je commit message. Waar de data precies staat hangt af van de opslag, zie [Checkpoint-opslag](#checkpoint-opslag-branch-of-refs). Bij ons is dat de branch `entire/checkpoints/v1` met een 12-tekens ID (bijv. `a3b2c4d5e6f7`).

```
Jouw branch                    entire/checkpoints/v1
     │                                  │
     ▼                                  │
[Base commit]                           │
     │                                  │
     │  ┌─── Agent werkt ───┐           │
     │  │  Stap 1           │           │
     │  │  Stap 2           │           │
     │  └───────────────────┘           │
     │                                  │
     ▼                                  ▼
[Commit] ─────────────────────► [Sessiemetadata]
                                 (transcript, prompts,
                                  bestanden)
```

## Installatie

=== ":fontawesome-brands-apple: macOS"

    Via Homebrew:

    ```bash
    brew tap entireio/tap
    brew trust entireio/tap
    brew install --cask entire
    ```

=== ":fontawesome-brands-linux: Linux"

    ```bash
    curl -fsSL https://entire.io/install.sh | bash
    ```

    Voor ARM64:

    ```bash
    curl -LO https://github.com/entireio/cli/releases/latest/download/entire-linux-arm64.tar.gz
    tar -xzf entire-linux-arm64.tar.gz
    sudo mv entire /usr/local/bin/
    ```

=== ":fontawesome-brands-windows: Windows"

    Via Scoop:

    ```bash
    scoop bucket add entire https://github.com/entireio/scoop-bucket.git
    scoop install entire/entire
    ```

=== ":lucide-code-xml: Vanuit bron"

    Vereist Go 1.21 of nieuwer:

    ```bash
    go install github.com/entireio/cli/cmd/entire@latest
    ```

### Verifiëren

```bash
entire version
```

## In onze omgeving

In de CEDA devcontainer is Entire al geconfigureerd. Je hoeft niets handmatigs te doen.

### Automatische activatie

De `claude`-functie in de container draait bij het starten `entire-setup`, en doet dan per CEDA-repo:

1. `entire enable -y --agent claude-code` — installeert de hooks
2. `entire configure --checkpoint-backend branch --checkpoint-remote github:cedanl/entire-checkpoints` — kiest de opslag (branch) en wijst de checkpoint-repo aan
3. Start daarna Claude Code met `--dangerously-skip-permissions`

`entire-setup` doet dit voor de repo waar je staat én voor elke repo direct onder `/workspaces/dev-dots`, dus ook als je Claude in de root start. Een repo die al klopt wordt alleen gelezen. Handmatig draaien of controleren kan met `entire-setup` en `entire-setup --check`. Een mislukte stap wordt met de reden getoond. Zie ook [dev-dots#49](https://github.com/cedanl/dev-dots/pull/49).

Dit gebeurt alleen in CEDA-repos: waar `origin` `cedanl/` bevat (GitHub) of `surf-internal/npuls/ceda/` (GitLab, git.sdp.surf.nl). Checkpoints van beide gaan naar dezelfde GitHub-repo, want Entire kent als checkpoint-remote alleen GitHub. Dit gebeurt bij elke start van `claude`, dus `entire disable` blijft niet staan. Uitzetten kan met `git config devdots.entire false` (één repo) of `export DEVDOTS_ENTIRE=0` (alle repo's).

Gebruik je een agent om Entire in te stellen? Zie de tekst voor je agent in de [werkafspraak](../werkafspraken/entire.md#laat-je-agent-het-regelen).

### Centrale checkpoint-repo

Alle checkpoints worden gesynchroniseerd naar **`cedanl/entire-checkpoints`**. Dit is een private repo waar de sessiedata van alle teamleden samenkomt. Bij een `git push` wordt de `entire/checkpoints/v1` branch automatisch meegestuurd.

### Configuratie

De configuratie staat per repo in `.entire/settings.json`. Die map staat in `.git/info/exclude`, dus ze wordt niet gecommit. De hooks voor Claude Code komen in `.claude/settings.local.json`, zodat een gedeelde `.claude/settings.json` schoon blijft.

```json
{
  "enabled": true,
  "strategy_options": {
    "checkpoint_remote": {
      "provider": "github",
      "repo": "cedanl/entire-checkpoints"
    }
  },
  "checkpoints": {
    "primary": {
      "type": "git-branch"
    }
  }
}
```

Persoonlijke overrides kunnen in `.entire/settings.local.json`.

### Checkpoint-opslag: branch of refs

Entire kent twee manieren om checkpoints op te slaan:

| Opslag | Instelling | Waar | ID |
|--------|------------|------|----|
| **Branch** (onze keuze) | `git-branch` | één gedeelde branch `entire/checkpoints/v1` | 12 tekens |
| Refs | `git-refs` | één ref per checkpoint: `refs/entire/checkpoints/<xx>/<id>` | ULID, 26 tekens |

De CLI noemt refs zelf de aanbevolen opslag. Refs staan niet in de branchlijst op GitHub en zijn daardoor makkelijk over het hoofd te zien. Wij kiezen de branch, zodat de sessies van het hele team op één plek zichtbaar zijn. Nadeel: iedereen schrijft naar dezelfde branch, dus pushes kunnen botsen.

Checkpoints met een ULID zijn alleen via de refs leesbaar door `entire checkpoint explain`. Een kopie op de branch is wel gewoon als bestand te bekijken op GitHub.

## Op je eigen Mac met Claude Desktop

Werk je zonder devcontainer, in de Code-tab van de Claude-app op macOS, dan is er geen `entire-setup`. Je zet Entire dan zelf op. Dit is getest op 24 november 2026 met Entire CLI 0.13.4 op een Mac met Apple Silicon.

### 1. Installeer de CLI

Installeer Entire volgens [Installatie](#installatie). Controleer daarna in een nieuwe terminal:

```bash
entire version
```

De Code-tab gebruikt dezelfde shell en dezelfde `PATH` als je terminal. Vindt `entire version` niets, dan vindt Claude het ook niet. Je krijgt dan bij de start van een chat de melding `Entire CLI is enabled but not installed or not on PATH`. Staat `entire` in `~/.local/bin`, zorg dan dat die map in je `PATH` staat, bijvoorbeeld via `~/.zshrc`.

### 2. Zet Entire aan per repo

Draai dit eenmalig in elke CEDA-repo:

```bash
entire enable --agent claude-code --checkpoint-remote github:cedanl/entire-checkpoints
```

Dit maakt drie dingen aan:

- `.entire/settings.json`, met `cedanl/entire-checkpoints` als checkpoint-remote en `git-branch` als opslag. Dat is dezelfde opslag als in de container.
- Git-hooks in `.git/hooks` (`commit-msg`, `post-commit`, `pre-push` en andere).
- De hooks voor Claude Code. **Let op:** op de Mac zet Entire die in `.claude/settings.json`, niet in `.claude/settings.local.json` zoals in de container.

Commit `.claude/settings.json` niet zonder overleg. Het bestand bevat alleen de Entire-hooks en staat bij een nieuwe repo als untracked in `git status`. Wil je dat niet zien, zet dan `/.claude/settings.json` in `.git/info/exclude`. Bestaat er in de repo al een gedeelde `.claude/settings.json`, kijk dan na wat `entire enable` eraan heeft toegevoegd voordat je commit.

### 3. Optioneel: automatisch aanzetten in nieuwe CEDA-repo's

Op de Mac kun je Entire bij elke nieuwe chat automatisch laten aanzetten met een globale SessionStart-hook van Claude Code. Die werkt voor alle projecten. Zet dit script in `~/.claude/hooks/entire-ceda-autoenable.sh`:

```sh
#!/bin/sh
# SessionStart-hook: zet Entire automatisch aan in CEDA-repo's (origin op github.com/cedanl/).
# Doet niets buiten CEDA-repo's, of als Entire al geconfigureerd is. Commit niets.

input=$(cat 2>/dev/null)
dir=""
if command -v jq >/dev/null 2>&1; then
  dir=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null)
fi
[ -n "$dir" ] || dir="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$dir" 2>/dev/null || exit 0

command -v entire >/dev/null 2>&1 || exit 0
root=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$root" || exit 0

origin=$(git remote get-url origin 2>/dev/null) || exit 0
case "$origin" in
  *github.com[:/]cedanl/*) ;;
  *) exit 0 ;;
esac

[ -f .entire/settings.json ] && exit 0

if entire enable --agent claude-code --checkpoint-remote github:cedanl/entire-checkpoints </dev/null >/dev/null 2>&1; then
  msg="Entire is automatisch aangezet in deze CEDA-repo. Deze eerste chat wordt mogelijk niet volledig vastgelegd."
else
  msg="Entire automatisch aanzetten in deze CEDA-repo is mislukt. Draai handmatig: entire enable --agent claude-code --checkpoint-remote github:cedanl/entire-checkpoints"
fi
printf '{"systemMessage":"%s"}\n' "$msg"
exit 0
```

En zet deze hook in `~/.claude/settings.json`. Staan daar al instellingen, voeg dan alleen het `SessionStart`-blok toe:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "sh \"$HOME/.claude/hooks/entire-ceda-autoenable.sh\"",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Wat je moet weten over deze hook:

- **Alleen GitHub.** De hook kijkt naar `github.com/cedanl/`. Repo's op git.sdp.surf.nl zet je met de hand aan (stap 2).
- **Eerste chat.** Entire schrijft zijn Claude-hooks pas tijdens de eerste chat in een nieuwe repo. Die eerste chat wordt daardoor waarschijnlijk niet volledig vastgelegd. Vanaf de tweede chat wel.
- **Alleen bij een nieuwe chat.** De hook draait bij de start van een chat, niet als je een bestaande chat hervat.
- **`jq` is niet verplicht.** Zonder `jq` valt het script terug op de projectmap van Claude.

### 4. Controleer of het werkt

1. `entire status` toont `Enabled` en `Checkpoints sync to: dedicated checkpoint remote (cedanl/entire-checkpoints)`.
2. Maak een kleine commit vanuit een chat en draai `git log -1 --format=%B`. Daar hoort een regel `Entire-Checkpoint: <12 tekens>` in te staan.
3. Push de branch. Entire meldt dan `Pushing entire/checkpoints/v1 to checkpoint remote... done`. De branch `entire/checkpoints/v1` komt in `cedanl/entire-checkpoints` terecht, niet in de projectrepo.

Bij de eerste push vanaf een nieuwe Mac kan Entire `Detected disconnected session metadata` melden. Het zet je lokale checkpoints dan bovenop die van het team (`Cherry-picking … onto remote`). Dat is normaal, er gaat niets verloren.

### Waar werkt het wel en niet

| Waar | Entire? |
|------|---------|
| Code-tab in de Claude-app op je Mac | Ja |
| `claude` in de terminal, of de extensie in VS Code of JetBrains | Ja, die gebruiken dezelfde instellingen |
| Chat-tab in de app, of claude.ai in de browser | Nee: geen hooks en geen repo |
| Claude Code in de cloud (claude.ai/code) | Nee: die draait niet op je Mac en ziet je hooks niet |

### Open punt: `checkpoint_remote` committen of niet

Bij elke push meldt Entire:

```
[entire] Note: Checkpoints were pushed to a separate checkpoint remote, but .entire/settings.json does not contain checkpoint_remote in the latest commit.
```

Volgens Entire kan entire.io de checkpoints pas vinden als `.entire/settings.json` met `checkpoint_remote` in de repo is gecommit. De [werkafspraak](../werkafspraken/entire.md) zegt dat `.entire/` lokaal blijft. De checkpoints zelf komen wel gewoon in `cedanl/entire-checkpoints` en zijn via de CLI te lezen. Alleen de koppeling op entire.io ontbreekt. Commit `.entire/` niet op eigen houtje: dat besluit loopt via de eigenaar van de werkafspraak.

## Basisgebruik

### Status controleren

```bash
entire status
```

Toont of Entire actief is, welke agent geconfigureerd is, en waar checkpoints naartoe gaan.

### Checkpoints bekijken

```bash
entire checkpoint list             # alle checkpoints in deze repo
entire checkpoint explain          # leg uit waarom code veranderd is
```

### Herleiden van regels

```bash
entire why <bestand>               # welke prompt heeft dit bestand veroorzaakt?
entire blame <bestand>             # welke regels kwamen uit een checkpoint?
```

> `entire blame` en `entire why` zijn Labs-commando's. Bekijk welke beschikbaar zijn met `entire labs`.

### Sessie hervatten

```bash
entire session resume <branch>     # hervat de laatste sessie op een branch
```

Herstelt de sessiemetadata en toont het commando om verder te gaan.

### Samenvatting

```bash
entire dispatch                    # markdown samenvatting van recent AI-werk
```

## Veiligheid

- **Redactie:** Entire voert automatische redactie uit op cloud-credentials, tokens, sleutels en hoge-entropie strings voordat data wordt opgeslagen.
- **Opslag:** Sessiedata staat op de branch `entire/checkpoints/v1` in de checkpoint-repo. Gebruik je Entire in een repo zonder aparte checkpoint-remote, dan staat die branch in je eigen repo en is de data zichtbaar als die repo publiek is.
- **Lokale sessies:** Tijdens een sessie maakt Entire tijdelijke shadow-branches aan met ongeredacteerde data. Deze worden niet gepusht.
- **Toegang:** De `cedanl/entire-checkpoints` repo is private, maar iedereen met toegang kan alle transcripts lezen. Dat zijn meer mensen dan er schrijven. Laad geen data met persoonsgegevens in een sessie, zie [Feedback zonder persoonsgegevens](../werkafspraken/feedback-zonder-persoonsgegevens.md).

## Troubleshooting

| Probleem | Oplossing |
|----------|-----------|
| `Not a git repository` | Ga eerst naar een Git-repository |
| `Entire is disabled` | Draai `entire enable` |
| `shadow branch conflict` | Draai `entire clean --force` |
| Geen `Entire-Checkpoint:` in je commit | Draai `entire-setup --check`. Start je Claude in de root, dan werkt een container van vóór dev-dots#49 niet voor zustermappen |
| `entire enable` zegt `Git identity is missing` | Draai eerst `onboard` of zet `git config --global user.name` en `user.email` |
| Push of sync naar `entire/checkpoints/v1` botst of de branches lopen uit elkaar | Draai `entire doctor` |
| `checkpoint not found` bij een ID van 26 tekens | Dat checkpoint staat als ref. Controleer of de opslag op `git-refs` staat of haal de refs op: `git fetch origin '+refs/entire/checkpoints/*:refs/entire/checkpoints/*'` |
| SSH-fout bij `session resume` | Voeg GitHub host keys toe: `ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts` |
| `Entire CLI is enabled but not installed or not on PATH` bij de start van een chat (Mac) | `entire` staat niet in je `PATH`. Controleer `entire version` in een nieuwe terminal en voeg de installatiemap toe aan `~/.zshrc` |
| `.claude/settings.json` staat als untracked in `git status` (Mac) | Daar staan de Entire-hooks in. Niet committen; zet `/.claude/settings.json` in `.git/info/exclude` |
| `does not contain checkpoint_remote in the latest commit` bij push | Bekend open punt, zie [Op je eigen Mac](#open-punt-checkpoint_remote-committen-of-niet). De checkpoints zijn wel gepusht |
| `failed to unlock correct collection` | De OS-keyring is niet beschikbaar — gebruik `ENTIRE_TOKEN_STORE=file entire login` |

### Debug-modus

```bash
ENTIRE_LOG_LEVEL=debug entire status
```

### Opschonen

```bash
entire clean --force              # sessiedata voor huidige commit
entire clean --all --force        # alle georkestreerde data
entire disable                    # verwijder hooks (code blijft onaangeroerd)
```

## Bronnen

- [Entire.io documentatie](https://docs.entire.io) — officiële docs
- [entireio/cli](https://github.com/entireio/cli) — broncode (MIT, Go, 5k stars)
- [cedanl/entire-checkpoints](https://github.com/cedanl/entire-checkpoints) — onze centrale checkpoint-repo
- [Werkafspraak Entire](../werkafspraken/entire.md) — de governance-regels
