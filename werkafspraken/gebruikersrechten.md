# Gebruikersrechten

**Niveau:** Verplicht · **Eigenaar:** [@Tomeriko96](https://github.com/Tomeriko96) · **Akkoord:** [@CorneeldH](https://github.com/CorneeldH)

## De afspraak

Je nodigt een niet-admin teamlid uit op de repo waar het aan werkt, in de rol **Maintainer**. Toegang regel je per repo, niet org-breed.

## Waarom

- **Minimale rechten.** Iemand krijgt toegang tot de repo's waar het nodig is, niet tot de hele org.
- **Duidelijkheid.** Per repo staat zwart op wit wie daar bij kan — handig bij een audit en bij vertrek.
- **Geen onnodige admin.** We geven geen org-admin aan mensen die aan één repo werken; dat is meer macht dan het werk vergt.

## In de praktijk

- Ga in de repo naar `Settings > Collaborators and teams > Manage access > Add People`.
- Kies bij **Role** `Maintainer` en nodig het teamlid uit.
- Een Maintainer mag branches beschermen, releases doen en collaborators beheren binnen die repo, maar geen org-instellingen aanraken.
- **Iemand vertrekt of wisselt van repo?** Verwijder de toegang op dezelfde plek, zodat de lijst klopt.
- **Meer rechten nodig dan Maintainer** (bijvoorbeeld org-settings)? Dat is de uitzondering, zie Afwijken.

## Achtergrond

- [GitHub Docs — Repository roles for an organization](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization) — wat een Maintainer wel en niet mag.
- [project_algemeen #3 — Gebruikersrechten regelen](https://github.com/cedanl/project_algemeen/issues/3) — de afspraak komt voort uit dit issue; de resolution note beschrijft de gekozen methode.

## Afwijken

Org-admin-toegang of een andere rol dan Maintainer regel je via [@Tomeriko96](https://github.com/Tomeriko96), met akkoord van [@CorneeldH](https://github.com/CorneeldH).
