# In einen anderen Workspace heben

Dieser Skill ist zu ~85 % generisch. Was ortsspezifisch ist, steht hier — beim Kopieren nur das anfassen.

## Vorgehen

1. `skills-ref/spec/` in den Ziel-Workspace kopieren (bzw. ins Ziel-Repo, wenn der Skill dort greifen soll — der Skill-Aufstieg endet am Repo-Root).
2. Die sechs Punkte unten durchgehen.
3. `beispiel/` behalten oder ersetzen. Behalten ist meist besser: das Zusammenspiel der Marker ist wichtiger als die Fachlichkeit des Beispiels.

## Was anzupassen ist

### 1. Wo `docs/` liegt

Traffino hat vier Ebenen (`intern/`, `intern/{repo}/`, `kundenprojekte/`, `kundenprojekte/{kunde}/`) mit einer eigenen Ablageregel, die in der jeweiligen `CLAUDE.md` steht. Andere Workspaces haben stattdessen `vault/` oder einen einzigen Ort — welche Regel gilt, fragt der Skill bei der `CLAUDE.md` der Ebene ab, er bringt keine eigene mit.

**Betroffen**: nichts am Skill selbst. `SKILL.md` → „Ordner", `propose.md` → „Dateien anlegen" und `archive.md` → „Verschieben" nennen nur `docs/…`-Pfade relativ zur Ebene, ohne eine bestimmte Ablageregel vorauszusetzen.

Ein Workspace **mit** Vault kann diesen Skill trotzdem nutzen — dann heisst der Wurzelordner `vault/` statt `docs/`, und `specs/`+`changes/` liegen darunter. Nichts anderes aendert sich.

### 2. Meeting-Verkettung (bzw. was an ihre Stelle tritt)

`origin:` verweist auf die nachvollziehbare Quelle eines Vorhabens — der Skill schreibt dafuer kein festes Schema vor, sondern zeigt auf das, was die jeweilige Ebene zur Herkunfts-Verfolgung fuehrt: eine Meeting-Themenblock-ID im Schema `{KUERZEL}-{YYYY-MM-DD}-{n}`, wenn dort ein `meeting`-Skill existiert; sonst eine Issue-ID, eine Ticket-Nummer, ein Protokoll-Dateiname. Gibt es im Ziel gar keine Herkunfts-Verfolgung, bleibt das Feld leer — nicht erfinden.

**Betroffen**: nichts am Skill selbst. `propose.md` → „Frontmatter" und `templates/proposal.md` nennen die Meeting-Themenblock-ID nur als **ein** Beispiel unter mehreren, nicht als Voraussetzung.

Nicht ersatzlos streichen. Ein Vorhaben ohne nachvollziehbaren Ausloeser ist genau das, was das Modell verhindern soll — auch ohne Meeting-Skill bleibt die Pflicht, eine Quelle zu nennen oder das Fehlen bewusst offen zu lassen.

### 3. Negativ-Speicher

Der Abgleich gegen `status: rejected` (in `propose.md`, erster Schritt) setzt `project/decisions/` voraus. In einem Ziel mit dem `docs/`-Wissens-Layer ist das ein fester, englischer Ordnername — nichts anzupassen (Struktur ist workspace-uebergreifend gleich, siehe Punkt 4). Traegt das Ziel stattdessen ein `vault/` mit eigenen Ordnernamen (z. B. `entscheidungen/`, `adr/`), zeigt der Pfad auf dessen Aequivalent. Existiert dort gar keiner: anlegen — der Schritt ist einer der wenigen, die eine Frage beantworten, die sonst **niemand** beantworten kann.

**Betroffen**: `propose.md`, `archive.md` → „Wenn ein Change nicht kommt" — nur bei einem `vault/`-Ziel, sonst unveraendert.

### 4. Sprache

Seit der Entscheidung `2026-08-30-struktur-englisch-inhalt-je-ebene.md` (im `project/decisions/` des Providers, der den Layer eingefuehrt hat) gilt eine **Zwei-Achsen-Regel** statt „Sprache ist eine Eigenschaft des ganzen Layers": die **Struktur** — Ueberschriften wie `## ADDED Requirements` / `### Requirement:` / `#### Scenario:`, Frontmatter-Schluessel und -Werte, Marker, Spaltenkoepfe — ist **immer** englisch und aendert sich beim Kopieren **nicht**. Nur der **Inhalt** folgt der Ebene: die Szenario-Schluesselwoerter `WENN`/`DANN`/`UND` bzw. `WHEN`/`THEN`/`AND`, die Modalverben `muss`/`wird`/`kann` bzw. `must`/`will`/`can`, der Fliesstext in `references/*.md`, die Platzhaltertexte in `templates/` und die Fachlichkeit in `beispiel/`.

`references/anforderungen.md` fuehrt die beiden Woerter-Vorraete seit dem Umbau **zweisprachig** in derselben Tabelle — dort ist beim Kopieren nichts mehr zu uebersetzen, ein Ziel mit `lang: en` folgt einfach der jeweils anderen Spalte. Was bei `lang: en` tatsaechlich noch angepasst werden muss: der Fliesstext in `references/*.md` (samt der Antipattern-Beispiele in `anforderungen.md`, die durchgehend Deutsch bleiben), die Platzhaltertexte in `templates/` und die Fachlichkeit in `beispiel/` — alle drei sind bislang durchgehend deutsch (`lang: de`) gehalten, mit einem Hinweis darauf am Anfang der Sprachwahl-Sektion in `anforderungen.md`.

**Betroffen bei `lang: en`**: der Fliesstext in `anforderungen.md` und den uebrigen `references/*.md`, alle `templates/` (Platzhaltertexte), `beispiel/` (die Fachlichkeit des Artikelimport-Falls). **Nicht mehr betroffen**: die Modalverben- und Szenario-Schluesselwoerter-Tabellen selbst — die stehen bereits in beiden Sprachen nebeneinander.

**Nebeneffekt unveraendert**: die Struktur-Keywords machen das Format bereits kompatibel zur OpenSpec-CLI, unabhaengig von der Inhaltssprache. Wer die CLI will, kann `openspec validate` und `openspec archive` nutzen statt der Handarbeit aus `archive.md` — das galt vorher nur fuer ein englischsprachiges Ziel, gilt jetzt fuer jedes.

### 5. Build-/Test-Gate

`apply.md` nennt keinen festen Befehl mehr, sondern verweist auf den kanonischen Build-/Test-Einstieg der Repo-`CLAUDE.md` (oder einer Ebene darueber) — ausgehandelt und dort nachgetragen, wenn keiner genannt ist.

**Betroffen**: nichts mehr. Frueher stand hier `./dev test` als traffino-Konvention fest verdrahtet; das ist seit der Verallgemeinerung des Skills Sache der jeweiligen Repo-`CLAUDE.md`, nicht mehr des Skills.

### 6. Standards-Achse

`verify.md` ueberspringt die Standards-Achse, wenn Tooling sie erzwingt. Ob das zutrifft, ist repo-spezifisch: ArchUnit, Custom-Lint, Layer-Tests. Der **Erkennungsschritt** bleibt generisch, seine Antwort nicht.

**Betroffen**: `verify.md` → „Zwei Achsen, getrennt halten".

## Was NICHT angefasst wird

Der Kern traegt ueberall, weil er nichts ueber die Umgebung annimmt:

- `specs/` = Ist, `changes/` = Soll, Ist-Spec aendert sich nur beim Archivieren
- Die Marker `ADDED` / `MODIFIED` / `REMOVED` und der Merge-Ablauf
- Anforderung + Szenario als Form, ein Szenario je auffallender Verzweigung
- Die drei Fund-Sorten in `verify.md` (fehlt · zu viel · sieht richtig aus)
- Slice-Tabelle, vertikaler Schnitt, Abgleich gegen `git log`
- Richtungswechsel anhaengen statt ueberschreiben
- Die Frage „aendert sich ein Szenario?" als Change-Kriterium

Wer daran etwas aendert, aendert das Modell — nicht die Umgebung.

## Als Vorlage fuer andere Skills

Der Aufbau ist absichtlich uebertragbar: `SKILL.md` traegt Entscheidungen und Verweise, `references/` das Detail je Phase, `templates/` kopierfertige Dateien, `beispiel/` einen vollstaendigen Durchlauf.

Die Aufteilung folgt daraus, wann etwas gebraucht wird. `SKILL.md` liegt bei jedem Treffer im Kontext und muss deshalb kurz bleiben; `references/` wird erst gelesen, wenn die Phase wirklich dran ist. Alles, was man beim **Entscheiden** braucht, gehoert nach oben — alles, was man beim **Ausfuehren** braucht, nach unten.

Faustregel: passt eine Phase nicht auf zwei Bildschirme, gehoert sie in `references/`.
