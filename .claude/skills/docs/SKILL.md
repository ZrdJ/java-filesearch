---
name: docs
version: 7
description: Wegweiser fuer den docs/-Wissens-Layer. Entscheidet, auf welcher Ebene eine Note liegt (Workspace / Sub-Bereich / Repo) und was stattdessen in die Datenhaltung des Providers gehoert, liefert Frontmatter-Schema und Template je Note-Typ (Entscheidung, Arbeitslog, Spec, Change, Karte, Ticket, Artefakt). Triggers auf docs/, Entscheidung festhalten, ADR, Arbeitslog, Wegfindung, Karte, offene Frage, veroeffentlichte Seite ablegen, "wo gehoert das hin".
# GENERIERT aus personal/skills-ref/docs/ — nicht hier editieren; Aenderungen gehoeren nach ~/.claude/skills-ref/docs/.
source: personal-provider-ref
ref-hash: sha256:14affee1f1c6b038392d14e00dc658d984d328b1f66ab43a1b164251ae8a41e5
---

# docs

Der `docs/`-Layer ersetzt in diesem Workspace den Vault. Dieser Skill beantwortet zwei Fragen: **wo liegt es** und **wie sieht es aus**. Lifecycle-Mechanik fuer Changes steht in `spec`, Meeting-Erfassung in `meeting`.

## 1. Ebene bestimmen — erste zutreffende Frage gewinnt

| # | Frage | Ablage |
|---|---|---|
| 1 | **Datensatz** — Person, Firma, Termin, Projekt, Todo, erfasste Zeit? | Datenhaltung des Providers (CRM, MCP-Tools, o.ae.) — **nicht** `docs/`. Welche das konkret ist, steht in der CLAUDE.md des Providers. |
| 2 | Arbeitsweise/Konfiguration statt Produkt? | `~/.claude/docs/` — **ausserhalb** dieses Workspaces |
| 3 | Betrifft mehr als einen Sub-Bereich? | `CLAUDE.md` des WS-Roots, nicht `docs/` |
| 4 | Betrifft einen Sub-Bereich als Ganzes? | `{sub-bereich}/docs/` |
| 5 | Genau ein Repo? | `{sub-bereich}/{repo}/docs/` |

Frage 1 ist die wichtigste, weil sie am haeufigsten falsch beantwortet wird. Die Trennlinie ist **Datensatz vs. Dokument**:

> Die Datenhaltung des Providers haelt den **Termin** und die **Person**. Die `docs/` halten die **Entscheidung**, die daraus folgte. Das Gespraech ist Quelle, die Entscheidung ist Artefakt.

Ein Gespraech, in dem eine Architekturfrage entschieden wird, erzeugt also **zwei** Dinge: einen Datensatz in der Datenhaltung des Providers und einen ADR in `docs/project/decisions/`. Nicht eins von beiden, und nicht dasselbe zweimal.

Zwei Faustregeln dazu:

- **Ein Repo, ein `docs/`.** Buendelt ein Repo mehrere Projekte in Unterordnern, gibt es trotzdem genau **ein** `docs/` — auf Repo-Ebene, nicht je Projekt-Unterordner. Projektbezug wird ueber `projects:` im Frontmatter hergestellt, nicht ueber den Pfad.
- **Keine Dubletten ueber Ebenen.** Wandert etwas hoch, wird es unten geloescht oder verlinkt.

## 2. Ordnersatz — ein Fundus, eine Pipeline

Auf jeder Ebene derselbe Satz, aber nicht mehr vier gleichrangige Ordner, sondern zwei Sorten:

```
docs/
├── README.md          Index dieser Ebene
│
├── project/            FUNDUS — von jeder Station verlinkbar und beschreibbar
│   ├── worklog/          {YYYY-MM-DD}.md, ein File je Tag
│   ├── decisions/        ADRs, inkl. status: rejected
│   ├── research/         selbst Erhobenes
│   └── sources/          fremd Geliefertes
│
├── records/            FUNDUS — Datensaetze, nur wo freigeschaltet (Abschnitt 4a)
│   ├── persons/{id}.md
│   └── meetings/{YYYY-MM-DD}-{slug}.md
│
├── artifacts/          FUNDUS — was veroeffentlicht wurde (Abschnitt 4b)
│   └── {YYYY-MM-DD}-{slug}/   note.md + page.html
│
├── wayfinding/{YYYY-MM-DD}-{slug}/   PIPELINE 1 — Weg ist unklar: map.md + tickets/
├── changes/{YYYY-MM-DD}-{slug}/      PIPELINE 2 — laufendes Vorhaben
├── archive/{YYYY-MM}/                PIPELINE 3 — abgeschlossene Changes
└── specs/{capability}/spec.md        PIPELINE 4 — Ist-Zustand, was das System HEUTE tut
```

**Die Pipeline laeuft in eine Richtung**: `wayfinding/` → `changes/` → `archive/` → `specs/`. Ein Change wird erst aufgemacht, wenn der Weg feststeht, die Ist-Spec aendert sich ausschliesslich beim Archivieren. Trifft ein Change unterwegs auf Nebel, eroeffnet er eine **neue** Wegfindung, statt die Frage im Proposal zu parken.

**`project/`, `records/` und `artifacts/` sind keine Stationen, sondern Fundus.** ADRs, Recherchen, Quellen, Arbeitslog-Eintraege und veroeffentlichte Seiten entstehen in jeder Phase — vor einer Wegfindung genauso wie waehrend eines Changes — und werden von ueberall verlinkt, nicht davor oder dahinter einsortiert.

**Wegfindung traegt eine Karte je Vorhaben, und die Karte ist Index, kein Speicher.** Eine beantwortete Frage verlaesst sie und wird ein ADR bzw. ein Recherche-Bericht im Fundus; die Karte behaelt nur eine Zeile mit Verweis. Vorlagen dazu in Abschnitt 6.

Der Satz wird beim Anlegen einer Ebene **vollstaendig** erzeugt; die `.gitkeep` eines Ordners verschwindet mit seiner ersten echten Note. Ein **weiterer** Ordner wird nicht erfunden, sondern eingeordnet: Station der Einbahnstrasse, oder Fundus? Passt es in keins von beidem, ist es fast immer eine Entscheidung oder ein Arbeitslog-Eintrag — oder ein Datensatz und gehoert nach Frage 1.

## 3. Struktur fest englisch, Inhalt je Ebene

Die Struktur dieses Layers ist nicht schaltbar: Ordnernamen, Dateinamen, Frontmatter-Schluessel und -Werte, Struktur-Marker und jede Ueberschrift, die eine Vorlage vorgibt, sind englisch — auf jeder Ebene, ohne Ausnahme. Ein Merge, ein Grep, jeder kuenftige Parser liest genau diese Namen; wuerden sie von einer Einstellung abhaengen, muesste jedes Werkzeug beide Varianten kennen. Der Inhalt dagegen folgt der Ebene, auf der die Note liegt — wie das eingestellt wird, steht in Abschnitt 4.

Die Trennlinie laeuft dabei nicht zwischen Ueberschrift und Fliesstext, sondern zwischen vorgegeben und frei gewaehlt: **eine Ueberschrift, die eine Vorlage vorgibt, ist Struktur; eine frei gewaehlte beschreibt ihren einen Fall und bleibt in der Inhaltssprache.** `## Context` in einem ADR (Vorlage in Abschnitt 6) steht in jedem ADR und wird gesucht — sie ist Struktur. Eine Ueberschrift wie `## Befund: OpenSpec-Grammatik verifiziert`, frei gewaehlt innerhalb eines Recherche-Berichts, beschreibt dagegen nur diesen einen Fall — sie ist Inhalt und bleibt in der Sprache der Ebene.

Zwei Ausnahmen von der Strukturregel, weil sie **im** Satz stehen und nicht um ihn herum: die Szenario-Schluesselwoerter (`WENN`/`DANN`/`UND`) in Specs und die Modalverben (`muss`/`wird`/`kann`) folgen der Inhaltssprache. „Der Import must in unter 60 Sekunden abschliessen" waere ein kaputter Satz.

## 4. Inhaltssprache — `lang:` und seine Vererbung

Welche Sprache eine Note traegt, steht nicht in ihr selbst, sondern als `lang:` im Frontmatter der `docs/README.md` der Ebene, auf der sie liegt. Die Einstellung vererbt nach unten — WS-Root → Sub-Bereich → Repo —, der Default ist `en`. Eine Repo-Ebene ohne eigene `docs/README.md` traegt also die Sprache ihres Sub-Bereichs, dieser die des WS-Roots, sofern niemand sie unterwegs umstellt.

Geltend ist die Sprache der **naechstgelegenen** `docs/README.md`, von der eigenen Ebene aus nach oben gesucht — nicht pauschal der Wert des WS-Roots. Eine Note in `{sub-bereich}/{repo}/docs/` folgt `{sub-bereich}/{repo}/docs/README.md`, wenn die existiert und `lang:` traegt, sonst der von `{sub-bereich}/docs/README.md`, sonst der des WS-Roots.

`lang:` steht bewusst in der `docs/README.md` und nicht in `repos.json`: der Ebenen-Index ist ohnehin Pflicht, es entsteht also kein neuer Ort. Ein uebergebenes Repo traegt seine Einstellung damit selbst mit, statt sie in einem Meta-Repo zurueckzulassen, dem es nicht mehr angehoert. Und WS-Root- und Sub-Bereich-Ebenen sind gar keine Repos — in `repos.json` haetten sie keinen Eintrag.

## 4a. Datensaetze — `records/`, und nur wo freigeschaltet

Ein Datensatz ist eine Person, ein Termin, eine Firma — etwas, das **existiert**, im Gegensatz zu einer Entscheidung, die **begruendet**. Bis 2026-08-30 galt: Datensaetze gehoeren nicht in `docs/`, sondern in die Datenhaltung des Providers. Diese Regel hat nicht getragen. Sie wurde in `traffino` am 2026-08-12 beschlossen und verwies auf ein CRM; zweieinhalb Wochen spaeter lagen dort **drei** Dateien. Was nicht neben der Arbeit liegt, wird nicht gepflegt.

Seither gibt es `records/` — im Layer, aber als **Fundus**, nicht als Station der Pipeline. Ein Datensatz entsteht in jeder Phase und wird von ueberall verlinkt, genau wie `project/`.

```
docs/records/
├── persons/{id}.md
└── meetings/{YYYY-MM-DD}-{slug}.md
```

**Der Zweig ist je Ebene freigeschaltet**, nicht ueberall an. Der Schalter steht im Frontmatter der `docs/README.md`, neben `lang:`, und vererbt genauso nach unten:

```yaml
---
lang: de
records: true
---
```

Ohne den Schluessel bleibt der Zweig aus, und die Pruefung ueberspringt ihn still. Das ist Absicht: nicht jeder Provider will seine Personen im Repo, und wer einen Tracker hat, soll ihn behalten duerfen. Wo `records:` fehlt, gilt die alte Regel weiter — Datensaetze gehoeren dann nicht in `docs/`.

**Die Adresse eines Datensatzes wird einmal vergeben und danach eingefroren** — aus demselben Grund wie bei der Anforderungs-Kennung: ein abgeleiteter Name wandert mit dem Titel, ein vergebener nicht. Bei einer Person ist die Adresse der Dateiname, bei einem Termin die Themenblock-Id.

### records/persons/{vorname}-{nachname}.md

```markdown
---
type: person
title: Max Mustermann
updated: 2026-08-30
company: nordwestchemie   # optional
---

Was fuer die Arbeit mit dieser Person zaehlt — Rolle, Zustaendigkeit, Erreichbarkeit.
```

Der **Dateiname ist die Adresse**: `max-mustermann.md` wird als `max-mustermann` referenziert. Kein eigenes `id:`-Feld — ein zweiter Schluessel neben dem Dateinamen waere eine Dublette, die auseinanderlaufen kann.

### records/meetings/{YYYY-MM-DD}-{slug}.md

```markdown
---
type: meeting
title: Kickoff Artikelimport
updated: 2026-08-11
date: 2026-08-11
company: nordwestchemie    # bei rein internen Terminen der eigene Name
internal: false            # true = nur eigene Teilnehmer
channel: meeting           # meeting | call | mail
participants: [max-mustermann, aleksandar-damjanovic]
projects: [article-import]
status: captured | processed
---

### NWC-2026-08-11-1 — Artikelstammdaten-Import

Was besprochen wurde. Ein Block je Thema, damit eine Entscheidung genau darauf zeigen kann.
```

**Themenbloecke tragen `{KUERZEL}-{YYYY-MM-DD}-{n}`**, das Kuerzel in Grossbuchstaben (`NWC` fuer Nordwestchemie). Sie werden **nie** neu vergeben oder umnummeriert, auch wenn ein Block spaeter gegenstandslos wird — sie sind Adressen, keine Gliederung. Eine Entscheidung nennt sie in `origin:`, und damit zeigt der Weg vorwaerts vom Termin in die Entscheidung und rueckwaerts von der Entscheidung ins Protokoll, ohne dass ein Satz zweimal existiert.

**`status: processed`** setzt ein Termin erst, wenn jeder Block entweder in einem Change gelandet oder als Entscheidung mit `status: rejected` abgelegt ist.

**Geprueft wird beides, verschieden hart** — dieselbe Asymmetrie wie bei Anforderung und Test, und aus demselben Grund: waeren beide Richtungen hart, stuende der Lauf am ersten Tag rot.

| Richtung | Haerte |
|---|---|
| `origin:` loest auf einen Block auf · `participants:` loest auf eine Person auf | **bricht den Lauf** |
| ein Block hat Folgen — ein Change oder eine Entscheidung mit `status: rejected` | wird gezaehlt, ohne Schwelle |

Die Mechanik steht im Skill `traceability`, hier steht nur, wie die Notes aussehen.

**Was auch mit `records:` nicht hineingehoert**: Zeiten, Rechnungen, Angebote und alles andere Kaufmaennische — das ist Buchhaltung und gehoert in den Tracker des Providers. Und Personenbezogenes ohne Arbeitsbezug, siehe Abschnitt 7.

## 4b. Artefakte — was veroeffentlicht wurde, liegt auch hier

Eine veroeffentlichte Seite ist ein Arbeitsergebnis mit Publikum: ein Bericht, ein Architekturbild,
eine Uebersicht, die jemand ueber einen Link bekommt. Sie liegt auf dem Artefakt-Server des
Providers — und **zusaetzlich** hier, als Fundus neben `project/` und `records/`.

Der Grund ist der Server selbst: er fuehrt keine Versionshistorie und kein Backup. Ein Update
ersetzt den Inhalt ersatzlos, eine geloeschte Seite ist weg, und der Titel steht mit dem Anlegen
fest und laesst sich danach nicht mehr aendern. Ohne Kopie im Layer gibt es die vorige Fassung
nirgends mehr. Was hier liegt, ist deshalb nicht die Kopie einer Kopie, sondern die einzige Fassung
mit Geschichte.

```
docs/artifacts/{YYYY-MM-DD}-{slug}/
├── note.md      Adresse, Sichtbarkeit, Anlass
└── page.html    das Veroeffentlichte, unveraendert
```

### artifacts/{YYYY-MM-DD}-{slug}/note.md

```markdown
---
type: artifact
title: Sub-Agenten begrenzen
updated: 2026-09-03
artifact_id: V1StGXR8_Z5jdHi6B-myT
url: https://artifact.traffino.com/private/artifact/V1StGXR8_Z5jdHi6B-myT
visibility: private | public
source:              # relativer Pfad auf die Note, aus der die Seite entstand; leer, wenn keine
---

Wofuer die Seite gebaut wurde und wer sie bekommen hat. Zwei bis drei Saetze — nicht der Inhalt der
Seite, der steht nebenan.
```

**`artifact_id` ist die Adresse und wird gebraucht, nicht dekoriert.** Nachbessern heisst denselben
Eintrag ersetzen — dasselbe Werkzeug mit derselben id —, nicht ein zweites Mal veroeffentlichen:
sonst liegen zwei Fassungen unter zwei Links, und der zuerst verschickte zeigt auf die alte.
Wechselt die Sichtbarkeit, wechselt die URL ihren Prefix; `visibility:` und `url:` werden dann
**gemeinsam** nachgezogen, sonst zeigt die Note auf einen toten Link.

**Nicht jede erzeugte HTML-Datei gehoert hierher.** Die Frage ist nie „ist es HTML?", sondern
„entsteht es auf Knopfdruck neu?":

| Fall | Ablage |
|---|---|
| Von Hand gesetzt, nicht wiederherstellbar — ein `diagram-design`-Bild, eine direkt geschriebene Seite | `artifacts/` |
| Aus einer Note gerendert, jederzeit neu erzeugbar | nicht ablegen, neu erzeugen |
| Werkzeug-Ausgabe (`graphify-out/` o.ae.) | nie, siehe Abschnitt 7 |

Haengt in einer Session gar kein Artefakt-Werkzeug, entsteht auch kein Eintrag: dann wird nicht
veroeffentlicht, sondern im Terminal berichtet oder als Datei abgelegt.

## 5. Gemeinsames Frontmatter

Jede Note traegt mindestens:

```yaml
---
type: index | decision | spec | change | worklog | map | ticket | person | meeting | research | source | artifact | archive
title: Kurztitel
updated: 2026-08-12          # letzte inhaltliche Aenderung
---
```

Dateinamen durchgaengig `kebab-case.md`, datierte Notes mit `{YYYY-MM-DD}-`-Praefix.

**`index` traegt genau eine Datei je Ebene: deren `docs/README.md`.** Sie ist keine Karte — eine
`map.md` fuehrt offene Fragen eines Vorhabens, der Index beschreibt, was auf dieser Ebene liegt.
Der Typ steht hier, weil er beim ersten Umzug ausserhalb von traffino gefehlt hat und jede Ebene
sonst ihren eigenen Wert erfindet: gemessen am 2026-08-31 trug die User-Ebene `type: map`, ein
frisch umgezogenes Repo `type: index`. Die `README.md` traegt ausserdem `lang:` und, wo die Ebene
Datensaetze fuehrt, `records: true` — beides gibt es nur dort.

**`research` und `source` fehlten hier aus demselben Grund wie zuvor `index`**: `project/research/`
traegt `type: research`, `project/sources/` traegt `type: source` — an der User-Ebene laengst in
Gebrauch, aber nirgends aufgeschrieben, bis eine frisch umgezogene Ebene am 2026-08-31 `type:
research` waehlte, ohne dass es hier stand.

**`artifact` traegt genau die `note.md` neben einer veroeffentlichten Seite** — Schema und
Begruendung in Abschnitt 4b. Das `page.html` daneben traegt kein Frontmatter; HTML kann keins
tragen, und ein zweiter Ort fuer dieselben Angaben waere eine Dublette, die auseinanderlaeuft.

**`type: archive` fehlte aus demselben Grund und war laengst in Gebrauch, bevor es hier stand**:
eine Note in `archive/`, die **nicht** plan- oder change-foermig ist — eine abgeschlossene
Konzept-Note, deren Gegenstand es nicht mehr gibt (ein weggefallener Dienst, eine verworfene
Architekturidee) — traegt `type: archive` und sonst nur `title:`/`updated:`, kein `status:`. Eine
plan- bzw. change-foermige Note im Archiv (`type: change`, `type: map`, ...) behaelt dagegen ihren
urspruenglichen Typ samt `status:` — sie wird beim Archivieren **nicht** auf `archive` umgestellt.
Ein `status: active`, das dabei stehen bleibt, ist ein Fehler und gehoert auf den zum Ordner
passenden Endzustand (`done`, `superseded`, ...) korrigiert, nicht auf `archive` umgetauft.

## 6. Templates je Typ

### project/decisions/{YYYY-MM-DD}-{slug}.md

```markdown
---
type: decision
title: Retry-Strategie fuer den externen API-Client
updated: 2026-08-12
status: draft | accepted | superseded | rejected | revoked
superseded_by: 2026-09-02-....md   # nur bei status: superseded
origin: []          # ID des Ausloesers, falls vorhanden (z.B. Meeting-Themenblock)
---

## Context

Was war die Lage, welche Kraefte standen gegeneinander.

## Decision

Ein Satz, aktiv, im Praesens.

## Rationale

Warum diese und nicht die Alternativen. Alternativen benennen.

## Consequences

Was wird dadurch leichter, was schwerer.
```

`origin:` nennt IDs des Ausloesers, sofern es einen gibt — etwa einen Meeting-Themenblock aus der Datenhaltung des Providers. Die Kette laeuft ueber **IDs, nicht ueber Pfade** — deshalb traegt sie auch ueber Repo-Grenzen.

**`status: rejected` ist der wichtigste Zustand.** Er beantwortet die Frage, die kein `git log` beantwortet: *„das hatten wir schon mal, und zwar aus diesem Grund verworfen."* Die Begruendung muss **dauerhaft** sein — „gerade keine Zeit" ist eine Verschiebung, keine Ablehnung, und gehoert nicht hierher.

Vor jedem neuen Vorhaben: `decisions/` nach `status: rejected` durchsehen.

**`status: revoked` gilt, wenn eine Entscheidung galt und nicht mehr gilt, ohne dass es einen Nachfolger gibt.** Anders als `superseded` (das einen `superseded_by:`-Verweis auf die abloesende Entscheidung verlangt) und anders als `rejected` (das hiesse, sie waere nie in Kraft getreten) — `revoked` ist der Zustand dazwischen: sie galt, wirkt aber nicht mehr, ohne dass etwas an ihre Stelle getreten ist. (`status: active` ist dagegen kein eigener Wert, sondern ein aelteres Synonym fuer `accepted` und wird bei der Uebernahme in dieses Schema dorthin normalisiert.)

**`status: draft` haelt eine Entscheidung fest, deren Richtung steht, deren Tragfaehigkeit aber noch nicht bewiesen ist** — etwa weil eine Datenschutzberatung sie noch abnehmen muss. Ein `draft` ist kein Dauerzustand: das Dokument muss benennen, auf welches Ereignis es wartet und wie es damit zu `accepted` oder `rejected` wechselt. Ein ADR, das seit Monaten auf `draft` steht, ohne dass jemand dieses Ereignis nennen kann, ist keine dokumentierte Entscheidung, sondern eine unerledigte.

### project/worklog/{YYYY-MM-DD}.md

**Eine Datei je Tag.** Groesser darf sie nicht werden. Ein Tag ohne Eintrag hat keine Datei. Der Grund ist gemessen: als der Log noch eine Datei je Ebene war, standen nach zwei Arbeitstagen 66 Zeilen darin — hochgerechnet eine vierstellige Datei im Jahr.

```markdown
---
type: worklog
title: Arbeitslog 2026-08-12
updated: 2026-08-12
---

- Kickoff-Gespraech gefuehrt, Protokoll in der Datenhaltung des Providers: `2026-08-12-1`
- Change `2026-08-12-artikelimport` angelegt → `../../changes/2026-08-12-artikelimport/`
- Eigener PDF-Renderer verworfen → `../decisions/2026-08-12-kein-eigener-pdf-renderer.md`
```

**Grob und verweisend.** Ein Eintrag nennt, *was* passiert ist, und zeigt auf die Stelle, an der es ausformuliert steht — ADR, Change, Spec. Ein bis zwei Zeilen je Punkt.

**Die Begruendung gehoert nicht hierher.** Wer mehr schreiben will, schreibt einen ADR und verlinkt ihn. Steht das Warum an zwei Stellen, altert die Fassung im Log zuerst — und niemand merkt, welche gilt.

Kein Ersatz fuer `git log`: hier steht, was **nicht** im Diff sichtbar ist — warum abgebrochen, was in einem Gespraech gesagt wurde, welche Sackgasse ausprobiert wurde. Aber als Notiz mit Verweis, nicht als Aufsatz.

### wayfinding/{YYYY-MM-DD}-{slug}/map.md

Ein Verzeichnis je Vorhaben, dessen Weg noch nicht feststeht. **Die Karte ist Index, kein Speicher** — eine beantwortete Frage verlaesst sie und wird ein ADR in `project/decisions/` bzw. ein Bericht in `project/research/`; die Karte behaelt nur eine Zeile mit Verweis. Sonst gaebe es zwei Wahrheiten.

```markdown
---
type: map
title: Kurztitel
updated: 2026-08-14
status: draft | active | done
goal: eine Zeile — worauf diese Wegfindung zulaeuft
origin: []          # ID des Ausloesers, falls vorhanden (z.B. Meeting-Themenblock)
projects: []          # optional
---

## Goal

## Open Questions

| No | Question | Kind | Blocked by | Claim |
|---|---|---|---|---|

## Fog

In Scope, aber noch nicht scharf genug zum Fragen.

## Out of Scope

Jenseits des Ziels, kommt nicht mehr zurueck.

## Decided

Eine Zeile je beantworteter Frage, mit Verweis auf den ADR bzw. Recherche-Bericht.
```

Bei `status: done` kommt `## The Path` dazu — die Synthese, aus der der Change abgeleitet wird, oder die begruendet, warum keiner folgt.

### wayfinding/{YYYY-MM-DD}-{slug}/tickets/{nr}-{slug}.md

Eine einzelne offene Frage aus der Karte, ausgelagert sobald sie eigene Klaerung braucht (`conversation` Gespraech · `research` Recherche · `draft` Entwurf · `task` Aufgabe).

```markdown
---
type: ticket
title: die Frage als Satz
updated: 2026-08-14
status: open | answered | rejected
kind: conversation | research | draft | task
blocked_by: []      # Ticket-Nummern
claim:                 # wer es gerade bearbeitet, sonst leer
result:              # relativer Pfad auf ADR/Recherche, nur bei status: answered
---

## Question

## Answer
```

`## Answer` kommt erst nach Aufloesung dazu — eine Zusammenfassung mit Verweis, der volle Inhalt lebt im ADR bzw. Recherche-Bericht, nie hier verdoppelt.

## 7. Was hier NICHT hingehoert

- **Datensaetze auf einer Ebene ohne `records: true`** — Personen, Firmen, Termine. Wo der Zweig nicht freigeschaltet ist, gehoeren sie in die Datenhaltung des Providers; eine Ansprechpartner-Notiz mitten in `project/` ist auch dort der haeufigste Fehlgriff. Wo er freigeschaltet ist, liegen sie in `records/` und nirgends sonst — siehe Abschnitt 4a.
- **Kaufmaennisches** — Zeiten, Rechnungen, Angebote, Projekte als Auftrag. Das ist Buchhaltung und gehoert in den Tracker des Providers, auch mit `records: true`.
- **Secrets, Zugangsdaten, `.env`-Inhalte** — nie, auf keiner Ebene.
- **Daten eines anderen Kunden/Tenants** in einem Repo, das mehrere buendelt. Die Trennlinie ist hart.
- **Personenbezogenes ohne Arbeitsbezug** (Privatadressen, Geburtstage, Gesundheit) — auch nicht in der Datenhaltung des Providers.
- **Werkzeug-Ausgaben** (`graphify-out/` o.ae.) — derived state wird nicht dokumentiert, sondern
  regeneriert. Das trifft **nicht** die veroeffentlichten Seiten aus Abschnitt 4b: die sind von Hand
  gesetzt und nicht wiederherstellbar, weil der Artefakt-Server keine Versionshistorie fuehrt.

## 8. Normatives wird Skill, nicht Dokument

Was befolgt und nicht gelesen wird — „suche in dieser Reihenfolge", „so wird committet" — gehoert nicht in eine Note, sondern in einen Skill, weil es dort als Anweisung laedt statt nur als Text herumzuliegen. `project/research/` bleibt fuer das Beschreibende: Lessons Learned, Messungen, was jemand herausgefunden hat, ohne ein Verfahren vorzuschreiben.

Beispiel fuer beides aus demselben Vorhaben: ein Playbook, das festlegt, in welcher Reihenfolge nach Code gesucht wird, wurde zum Skill `code-lookup-routing` — es sagt, was zu tun ist. Sein Nachbar zur Shell-Robustheit von Hooks blieb Recherche in `project/research/` — er beschreibt, was jemand ueber Shell-Robustheit herausgefunden hat.

## 9. Diagramme

Zwei Werkzeuge mit klarer Arbeitsteilung:

- **mermaid im Markdown** fuer alles, was mit dem Code mitwandert — Datenmodell, Ablaeufe, Statusautomaten. Lebt als Codeblock **in** der `.md`, ist diffbar und wird beim Aendern neu erzeugt.
- **Skill `diagram-design`** fuer alles, was jemandem **gezeigt** wird — Praesentationen, Angebote, Architekturbilder. Erzeugt eigenstaendiges HTML mit inline-SVG, das von Hand gesetzt ist und sich nicht sinnvoll diffen laesst.

Faustregel: aendert sich das Diagramm mit dem Code, ist es mermaid. Wird es einmal gebaut und dann gezeigt, ist es `diagram-design`.

Ein `diagram-design`-Bild, das veroeffentlicht wird, landet danach in `artifacts/` (Abschnitt 4b) — es ist von Hand gesetzt und entsteht nicht auf Knopfdruck neu.

## 10. Pflege

Dokumentiert wird **waehrend** der Arbeit, nicht am Ende:

1. Neue Erkenntnis → sofort in die passende Note. Nicht in der Commit-Message verstecken.
2. Code-Aenderung, die eine Note falsch macht (Rename, entfernter Pfad, geaendertes Verhalten) → Note im **selben** Arbeitsschritt nachziehen. Eine stale Note ist schaedlicher als eine fehlende.
3. Verweise als relativer Pfad in Backticks, nicht als Wiki-Link — dieser Layer ist kein Obsidian-Vault. Verweise in die Datenhaltung des Providers laufen ueber IDs, nicht ueber Pfade.
