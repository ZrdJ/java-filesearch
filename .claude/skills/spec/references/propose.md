# Phase 1 — propose

Ein Vorhaben beschreiben, bevor Code entsteht. Ergebnis ist ein Verzeichnis `docs/changes/{YYYY-MM-DD}-{slug}/`.

## Vorher: steht der Weg ueberhaupt fest?

**Erste Vorbedingung, gleichrangig zum Abgleich gegen Verworfenes.** Ein Proposal setzt voraus, dass Problem, Loesung und Scope feststehen. Steht das nicht fest, wird kein Change angelegt, sondern eine Wegfindung eroeffnet: `docs/wayfinding/{YYYY-MM-DD}-{slug}/`, Skill `wayfinder`.

Kommt das Vorhaben aus einer **abgeschlossenen** Karte, wird sie im Frontmatter unter `origin:` genannt — im selben Referenz-Schema, das die Ebene sonst fuer Herkunft nutzt.

## Vorher: gegen Verworfenes abgleichen

**Zweite Vorbedingung, ebenfalls vor der ersten Datei.** `docs/project/decisions/` nach `status: rejected` durchsehen. Kommt ein Thema zurueck, das schon einmal abgelehnt wurde, nicht stillschweigend neu aufsetzen, sondern benennen:

> „Das entspricht `2026-06-02-eigener-pdf-renderer.md` — damals verworfen, weil […]. Gilt die Begruendung noch?"

Antwortet der User „ja, trotzdem", ist das eine neue Entscheidung und die alte geht auf `status: superseded`.

## Dateien anlegen

```
docs/changes/2026-08-11-artikelimport/
├── proposal.md                          templates/proposal.md
├── specs/artikelimport/spec.md          templates/spec-delta.md
├── design.md                            templates/design.md   (nur wenn noetig)
└── tasks.md                             templates/tasks.md
```

Slug: kurz, fachlich, kebab-case. Datum ist das des Anlegens und aendert sich nie — auch nicht, wenn der Change Monate laeuft.

`design.md` **weglassen**, wenn die Technik offensichtlich ist. Ein leeres Template ist schlechter als keine Datei. Anlegen, sobald es eine Entscheidung gibt, die jemand spaeter hinterfragt.

## proposal.md

Vier Abschnitte tragen die Arbeit:

**`## Problem`** — aus **Nutzersicht**, nicht aus Systemsicht. Was geht heute nicht, oder was kostet zu viel. Kein „wir haben keine Import-Funktion" (das ist die Loesung, negiert), sondern „Artikelstammdaten werden heute einzeln von Hand angelegt, ein Sortimentswechsel kostet zwei Tage".

**`## Solution`** — ebenfalls aus Nutzersicht. Was kann der Nutzer danach, was vorher nicht ging. Keine Technik.

**`## Out of Scope`** — der wichtigste Abschnitt. Was bewusst draussen bleibt und warum. Er ist die Grundlage jeder spaeteren Nachtragsdiskussion; fehlt er, ist jede Erweiterung „war doch klar, dass das dazugehoert".

Gut gefuellt sieht er so aus:

```markdown
## Out of Scope

- **Export.** Nur Import. Export ist ein eigenes Vorhaben.
- **Bildzuordnung.** Artikelbilder bleiben unberuehrt, auch wenn die CSV
  Dateinamen enthaelt.
- **Automatischer Import per Zeitplan.** Manuell angestossen. Automatik
  erst, wenn der manuelle Weg im Betrieb steht.
```

**`## Open Questions`** — Ausnahme, kein Sammelbecken. Hier steht nur, was **bewusst offen gelassen** ist, typischerweise weil die Antwort bei einem Dritten liegt (Kunde, Betreiber). Alles **Ungeklaerte**, an dem die Umsetzbarkeit haengt, gehoert nicht hierher, sondern in eine Wegfindung (`docs/wayfinding/`). Test: haengt ein Slice daran, ob die Frage so oder anders beantwortet wird, ist es kein offener Punkt, sondern eine Wegfindung.

## Frontmatter

```yaml
---
type: change
title: CSV-Import fuer Artikelstammdaten
updated: 2026-08-11
status: draft | active | fulfilled | rejected
projects: [artikelimport]
origin: [{Referenz-ID}]
---
```

- **`status`** beschreibt den **Vertrag**, nicht den Fortschritt. `draft` = in Verhandlung, `active` = gilt und wird umgesetzt, `fulfilled` = archiviert, `rejected` = kommt nicht. Wie weit die Umsetzung ist, steht in `tasks.md`.
- **`origin`** nennt die nachvollziehbare Quelle, die das Vorhaben ausgeloest hat — im Referenz-Schema, das die Ebene dafuer fuehrt (z. B. eine Meeting-Themenblock-ID, ein Ticket, ein Protokoll-Verweis). Leer lassen, wenn es keine gibt — nicht erfinden. Bei rekonstruierten Vorhaben: `[rekonstruiert]`.
- **`projects`** ist der Projektbezug, wenn ein Repo mehrere Projekte fuehrt (Monorepo-Fall). Er entsteht hier, nicht ueber den Pfad.

## Delta-Spec schreiben

In `specs/{capability}/spec.md` des Changes — **nicht** in der Ist-Spec. Drei Marker, jeder optional, Reihenfolge fest:

```markdown
## ADDED Requirements

### Requirement: {…}
`req~{capability}.{kurzname}~1`
…

## MODIFIED Requirements

### Requirement: {Titel, darf vom bisherigen abweichen}
`req~{capability}.{kurzname}~{revision}`
{vollstaendiger neuer Text — nicht nur die Aenderung}

Previously: {ein Satz, was vorher galt}

## REMOVED Requirements

### Requirement: {Titel}
`req~{capability}.{kurzname}~{revision}`
Reason: {warum sie wegfaellt}
Superseded by: `req~{…}~1`   {nur wenn eine andere an ihre Stelle tritt}
```

Vier Regeln, an denen der spaetere Merge haengt:

1. **Bei MODIFIED und REMOVED muss die Kennung der in der Ist-Spec entsprechen.** Der Merge sucht ueber sie, nicht ueber den Titel — der Titel darf sich geaendert haben. Eine abweichende Kennung erzeugt stillschweigend eine Dublette statt einer Aenderung.
2. **Jede Anforderung traegt ihre Kennung in einer eigenen Backtick-Zeile** unter der Ueberschrift. Kurzname von Hand vergeben, danach eingefroren; Regeln im Skill `traceability`.
3. **MODIFIED traegt den vollstaendigen neuen Text**, nicht ein Diff-Fragment. Beim Archivieren wird ersetzt, nicht gepatcht.
4. **Betrifft der Change mehrere Faehigkeiten**, gibt es mehrere Dateien: `specs/artikelimport/spec.md`, `specs/freigabeprozess/spec.md`. Nicht alles in eine.

Neue Faehigkeit → nur `## ADDED Requirements`, und beim Archivieren entsteht `docs/specs/{capability}/spec.md` aus `templates/spec.md`.

## tasks.md — Slices

```markdown
| # | Slice | Project | Blocked by | Status |
|---|---|---|---|---|
| 01 | CSV-Parser + Validierung | artikelimport | — | open |
| 02 | Upload-Endpoint + Fehlerprotokoll | artikelimport | 01 | open |
| 03 | Upload-Maske | artikelimport | 02 | open |
```

- **Vertikal schneiden.** Jeder Slice ist fuer sich lauffaehig und bringt beobachtbaren Nutzen. Nicht „erst alle Models, dann alle Endpoints" — das ergibt drei Slices, von denen zwei nichts koennen.
- **Nummer ist die Reihenfolge.** Sie aendert sich nicht; neue Slices haengen hinten an, auch wenn sie fachlich dazwischen gehoeren.
- **`Project`** loest den Monorepo-Fall: eine Session im Unterordner sieht, welche Zeilen ihre sind. Bei einem Ein-Projekt-Repo kann die Spalte weg.
- **Status**: `open` · `in progress` · `done`. Anzeige, nicht Wahrheit — die Wahrheit ist `git log`, siehe [`archive.md`](archive.md).

## Fertig, wenn

- [ ] `## Out of Scope` ist gefuellt und nennt mindestens einen echten Ausschluss
- [ ] jede Anforderung im Delta hat mindestens ein Szenario
- [ ] keine verbotenen Modalverben (siehe [`anforderungen.md`](anforderungen.md))
- [ ] jede Anforderung traegt eine Kennung, und die Kurznamen sind je Faehigkeit eindeutig
- [ ] MODIFIED/REMOVED-Kennungen finden sich in der Ist-Spec wieder
- [ ] `origin:` gefuellt oder bewusst leer
- [ ] Slices sind vertikal und einzeln lauffaehig
- [ ] offene Fragen sind bewusst offen gelassen, nicht ungeklaert — Ungeklaertes mit Slice-Abhaengigkeit steht in einer Wegfindung, nicht hier

Danach `status: active` und Phase 2.
