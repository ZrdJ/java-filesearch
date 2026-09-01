---
name: spec
version: 3
description: Spec-driven Arbeiten nach OpenSpec-Format, ohne dessen CLI. Legt Changes an (proposal, Delta-Spec, design, tasks), arbeitet sie ab, prueft Code gegen Spec und archiviert inklusive Delta-Merge in die Ist-Spec. Triggers auf Spec, Anforderung, Akzeptanzkriterium, Change, Vorhaben, Feature planen, propose, verify, archivieren, Scope-Creep, "was soll gebaut werden".
# GENERIERT aus personal/skills-ref/spec/ — nicht hier editieren; Aenderungen gehoeren nach ~/.claude/skills-ref/spec/.
source: personal-provider-ref
ref-hash: sha256:2077ef1d72d4c36ad3500b5e7f7a461914659572a77bd41ba73d7b0c53c85b31
---

# spec

Der Anforderungs-Layer des `docs/`-Verzeichnisses. Vier Phasen, jede mit eigener Detaildatei.

## Das eine Prinzip

Zwei Sorten Dokument, die man nicht verwechseln darf:

| | `specs/` | `changes/` |
|---|---|---|
| Aussage | das System **tut** heute X | das System **soll** kuenftig Y tun |
| Lebensdauer | langlebig, wird fortgeschrieben | endet mit dem Archivieren |
| Aenderung | **nur** beim Archivieren eines Changes | laufend waehrend der Umsetzung |

**Die Ist-Spec wird nie direkt editiert.** Sie aendert sich ausschliesslich dadurch, dass ein Change archiviert und sein Delta eingearbeitet wird. Das ist die ganze Disziplin des Modells. Wer die Ist-Spec „mal eben" anfasst, hat ab dann zwei Wahrheiten und keine Moeglichkeit mehr zu pruefen, welche stimmt.

## Braucht das ueberhaupt einen Change?

Eine Frage entscheidet: **aendert sich ein Szenario in `specs/`?**

- **Nein** → kein Change. Direkt umsetzen. Gilt fuer Bugfix (das Szenario galt schon, es war nur kaputt), Refactor ohne Verhaltensaenderung, Dependency-Update, Formatierung.
- **Ja** → Change. Auch wenn es „nur eine Kleinigkeit" ist. Genau die Kleinigkeiten sind es, die spaeter niemand mehr begruenden kann.

Grenzfall Bugfix: deckt der Fix ein Verhalten auf, das nie spezifiziert war, ist das ein Change — nicht weil der Fix gross ist, sondern weil die Spec unvollstaendig war.

## Die vier Phasen

| Phase | Was passiert | Detail |
|---|---|---|
| **1 · propose** | Vorhaben beschreiben: Problem, Loesung, Nicht-im-Scope, Delta-Spec, Slices | [`references/propose.md`](references/propose.md) |
| **2 · apply** | Slices abarbeiten, Richtungswechsel anhaengen | [`references/apply.md`](references/apply.md) |
| **3 · verify** | Code gegen Spec pruefen: fehlt was, ist zu viel drin, stimmt es wirklich | [`references/verify.md`](references/verify.md) |
| **4 · archive** | Delta in die Ist-Spec mergen, Change wegraeumen | [`references/archive.md`](references/archive.md) |

Die Phasen sind **nicht** streng sequenziell. Ein Richtungswechsel in Phase 2 aendert die Delta-Spec aus Phase 1; `verify` darf jederzeit laufen, nicht erst am Ende. Was nicht verhandelbar ist: **archivieren erst nach verify**, und die Ist-Spec aendert sich nur dort.

Mit `records: true` auf der Ebene prueft Phase 3 **beides in einem Lauf**: die Kette Anforderung ↔ Test und die Kette Datensatz ↔ Entscheidung. Ein `origin:`, das auf keinen Themenblock aufloest, bricht den Lauf genauso wie ein toter `[impl->req~…]`. Ohne den Schalter faellt der zweite Teil still weg. Warum das zusammengehoert: eine Anforderung ohne Test ist unbelegt, eine Entscheidung ohne Ausloeser ist unbegruendet — beides ist dieselbe Sorte Luecke, nur an verschiedenen Enden derselben Kette.

## Wie Anforderungen aussehen

Vollstaendig in [`references/anforderungen.md`](references/anforderungen.md) — inklusive Antipatterns. Die Kurzform:

```markdown
### Requirement: Artikelstammdaten koennen als CSV importiert werden
`req~artikelimport.csv-import~1`

Das System muss CSV-Dateien mit Artikelstammdaten einlesen und die
enthaltenen Artikel anlegen oder aktualisieren.

#### Scenario: Datei mit fehlerhaften Zeilen

- **WENN** eine CSV hochgeladen wird, in der Zeile 12 eine unbekannte Warengruppe nennt
- **DANN** werden die uebrigen Zeilen importiert
- **UND** Zeile 12 wird mit Grund im Fehlerprotokoll ausgewiesen
- **UND** der Import wird nicht abgebrochen
```

Vier harte Regeln:

1. **Nur `muss`/`must`, `wird`/`will`, `kann`/`can`** — deutsch oder englisch je nach `lang:` der Ebene, innerhalb eines Dokuments nicht gemischt; volle Tabelle inklusive Verboten-Liste je Sprache in [`references/anforderungen.md`](references/anforderungen.md). Kein „sollte"/„should", „moeglichst"/„where possible", „idealerweise"/„ideally", „zeitnah"/„promptly". Was nicht pruefbar formuliert ist, ist kein Kriterium.
2. **Jede Anforderung braucht mindestens ein Szenario.** Ohne Szenario ist es eine Absichtserklaerung.
3. **Ein Begriff, eine Bedeutung.** Keine Synonymketten. Der Kunde sagt „Warengruppe" → es heisst ueberall „Warengruppe", auch wenn die Tabelle `category` heisst.
4. **Jede Anforderung traegt eine Kennung** in einer eigenen Backtick-Zeile unter der Ueberschrift. Sie wird von Hand vergeben und danach eingefroren; der Merge beim Archivieren sucht ueber sie, und Tests verweisen darauf.

**Die Kennung gehoert nicht diesem Skill.** Wie sie gebildet wird, wann die Revision steigt, was bei abgeloesten Anforderungen passiert und wie ein Test auf sie zeigt, steht im Skill `traceability`. Hier steht nur, dass sie da sein muss und wo sie hingehoert — die Regeln stehen einmal, nicht zweimal.

## Ordner

```
docs/
├── specs/{capability}/spec.md          Ist-Zustand
├── changes/{YYYY-MM-DD}-{slug}/
│   ├── proposal.md                     Warum + Scope
│   ├── specs/{capability}/spec.md      Delta: ADDED / MODIFIED / REMOVED
│   ├── design.md                       nur bei nicht-offensichtlicher Technik
│   └── tasks.md                        Slices
├── archive/{YYYY-MM}/{slug}/
└── records/                            Datensaetze, nur mit records: true
    ├── persons/{id}.md
    └── meetings/{YYYY-MM-DD}-{slug}.md
```

`{capability}` ist eine **fachliche** Faehigkeit, kein Modul: `article-import`, `quoting`, `approval`. Nicht `api`, nicht `frontend`, nicht `database`. Test: kann der Kunde den Namen verstehen? Nein → falscher Schnitt.

**Der Name ist englisch, auch wenn der Inhalt der Ebene deutsch ist.** Er ist ein Ordnername und damit Struktur — die Ablage soll ueber alle Projekte gleich aussehen, unabhaengig von der Inhaltssprache. Dasselbe gilt fuer die Slugs der Vorhaben unter `changes/`, `wayfinding/` und `archive/`. Weil der Name zugleich als erste Komponente jeder Kennung steht (`req~approval.…`), wird er einmal vergeben und danach nicht mehr angefasst.

Wo `docs/` liegt, entscheidet die Ablageregel der jeweiligen Ebene — sie steht in der `CLAUDE.md`, die dort gilt, nicht in diesem Skill.

## Vorlagen

Kopierfertig unter [`templates/`](templates/) — **kopieren, nicht nachbauen**:

| Datei | Wofuer |
|---|---|
| `templates/proposal.md` | Phase 1, Kopf eines Changes |
| `templates/spec-delta.md` | Phase 1, die Delta-Spec |
| `templates/design.md` | Phase 1/2, Technik + Test-Seams |
| `templates/tasks.md` | Phase 1, Slice-Tabelle |
| `templates/spec.md` | Ist-Spec, beim Anlegen einer neuen Faehigkeit |

## Vollstaendiges Beispiel

[`beispiel/`](beispiel/README.md) zeigt einen Change von Ende zu Ende: Ist-Spec **vorher**, Proposal mit `origin:`, Delta mit allen drei Markern, Design mit Test-Seams, Slices — und die Ist-Spec **nachher**.

Bei Unsicherheit ueber den Delta-Merge dort nachsehen, nicht raten. `vorher/` + Delta = `nachher/` ist nachrechenbar; Prosa erklaert das schlechter als ein Vorher/Nachher.

## In einen anderen Workspace heben

[`references/uebertragen.md`](references/uebertragen.md) listet, was ortsspezifisch ist und beim Kopieren angepasst werden muss. Der Rest ist generisch.
