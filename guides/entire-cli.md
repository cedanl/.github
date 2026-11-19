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

### macOS (Homebrew)

```bash
brew tap entireio/tap
brew trust entireio/tap
brew install --cask entire
```

### Linux

```bash
curl -fsSL https://entire.io/install.sh | bash
```

Voor ARM64:

```bash
curl -LO https://github.com/entireio/cli/releases/latest/download/entire-linux-arm64.tar.gz
tar -xzf entire-linux-arm64.tar.gz
sudo mv entire /usr/local/bin/
```

### Windows (Scoop)

```bash
scoop bucket add entire https://github.com/entireio/scoop-bucket.git
scoop install entire/entire
```

### Vanuit bron (Go 1.21+)

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

De `claude`-functie in de container voert automatisch het volgende uit bij het starten:

1. `entire enable -y --agent claude-code` — installeert de hooks
2. `entire configure --checkpoint-backend branch --checkpoint-remote github:cedanl/entire-checkpoints` — kiest de opslag (branch) en wijst de checkpoint-repo aan
3. Start Claude Code met `--dangerously-skip-permissions`

Dit gebeurt alleen in CEDA-repos: waar `origin` `cedanl/` bevat (GitHub) of `surf-internal/npuls/ceda/` (GitLab, git.sdp.surf.nl). Checkpoints van beide gaan naar dezelfde GitHub-repo, want Entire kent als checkpoint-remote alleen GitHub. Dit gebeurt bij elke start van `claude`, dus `entire disable` blijft niet staan.

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
| Push of sync naar `entire/checkpoints/v1` botst of de branches lopen uit elkaar | Draai `entire doctor` |
| `checkpoint not found` bij een ID van 26 tekens | Dat checkpoint staat als ref. Controleer of de opslag op `git-refs` staat of haal de refs op: `git fetch origin '+refs/entire/checkpoints/*:refs/entire/checkpoints/*'` |
| SSH-fout bij `session resume` | Voeg GitHub host keys toe: `ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts` |
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
