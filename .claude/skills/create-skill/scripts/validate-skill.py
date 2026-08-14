#!/usr/bin/env python3
"""Validate CEDA skills against the Agent Skills spec plus the CEDA ontology.

Usage:
    python3 validate-skill.py .claude/skills/<name>      # one skill
    python3 validate-skill.py .claude/skills             # every skill in the dir

Exit code 0 = no errors, 1 = at least one error. Warnings never fail the run.

Two rule sets:
  * the spec (agentskills.io/specification) — name/description constraints, the six
    allowed frontmatter fields, custom keys under `metadata:` as strings
  * the CEDA ontology — the `ceda-*` metadata keys and the rules between them

Stdlib only on purpose: it has to run in any repo that received the skill via
`npx skills add cedanl/.github`, without a Python project around it.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

ENUMS = {
    "ceda-type": {"workflow", "reference", "connector"},
    "ceda-subtype": {"knowledge", "presentation"},
    "ceda-origin": {"external", "extended", "own"},
    "ceda-activation": {"ambient", "command", "hook", "scheduled", "chained"},
    "ceda-binding": {"hard", "default", "suggestie"},
    "ceda-execution": {"inline", "isolated", "deterministic"},
    "ceda-scope": {"org", "project"},
    "ceda-verifies": {"measurable", "observable", "none"},
}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESCRIPTION_MAX = 1024
DESCRIPTION_MIN = 80
# Een aangeroepen skill heeft een herkenningsteken nodig, geen handleiding: de gebruiker typt
# `/naam` of de projectinstructies verwijzen ernaar, dus het triggeroppervlak doet weinig werk.
# Een ambient skill moet vuren op geplakte foutmeldingen die niemand aankondigt en mag het volle
# spec-budget gebruiken. Vandaar twee grenzen in plaats van één.
DESCRIPTION_MAX_AANGEROEPEN = 400
ACTIVATION_AANGEROEPEN = {"command", "chained"}
# Mechaniek in een description: paden, bestandsnamen, vlaggen, placeholders. Dit verandert
# zonder dat de trigger verandert, en het staat élke sessie in context.
# Let op: schuine strepen alleen zijn géén pad. `type/origin/scope`, `connector/command` en
# `skill/hook` zijn opsommingen die in een goede description thuishoren. Daarom geen generieke
# slash-regel maar echte signalen: een bekende directorynaam, een placeholder, een
# bestandsextensie of een vlag.
MECHANIEK_PATRONEN = (
    r"(?:^|[\s`(])\.?/?(?:data|docs|src|tests?|scripts|references|assets|\.claude|\.github)/",
    r"[a-z0-9_-]+/<[a-z-]+>",           # repo/<naam>
    r"\.(md|py|json|ya?ml|toml|sh)\b",  # bestandsnamen
    r"\s--[a-z-]{2,}",                  # --flags
    r"<[a-z-]+>",                       # <repo>, <naam>
)
COMPATIBILITY_MAX = 500
BODY_MAX_LINES = 500
BUNDLE_DIRS = ("references", "assets", "scripts")

STOPWORDS = {
    "een", "de", "het", "van", "voor", "met", "bij", "als", "wanneer", "iemand",
    "gebruik", "gebruiken", "wil", "wilt", "naar", "aan", "die", "dat", "deze",
    "wordt", "worden", "over", "door", "uit", "toe", "ook", "niet", "geen",
    "the", "a", "an", "of", "for", "with", "when", "use", "used", "using",
    "this", "that", "and", "or", "to", "in", "on", "is", "are", "it", "you",
    "skill", "skills", "claude", "ceda", "cedanl", "repo", "repos",
}

# An exclusion-clause takes one of two documented forms (references/description-schrijven.md):
# bounding ("niet voor X") or referring ("gebruik dan `andere-skill`"). Matching the marker
# words as bare substrings recognised neither reliably: `buiten` fired inside "buitenwereld",
# "gebruik dan" fired on "gebruik dan deze skill" (which widens the trigger instead of
# bounding it), and "instead" fired on "fill in the template instead of leaving it blank".
# That mattered: it suppressed the overlap warning on the one pair in the collection whose
# descriptions are byte-identical. So the bounding form needs a scope word after it, and the
# referring form has to actually name another skill.
BOUNDING_CLAUSE = re.compile(
    r"\bniet(?: te)? gebruiken (?:voor|bij|als)\b|\bniet voor\b|\bnooit voor\b|"
    r"\bgebruik niet\b|\bnot for\b|\bdo(?:n't| not) use (?:for|when|this)\b",
    re.IGNORECASE,
)
REFERRING_MARKER = re.compile(
    r"\blet op\b|\bin plaats\b|\bgebruik(?: dan| je)?\b|\binstead\b|\brather than\b|\btenzij\b",
    re.IGNORECASE,
)
# A backticked name, or "skill <naam>" — but not "deze/dit/this skill", which points at itself.
NAMES_OTHER_SKILL = re.compile(
    r"`[a-z0-9][a-z0-9_-]*`|(?<!deze )(?<!dit )(?<!this )\bskill\s+[a-z0-9][a-z0-9_-]*\b",
    re.IGNORECASE,
)
CLAUSE_WINDOW = 120

NO_VERIFY_MOTIVATION = re.compile(r"geen verificatie|no verification", re.IGNORECASE)


# --------------------------------------------------------------------------- #
# Minimal frontmatter parser (the spec's subset: scalars, block scalars, one map)
# --------------------------------------------------------------------------- #

def _scalar(raw: str):
    raw = raw.strip()
    if raw in ("~", "null", ""):
        return ""
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [p.strip().strip("'\"") for p in inner.split(",") if p.strip()] if inner else []
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
        return raw[1:-1]
    return raw


def parse_frontmatter(text: str) -> tuple[dict, list[str], str]:
    """Return (fields, errors, body)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["frontmatter ontbreekt (bestand begint niet met `---`)"], text
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, ["frontmatter niet afgesloten met `---`"], text

    data: dict = {}
    errors: list[str] = []
    i, key = 1, None
    while i < end:
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip())

        if indent == 0:
            if ":" not in stripped:
                errors.append(f"frontmatter-regel zonder `:` — {stripped!r}")
                i += 1
                continue
            key, _, value = stripped.partition(":")
            key, value = key.strip(), value.strip()
            if value in (">", ">-", "|", "|-", ">+", "|+"):  # block scalar
                fold = value[0] == ">"
                chunk, i = [], i + 1
                while i < end and (not lines[i].strip() or len(lines[i]) - len(lines[i].lstrip()) > 0):
                    chunk.append(lines[i].strip())
                    i += 1
                data[key] = (" " if fold else "\n").join(c for c in chunk if c)
                continue
            data[key] = _scalar(value) if value else {}
        elif isinstance(data.get(key), dict):  # nested map (metadata:)
            if ":" in stripped:
                k, _, v = stripped.partition(":")
                data[key][k.strip()] = _scalar(v)
            else:
                errors.append(f"ingesprongen regel zonder `:` — {stripped!r}")
        elif isinstance(data.get(key), str):  # continuation of a plain multi-line scalar
            data[key] = f"{data[key]} {stripped}".strip()
        else:
            errors.append(f"ingesprongen regel zonder bijbehorend veld — {stripped!r}")
        i += 1
    return data, errors, "\n".join(lines[end + 1:])


# --------------------------------------------------------------------------- #

@dataclass
class Result:
    name: str
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    legacy: bool = False
    description: str = ""
    declared_name: str = ""

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def trigger_tokens(description: str) -> set[str]:
    words = re.findall(r"[a-zà-ÿ0-9_-]{4,}", (description or "").lower())
    return {w for w in words if w not in STOPWORDS}


def has_exclusion_clause(description: str) -> bool:
    desc = description or ""
    if BOUNDING_CLAUSE.search(desc):
        return True
    return any(
        NAMES_OTHER_SKILL.search(desc[m.start(): m.start() + CLAUSE_WINDOW])
        for m in REFERRING_MARKER.finditer(desc)
    )


# --------------------------------------------------------------------------- #
# Rules
# --------------------------------------------------------------------------- #

def validate_skill(skill_dir: Path) -> Result:
    md = skill_dir / "SKILL.md"
    res = Result(name=skill_dir.name, path=md)
    if not md.exists():
        res.err("geen SKILL.md in de skilldirectory")
        return res

    text = md.read_text(encoding="utf-8")
    fm, parse_errors, body = parse_frontmatter(text)
    for e in parse_errors:
        res.err(e)
    body_lines = len(body.splitlines())

    # --- spec: allowed top-level fields --------------------------------------
    for extra in sorted(set(fm) - SPEC_FIELDS):
        res.err(
            f"`{extra}:` staat op topniveau — de spec kent alleen "
            f"{', '.join(sorted(SPEC_FIELDS))}; eigen velden horen onder `metadata:`"
        )

    # --- spec: name -----------------------------------------------------------
    name = fm.get("name") or ""
    res.declared_name = name
    res.description = fm.get("description") or ""
    if not name:
        res.err("`name` ontbreekt")
    else:
        if len(name) > NAME_MAX:
            res.err(f"`name` is {len(name)} tekens (max {NAME_MAX})")
        if not NAME_RE.match(name):
            res.err(
                f"`name: {name}` voldoet niet aan de spec: alleen a-z, 0-9 en losse "
                "streepjes, niet beginnen of eindigen met een streepje"
            )
        if name != skill_dir.name:
            res.err(f"`name: {name}` wijkt af van de directorynaam `{skill_dir.name}`")

    # --- spec: description ----------------------------------------------------
    desc = res.description
    if not desc:
        res.err("`description` ontbreekt — dit is het enige veld dat activeert")
    else:
        if len(desc) > DESCRIPTION_MAX:
            res.err(f"`description` is {len(desc)} tekens (spec-maximum {DESCRIPTION_MAX})")
        elif len(desc) < DESCRIPTION_MIN:
            res.warn(f"`description` is {len(desc)} tekens — kort; noem expliciete triggerwoorden")
        if re.search(r"\bnieuwe manier\b|\bvanaf nu\b|\bnog steeds\b", desc, re.I):
            res.warn("`description` lijkt tijdsgebonden geformuleerd — dat veroudert stil")
        mechaniek = [m for m in MECHANIEK_PATRONEN if re.search(m, desc)]
        if mechaniek:
            res.warn(
                "`description` bevat mechaniek (paden, bestandsnamen, vlaggen of "
                "placeholders) — dat verandert zonder dat de trigger verandert en hoort "
                "in de body"
            )

    # --- spec: allowed-tools / compatibility ----------------------------------
    tools = fm.get("allowed-tools")
    if isinstance(tools, list):
        res.err("`allowed-tools` is een spatie-gescheiden string in de spec, geen YAML-lijst")
    compat = fm.get("compatibility")
    if isinstance(compat, str) and len(compat) > COMPATIBILITY_MAX:
        res.err(f"`compatibility` is {len(compat)} tekens (max {COMPATIBILITY_MAX})")

    meta_raw = fm.get("metadata")
    meta: dict = meta_raw if isinstance(meta_raw, dict) else {}
    for k, v in meta.items():
        if not isinstance(v, str):
            res.err(f"`metadata.{k}` moet een string zijn (de spec staat alleen string-waarden toe)")

    # Skills that predate the schema: report once, skip the CEDA rules.
    if not any(k.startswith("ceda-") for k in meta):
        res.legacy = True
        if body_lines > BODY_MAX_LINES:
            res.warn(f"SKILL.md-body is {body_lines} regels (richtlijn {BODY_MAX_LINES})")
        return res

    # --- CEDA: enums ----------------------------------------------------------
    for key, allowed in ENUMS.items():
        value = meta.get(key, "")
        if key == "ceda-subtype":
            continue
        if value not in allowed:
            res.err(f"`metadata.{key}` moet een van {sorted(allowed)} zijn, niet {value!r}")

    stype = meta.get("ceda-type", "")
    subtype = meta.get("ceda-subtype", "")
    if stype == "reference":
        if subtype not in ENUMS["ceda-subtype"]:
            res.err(f"`ceda-type: reference` vereist `ceda-subtype` uit {sorted(ENUMS['ceda-subtype'])}")
    elif subtype:
        res.err(f"`ceda-subtype: {subtype}` mag alleen bij `ceda-type: reference`")

    origin = meta.get("ceda-origin", "")
    if origin == "extended" and not meta.get("ceda-upstream"):
        res.err("`ceda-origin: extended` zonder `ceda-upstream` — benoem de bron-skill, anders is bijwerken onmogelijk")
    if origin != "extended" and meta.get("ceda-upstream"):
        res.warn("`ceda-upstream` ingevuld terwijl `ceda-origin` niet `extended` is")

    source = meta.get("ceda-source", "")
    if not source:
        res.err("`ceda-source` ontbreekt — leeg betekent 'geen bron' én 'nog niet ingevuld'; gebruik `self`, een pad, een url of `intern:<vindplaats>`")
    elif source.startswith("intern:"):
        res.warn("`ceda-source: intern:` — controleer dat de skill zelfstandig leesbaar is; wie 'm laadt kan de bron mogelijk niet openen")

    scope = meta.get("ceda-scope", "")
    if scope == "user" and subtype == "knowledge":
        res.err("`ceda-scope: user` mag alleen `presentation` dragen, nooit `knowledge`")
    if source == "self" and scope == "project":
        res.err("`ceda-source: self` hoort op `ceda-scope: org` — is de skill de bron, dan is hij gedeeld")

    if (
        meta.get("ceda-activation") in ACTIVATION_AANGEROEPEN
        and len(res.description) > DESCRIPTION_MAX_AANGEROEPEN
    ):
        res.warn(
            f"`description` is {len(res.description)} tekens bij "
            f"`ceda-activation: {meta.get('ceda-activation')}` (richtlijn "
            f"{DESCRIPTION_MAX_AANGEROEPEN}) — een aangeroepen skill heeft een "
            "herkenningsteken nodig, geen handleiding; verplaats de mechaniek naar de body"
        )

    if meta.get("ceda-binding") == "hard" and meta.get("ceda-activation") != "hook":
        res.err("`ceda-binding: hard` zonder `ceda-activation: hook` — zonder afdwinging is dit `default` met een mooie titel")

    if meta.get("ceda-verifies") == "none" and not NO_VERIFY_MOTIVATION.search(body):
        res.err("`ceda-verifies: none` vereist een expliciete motivatie in de body")

    if not tools:
        msg = "`allowed-tools` ontbreekt — benoem wat de skill mag aanraken"
        (res.err if origin == "external" else res.warn)(
            msg + (" (verplicht bij `ceda-origin: external`)" if origin == "external" else "")
        )

    if not meta.get("ceda-id"):
        res.warn("`ceda-id` ontbreekt — zonder stabiele identiteit valt de evaluatie over repo's heen om")
    if not meta.get("ceda-version"):
        res.warn("`ceda-version` ontbreekt — nodig om waarnemingen te aggregeren")

    # --- bundles: elk meegeleverd bestand moet in de body genoemd worden ------
    bundled: list[str] = []
    for d in BUNDLE_DIRS:
        sub = skill_dir / d
        if not sub.is_dir():
            continue
        bundled += [f"{d}/{p.name}" for p in sorted(sub.iterdir())
                    if p.is_file() and not p.name.startswith(".")]
    unmentioned = [b for b in bundled if b not in body]
    for b in unmentioned:
        res.err(f"`{b}` wordt nergens in de body genoemd — een bundle zonder laadconditie laadt nooit")
    if body_lines > BODY_MAX_LINES:
        (res.warn if bundled else res.err)(
            f"SKILL.md-body is {body_lines} regels (richtlijn {BODY_MAX_LINES})"
            + ("" if bundled else " en er zijn geen gebundelde bestanden — splits het zeldzame deel af")
        )

    return res


def check_duplicate_names(results: list[Result]) -> None:
    """Two directories claiming the same `name` in their frontmatter.

    The per-skill name!=directory rule catches this only by accident, and only
    on the copy that was renamed. Stating it as its own error names the actual
    problem: there are two artefacts competing for one identity, so `ceda-id`,
    the evaluation and every cross-reference land on whichever one wins.
    """
    by_declared: dict[str, list[Result]] = {}
    for r in results:
        if r.declared_name:
            by_declared.setdefault(r.declared_name, []).append(r)
    for declared, group in by_declared.items():
        if len(group) < 2:
            continue
        dirs = ", ".join(f"`{r.name}`" for r in group)
        for r in group:
            r.err(
                f"`name: {declared}` wordt door meerdere directories geclaimd ({dirs}) — "
                "twee kopieën van één identiteit; voeg samen of deprecate, zie `dedup-skills`"
            )


def check_overlap(results: list[Result]) -> None:
    """Overlapping trigger words without an exclusion-clause on either side.

    Words that show up in a large share of all descriptions ("maak", "levert",
    "altijd") carry no trigger signal in this collection, so they are dropped
    corpus-wide before comparing. That keeps the check language-agnostic instead
    of depending on an ever-growing stopword list.
    """
    tokens = {r.name: trigger_tokens(r.description) for r in results if r.description}
    if len(tokens) >= 10:
        df: dict[str, int] = {}
        for toks in tokens.values():
            for t in toks:
                df[t] = df.get(t, 0) + 1
        ceiling = max(2, int(0.12 * len(tokens)))
        common = {t for t, n in df.items() if n > ceiling}
        tokens = {name: toks - common for name, toks in tokens.items()}

    by_name = {r.name: r for r in results}
    seen: set[tuple[str, str]] = set()
    for a, ta in tokens.items():
        for b, tb in tokens.items():
            if a >= b:
                continue
            shared = ta & tb
            if len(shared) < 4 or (a, b) in seen:
                continue
            seen.add((a, b))
            for name, other in ((a, b), (b, a)):
                r = by_name[name]
                if not has_exclusion_clause(r.description):
                    r.warn(
                        f"overlappende triggerwoorden met `{other}` "
                        f"({', '.join(sorted(shared)[:5])}) en geen exclusion-clause in de description"
                    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    target = Path(argv[1])
    if not target.exists():
        print(f"pad bestaat niet: {target}")
        return 2

    if (target / "SKILL.md").exists():
        dirs, cross = [target], False
    else:
        dirs = sorted(p for p in target.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
        cross = True
        if not dirs:
            print(f"geen skills gevonden onder {target}")
            return 2

    results = [validate_skill(d) for d in dirs]
    if cross:
        check_duplicate_names(results)
        check_overlap(results)

    n_err = n_warn = n_legacy = 0
    for r in results:
        if r.legacy:
            n_legacy += 1
        if not (r.errors or r.warnings):
            print(f"OK       {r.name}")
            continue
        label = "LEGACY" if r.legacy else ("FOUT" if r.errors else "WAARSCHUWING")
        print(f"{label:8} {r.name}")
        if r.legacy:
            print("         · nog niet gemigreerd naar het CEDA-schema (alleen spec-velden)")
        for e in r.errors:
            print(f"         ✗ {e}")
            n_err += 1
        for w in r.warnings:
            print(f"         ! {w}")
            n_warn += 1

    print(f"\n{len(results)} skill(s) — {n_err} fout(en), {n_warn} waarschuwing(en), {n_legacy} nog niet gemigreerd")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
