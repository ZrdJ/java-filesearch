# Dokumentations-Pflege (Lifecycle)

Die `docs/` unter Astro Starlight ist **einzige Wahrheit** fuer das Projekt. Nicht einmalig aufgesetzt, sondern mit jedem Feature mitgepflegt. Diese Rule definiert, welches Dokument **wann** aktualisiert wird und wo **Claude-Plans** landen.

---

## Kernprinzip: SOLL vs IST

| Bereich | Bedeutung | Aktualisierung |
|---------|-----------|----------------|
| `vision/` | Warum bauen wir das? | Selten — bei strategischen Aenderungen |
| `requirements/` | Was muss es koennen? | Wenn neue Anforderungen dazukommen |
| `architektur/` | **SOLL** — wie soll es aufgebaut sein? | Vor Implementierung, bei Entscheidungen |
| `roadmap/` | Welche Reihenfolge? | Wenn Stufen/Features verschoben werden |
| `entwicklung/` | Arbeit an Features | Laufend waehrend Implementierung |
| `systemdokumentation/` | **IST** — was ist tatsaechlich gebaut? | Nach jedem Feature-Abschluss |

**Regel:** Architektur beschreibt das Ziel. Systemdokumentation beschreibt den Stand. Die beiden duerfen auseinanderlaufen — dann wird entweder die Architektur nachgezogen (bewusste Aenderung) oder das System angepasst (Rueckfuehrung).

---

## Feature-Lifecycle

Jedes nicht-triviale Feature durchlaeuft diese Stationen. Gilt fuer Claude-gestuetzte Arbeit genauso wie fuer manuelle.

### 1. Vor Implementierung — Spec + Plan

**Design Spec:** `entwicklung/specs/{YYYY-MM-DD}-{feature}-design.md`
- Datenmodell, API-Contracts, Flows, Architektur-Entscheidungen
- Wird vor dem Code geschrieben und abgestimmt
- Bleibt als historisches Artefakt liegen — spaeter nicht aktualisiert

**Implementation Plan:** `entwicklung/plans/{YYYY-MM-DD}-{feature}.md`
- Schritt-fuer-Schritt Aufgabenliste (Backend, Frontend, DB, Migrationen)
- Basis fuer Claude-Ausfuehrung (siehe `superpowers:writing-plans`)
- Haken werden waehrend der Umsetzung gesetzt

**Index-Dateien aktualisieren:** `specs/index.md` und `plans/index.md` bekommen einen neuen Tabelleneintrag.

### 2. Waehrend Implementierung — TODO-Tracker

**Datei:** `entwicklung/implementierung/{stufe-X|milestone-Y}-uebersicht.md`

Eine Datei pro Stufe/Milestone mit **zwei Tabellen**:

```markdown
## Entscheidungen

| Datum | Entscheidung | Begruendung |
|-------|-------------|-------------|
| 2026-04-09 | 2FA per Email statt TOTP | Einfacher fuer Endkunden |

## Fortschritt

| Feature | Status | Datum |
|---------|--------|-------|
| Auth (Login, 2FA, Session) | Fertig | 2026-04-09 |
| Placeholder-System         | Offen  | —         |
```

**Status-Werte:** `Offen` | `In Arbeit` | `Fertig` | `Verworfen` | `Blockiert`

**Warum genau dieses Format:**
- Eine einzige Datei pro Stufe statt verstreute Notizen → Claude findet sich schnell zurecht
- Entscheidungs-Log chronologisch → Rueckverfolgbarkeit ohne Git-Archaeologie
- Fortschritts-Tabelle ersetzt Jira/Trello fuer Ein-Personen- und Kleinteam-Projekte
- Markdown-Tabelle bleibt in Starlight lesbar und ist schnell editierbar

### 3. Nach Implementierung — Systemdokumentation

**Datei:** `systemdokumentation/{subsystem}.md`

Wird neu angelegt oder aktualisiert, sobald ein Feature verkaufbar/ausrollbar ist:
- Flow-Beschreibung (was passiert wann)
- Datenmodell (DB-Schema-Auszug)
- API-Endpoints / UseCase-Signaturen
- Code-Struktur-Hinweise (Pfade, Packages)
- Bekannte Einschraenkungen

**Index aktualisieren:** `systemdokumentation/index.md` bekommt einen Eintrag.

**Die alten Specs/Plans bleiben liegen** — sie sind historische Artefakte. Die Systemdoku ist der aktuelle Stand.

---

## Claude-Plans gehoeren in die Docs

Alles was Claude als Plan erzeugt (z.B. ueber `superpowers:writing-plans`) wird **nicht** ephemer im Chat oder in lokalen Notizen gehalten, sondern direkt unter `entwicklung/plans/` abgelegt.

**Vorteile:**
- Ueber Sessions hinweg nachlesbar
- Teil des Repos, versioniert, im Starlight-Build sichtbar
- Neue Claude-Sessions finden den aktuellen Stand ueber den TODO-Tracker + Plan-Index
- Plans werden nicht dupliziert — ein Plan pro Feature

**Ausnahme:** Triviale Einzelaenderungen (< 30 Min, keine Architektur-Wirkung) brauchen keinen Plan.

---

## Session-Start-Protokoll

Fuer Claude bei Projektarbeit **immer zuerst**:

1. **CLAUDE.md lesen** (Projekt-Status, aktuelle Phase, TODO-Tracker-Pfad)
2. **TODO-Tracker oeffnen** (`entwicklung/implementierung/{aktuelle-stufe}-uebersicht.md`)
3. **Falls Feature-Arbeit:** passenden Plan unter `entwicklung/plans/` lesen
4. **Falls System-Frage:** erst `systemdokumentation/` lesen (IST), dann `architektur/` (SOLL)

Damit ist Claude nach 3 Dateien voll im Bild.

---

## Sidebar-Hinweise (Starlight)

Die Reihenfolge in der Sidebar folgt dem Lifecycle:

```
Vision → Requirements → Architektur (SOLL) → Roadmap → Systemdokumentation (IST) → Entwicklung
```

---

## Schneller Kontext-Ueberblick: Index-Tabellen-Pattern

Damit Claude beim Session-Start oder Seitenaufruf in wenigen Dateien den aktuellen Stand erfasst, **muss jede Seite** dem Page-Level-Index-Pattern aus dem `markdown` Skill folgen.

**Kern-Pattern** (siehe `markdown` Skill → `pattern-page-level-index.md`):
- Jedes Verzeichnis hat ein `index.md` mit `## In diesem Abschnitt` + Tabelle `| Seite | Beschreibung |`
- Relative Links (`vision/` statt `/docs/vision/`), Verzeichnisse mit Trailing-Slash
- Keyword-reiche Beschreibungen als Routing-Signal — Claude entscheidet ohne Oeffnen, ob eine Datei relevant ist
- Aussagekraeftige H2-Ueberschriften als implizites TOC, ab ~80 Zeilen explizites `## Inhalt`

**Top-Level Root-Index** (`src/content/docs/index.mdx`): listet alle Bereiche mit Ein-Satz-Beschreibung:

```markdown
## In diesem Abschnitt

| Seite | Beschreibung |
|-------|--------------|
| [Vision](vision/) | Elevator Pitch, Ziele, Positionierung, Stakeholder |
| [Requirements](requirements/) | Feature-Uebersicht, NFRs, Constraints, User Stories |
| [Architektur](architektur/) | System-Diagramm, Tech-Stack, uebergreifende Patterns |
| [Roadmap](roadmap/) | Stufenplan — vom Minimum zum vollen Produkt |
| [Systemdokumentation](systemdokumentation/) | Ist-Zustand — implementierte Features und technische Details |
| [Entwicklung](entwicklung/) | Arbeitsartefakte — Entscheidungen, Specs, Plans |
```

**Specs/Plans-Index** (chronologisch, mit Datum im Dateinamen):

```markdown
## In diesem Abschnitt

| Seite | Beschreibung |
|-------|--------------|
| [Auth Feature](2026-04-09-auth-feature.md) | Login, 2FA, Sessions, Middleware |
| [Account-Verwaltung](2026-04-13-account-verwaltung.md) | Profil, Passwort, Sessions, Team-CRUD |
```

**Systemdokumentations-Index** (nach Subsystem, nicht chronologisch):

```markdown
## In diesem Abschnitt

| Seite | Beschreibung |
|-------|--------------|
| [Authentifizierung](authentifizierung.md) | Login-Flow, 2FA per E-Mail, Sessions, Device-Erkennung |
| [Datenbank](datenbank.md) | Schema, Audit-Pattern, Migrationen, ID-Strategie |
```

**Warum das fuer Claude wichtig ist:** Root-Index → Bereichs-Index → Zieldatei. Maximal 3 Reads fuer jede beliebige Information. Bei fehlenden Index-Dateien muesste Claude `ls` + jede Datei einzeln oeffnen.

---

## Checkliste pro Feature

Bevor ein Feature als `Fertig` markiert wird:

- [ ] Design Spec existiert unter `entwicklung/specs/`
- [ ] Implementation Plan existiert unter `entwicklung/plans/`
- [ ] Beide sind in den jeweiligen `index.md` verlinkt
- [ ] Entscheidungen sind im Entscheidungs-Log des TODO-Trackers erfasst
- [ ] `systemdokumentation/{subsystem}.md` ist neu oder aktualisiert
- [ ] `systemdokumentation/index.md` verweist darauf
- [ ] Falls Architektur-Aenderung: `architektur/` aktualisiert
- [ ] Fortschritts-Tabelle im TODO-Tracker auf `Fertig` gesetzt
- [ ] `npm run build` im `docs/` laeuft fehlerfrei

---

## Anti-Patterns

| Anti-Pattern | Warum schlecht | Stattdessen |
|--------------|----------------|-------------|
| Spec/Plan nachtraeglich schreiben | Dient dann nur noch als Alibi | Vor der Implementierung oder gar nicht |
| System-Aenderung ohne Architektur-Update | SOLL und IST laufen unbemerkt auseinander | Erst Architektur, dann Code |
| TODO-Tracker in separater Tool-Liste | Claude findet es nicht | Immer im Repo unter `entwicklung/implementierung/` |
| Alte Specs "aktuell halten" | Dokumentation verliert Aussagekraft | Specs sind Momentaufnahmen. Systemdoku ist aktuell |
| Umlaute in Dateinamen | Bricht auf manchen Systemen | Konsequent `ae/oe/ue/ss` |
