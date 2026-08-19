# Entire CLI — Handleiding

Entire is een Git-natieve tool die AI-sessies (prompts, tool calls, transcripts) vastlegt naast je commits. Elke wijziging is herleidbaar naar de prompt die hem veroorzaakte. De CLI is open source ([entireio/cli](https://github.com/entireio/cli), MIT-licentie, Go).

Voor de governance-regels zie de [werkafspraak Entire](../werkafspraken/entire.md).

## Hoe het werkt

Entire installeert Git-hooks in je repository die sessiedata vastleggen terwijl je werkt. Bij een `git commit` wordt een **checkpoint** aangemaakt — een snapshot van de volledige sessiecontext (prompts, tool-calls, gewijzigde bestanden, transcripts).

Checkpoint-data wordt opgeslagen op een aparte branch `entire/checkpoints/v1`, zodat je git-historie schoon blijft. Alleen een 12-tekens ID (bijv. `a3b2c4d5e6f7`) verschijnt als `Entire-Checkpoint`-trailer in je commit message.

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
2. `entire configure --checkpoint-remote github:cedanl/entire-checkpoints` — wijst de checkpoint-repo aan
3. Start Claude Code met `--dangerously-skip-permissions`

Dit gebeurt alleen in repos waar `origin` met `cedanl/` begint.

### Centrale checkpoint-repo

Alle checkpoints worden gesynchroniseerd naar **`cedanl/entire-checkpoints`**. Dit is een private repo waar de sessiedata van alle teamleden samenkomt. Bij een `git push` wordt de `entire/checkpoints/v1` branch automatisch meegestuurd.

### Configuratie

De configuratie staat in `.entire/settings.json` (gecommit in dev-dots):

```json
{
  "enabled": true,
  "strategy_options": {
    "checkpoint_remote": {
      "provider": "github",
      "repo": "cedanl/entire-checkpoints"
    }
  }
}
```

Persoonlijke overrides kunnen in `.entire/settings.local.json` (niet gecommit).

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
- **Opslag:** Sessiedata staat in je git-repo op de `entire/checkpoints/v1` branch. Als je repo publiek is, is deze data zichtbaar.
- **Lokale sessies:** Tijdens een sessie maakt Entire tijdelijke shadow-branches aan met ongeredacteerde data. Deze worden niet gepusht.
- **Toegang:** De `cedanl/entire-checkpoints` repo is private; alleen cedanl-leden hebben toegang.

## Troubleshooting

| Probleem | Oplossing |
|----------|-----------|
| `Not a git repository` | Ga eerst naar een Git-repository |
| `Entire is disabled` | Draai `entire enable` |
| `shadow branch conflict` | Draai `entire clean --force` |
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
