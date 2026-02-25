# CEDA Technical Standards

Technical standards for the [cedanl](https://github.com/cedanl) organization. These documents define how we build, structure, and maintain our R and Python repositories for educational analytics.

## Standards
Follow the CEDA technical standards at https://github.com/cedanl/.github/tree/main/standards. These be reference from `CLAUDE.md` as well.
- [Principles](https://github.com/cedanl/.github/blob/main/standards/principles.md)
- [Project Structure](https://github.com/cedanl/.github/blob/main/standards/project-structure.md)
- [Data Conventions](https://github.com/cedanl/.github/blob/main/standards/data-conventions.md)
- [R Style Guide](https://github.com/cedanl/.github/blob/main/standards/r-style.md) (for R repos)
- [Python Style Guide](https://github.com/cedanl/.github/blob/main/standards/python-style.md) (for Python repos)

## How to Use

### For developers
Read through the principles first, then the relevant project structure for your repo type. Reference these standards when starting new repos or reviewing code.

### With Claude Code

These standards are also available as Claude Code skills for interactive use:

| Skill | Command | Description |
|-------|---------|-------------|
| Init Repo | `/init-repo` | Scaffold a new repo with the correct CEDA structure |
| Check Style | `/check-style` | Review code against R or Python style standards |
| Migrate Cookiecutter | `/migrate-cookiecutter` | Convert cookiecutter data science repos to CEDA package standard |

Skills live in `.claude/skills/` in this repo. To use them, reference this repo from your project's `CLAUDE.md`:

```markdown
## Standards
Follow CEDA technical standards: https://github.com/cedanl/.github/tree/main/standards/README.md
```

## Scope

These standards apply to repositories being scaled up by the central CEDA team, particularly around:
- **Dropout analysis**: Uitnodigingsregel, 1cijferho, no-fairness-without-awareness, 1cho_ins_preparation_r
- **Enrollment forecasting**: instroomprognose-mbo, student-instroom-mbo, dashboard-instroomprognose-mbo

This is a vision document. Existing repos may not yet fully conform to these standards.
