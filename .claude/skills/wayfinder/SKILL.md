---
name: wayfinder
version: 1
license: MIT
upstream: https://github.com/mattpocock/skills
upstream-commit: 8b78b531ab965735c5dc74f6f7a219e1e37326df
description: Ein Vorhaben, dessen Weg noch nicht feststeht, als Karte offener Fragen fuehren und Ticket fuer Ticket aufloesen, bis der Weg klar ist und ein Change abgeleitet werden kann. Legt Karten unter docs/wayfinding/ an, trennt scharfe Fragen vom Nebel, haelt Blockierungen fest und schliesst mit einem Sondierungsergebnis. Triggers auf Wegfindung, Karte, unklarer Weg, "wie gehen wir das an", Vorhaben sondieren, offene Fragen sammeln, Nebel, Out of Scope, "wissen noch nicht was wir bauen".
# GENERIERT aus ~/.claude/skills-ref/wayfinder/ — nicht hier editieren, Aenderungen gehoeren in die Referenz.
source: personal-user-ref
ref-hash: sha256:97ac9b071336d1fdaff5ec1757f109ffd774c1a004219dab42cd380678670811
---

# wayfinder

Fuer Vorhaben, die **zu gross fuer eine Session** sind und deren Weg **noch nicht sichtbar** ist. Nicht fuer „wir wissen was zu tun ist, es ist nur viel" — dafuer ist `spec` mit seinen Slices da.

## Herkunft und Zuschnitt

Uebernommen aus [mattpocock/skills](https://github.com/mattpocock/skills) (MIT, Commit `8b78b53`), **nicht verbatim**. Uebernommen sind das Konzept und seine Begriffe: Karte als Index, Entscheidungs-Tickets, Nebel, Out of Scope, ein Ticket je Session. Ersetzt ist die Mechanik: das Original setzt einen **Issue-Tracker** voraus (Child-Issues, native Blocking-Relationen, Assignee als Anspruch). Hier lebt alles als Markdown unter `docs/wayfinding/`, wo die jeweilige Ebene keinen Tracker fuehrt — ob sie das tut, entscheidet deren CLAUDE.md.

Die Verweise des Originals auf `/grilling`, `/domain-modeling`, `/research` und `/prototype` zeigen auf Skills, die es hier nicht gibt. Womit sie ersetzt sind, steht unter [Werkzeuge](#werkzeuge).

Upstream-Drift wird **nicht** automatisch bemerkt — wer wissen will, ob es Neues gibt, vergleicht von Hand gegen `upstream-commit`.

## Wo das sitzt

Erste Station der Pipeline aus der CLAUDE.md-Hierarchie:

```
wayfinding/  ──▶  changes/  ──▶  archive/  ──▶  specs/
Weg unklar        Vorhaben       erledigt       Ist-Zustand
```

Ein Change setzt voraus, dass Problem, Loesung und Scope feststehen. Solange sie das nicht tun, wird **kein** Change angelegt. Trifft ein laufender Change auf Nebel, eroeffnet er eine **neue** Karte, statt die Frage im Proposal zu parken.

Begruendung des Schnitts: `docs/project/decisions/2026-08-14-wegfindung-als-eigene-station.md`.

## Das eine Prinzip: planen, nicht bauen

Jedes Ticket loest eine **Entscheidung** auf, keinen Bauabschnitt. Die Karte ist fertig, wenn nichts mehr zu entscheiden ist — nicht, wenn etwas gebaut ist.

Der Drang, „das eben schnell zu machen", ist fast immer das Signal, dass der Rand der Karte erreicht ist und der Change beginnt. Ihm nachzugeben ist der haeufigste Weg, eine Wegfindung zu ruinieren: ab dann steht Code da, den keine Entscheidung deckt.

Die einzige Ausnahme ist die Ticket-Art `task` — siehe unten.

## Aufbau

Ein Verzeichnis **je Vorhaben**. Mehrere Wegfindungen duerfen gleichzeitig laufen; eine globale Karte gibt es nicht, weil eine Karte genau ein Ziel hat und mit dessen Erreichen schliesst.

```
docs/wayfinding/{YYYY-MM-DD}-{slug}/
├── map.md
└── tickets/{nr}-{slug}.md
```

Frontmatter und Body-Sektionen beider Dateien stehen im Skill `docs` → „Templates je Typ". Hier steht, **wie** damit gearbeitet wird.

### Die Karte ist Index, kein Speicher

Die wichtigste Regel des Modells. Eine beantwortete Frage **verlaesst** die Karte:

| Ticket-Art | Ergebnis landet in |
|---|---|
| `conversation`, `draft`, `task` | `project/decisions/{datum}-{slug}.md`, `status: accepted` |
| `research` | `project/research/{datum}-{slug}.md` — plus der ADR, den sie ermoeglicht |
| jenseits des Ziels | `project/decisions/…`, `status: rejected` |

In der Karte bleibt **eine Zeile mit Verweis**. Wer die Antwort in die Karte schreibt, hat ab da zwei Wahrheiten und keine Moeglichkeit mehr zu pruefen, welche gilt.

**Wann wird eine Antwort ein ADR?** Test: *interessiert sie jemanden, der die Karte nie gesehen hat?* Ja → ADR, sofort. Nein → die Zeile in der Karte genuegt, und beim Abschluss wird entschieden, ob sie noch einen bekommt. Ein ADR ist hier 40 bis 60 Zeilen; fuer jede Zwischenfrage einen zu schreiben, kostet mehr als es traegt.

### Ticket-Arten

Jedes Ticket ist entweder **mit Mensch** — es loest sich nur im lebenden Austausch — oder **allein**, vom Agenten getrieben. Bei den Mensch-Arten spricht der Agent **nie** fuer die andere Seite. Ein Ticket, dessen Fragen der Agent sich selbst beantwortet hat, ist nicht aufgeloest.

| `kind` | Wer | Wofuer |
|---|---|---|
| `research` | allein | Wissen ausserhalb des Arbeitsverzeichnisses beschaffen — Doku, fremde API, Quellen. Ergebnis ist ein Bericht, auf den eine Entscheidung wartet. |
| `draft` | mit Mensch | Die Diskussion konkret machen: Skizze, Attrappe, Stub, Diagramm — etwas, worauf man reagieren kann. Wenn „wie soll das aussehen / sich verhalten" die eigentliche Frage ist. |
| `conversation` | mit Mensch | Der Normalfall. Es wird geredet, bis die Entscheidung steht. |
| `task` | beides | Handarbeit, die **vor** einer Entscheidung passieren muss: Zugang beschaffen, Konto anlegen, Daten bewegen, damit ihre Form sichtbar wird. Die einzige Art, die **tut** statt entscheidet — und sie rechtfertigt sich allein dadurch, dass sie eine Entscheidung entsperrt, nie durch ihr Ergebnis. Was der Agent allein kann, macht er; sonst uebergibt er eine praezise Checkliste. |

### Blockierung und Front

`blocked_by: [2, 3]` nennt Ticket-Nummern derselben Karte. Ein Ticket ist **frei**, wenn alle blockierenden auf `answered` stehen.

Die **Front** ist die Menge der Tickets, die `open`, frei und ohne `claim` sind — der Rand des Bekannten. Wer ein Ticket zieht, traegt sich **zuerst** in `claim` ein, vor jeder Arbeit, damit parallele Sessions es ueberspringen.

## Nebel und Out of Scope

Zwei Sektionen der Karte, die leicht verwechselt werden. Die Trennlinie ist **nicht** dieselbe.

**`## Fog`** — in Scope, aber noch nicht scharf genug zum Fragen. Was man kommen sieht, aber nicht formulieren kann, weil es an offenen Fragen haengt. Wird ein Ticket aufgeloest, lichtet sich der Nebel dahinter: was jetzt formulierbar ist, wird zu neuen Tickets und **verschwindet aus dieser Sektion** — es lebt ab da nur noch als Ticket.

Der Test lautet: **kann ich die Frage jetzt praezise stellen?** — nicht: kann ich sie beantworten.

- Praezise stellbar → Ticket, auch wenn es blockiert ist und niemand daran arbeiten kann.
- Nicht praezise stellbar → Nebel. Nicht in ticketgrosse Stuecke vorschneiden; ein Nebelfeld wird spaeter zu mehreren Tickets, zu einem, oder zu keinem.

**`## Out of Scope`** — jenseits des Ziels. Kein Nebel, sondern bewusst ausgeschlossen. Hier entscheidet **Scope**, nicht Schaerfe. Nebel sammelt sich nur *auf dem Weg zum Ziel*; das Ziel begrenzt ihn.

Out of Scope kommt **nie** zurueck. Wird das Ziel neu gezogen, ist das eine neue Wegfindung, keine Fortsetzung.

Stellt sich bei einem bestehenden Ticket heraus, dass es jenseits des Ziels liegt: auf `status: rejected` setzen, eine Zeile mit Begruendung nach `## Out of Scope`, Verweis auf das Ticket. Es bleibt **aus `## Decided` heraus** — dort steht der tatsaechlich gegangene Weg, und eine Scope-Grenze ist kein Schritt darauf.

## Zwei Modi

### Karte anlegen

Ausgangspunkt ist eine lose Idee.

1. **Ziel benennen.** Worauf laeuft das zu — ein Proposal, eine Entscheidung, eine Umstellung? Das Ziel steht **zuerst** fest, weil es den Scope fixiert. Es wird nicht mitevaluiert; evaluiert werden die Wege dorthin.
2. **Front kartieren.** In die Breite fragen, nicht in die Tiefe: welche Entscheidungen stehen an, was ist jetzt schon angehbar. **Entsteht dabei kein Nebel**, ist der Weg bereits klar und es braucht keine Karte — sagen und nachfragen, wie weiter.
3. **`map.md` anlegen**, `status: active`: Ziel gefuellt, `## Decided` leer, der Nebel skizziert.
4. **Tickets anlegen**, die sich jetzt praezise stellen lassen. `blocked_by` in einem **zweiten Durchgang** setzen — die Nummern muessen erst existieren. Was sich nicht formulieren laesst, bleibt im Nebel.
5. **Recherche-Tickets sofort starten**, parallel, per Sub-Agent (siehe [Werkzeuge](#werkzeuge)).
6. **Aufhoeren.** Kartieren ist die Arbeit einer Session. Es loest kein Ticket auf.

### Karte abarbeiten

**Nie mehr als ein Ticket je Session** — ausser Recherche-Tickets, die laufen parallel.

1. `map.md` lesen, nicht saemtliche Tickets.
2. Ticket waehlen: das vom User genannte, sonst das erste der Front. **`claim` eintragen, bevor gearbeitet wird.**
3. Aufloesen. Verwandte oder geschlossene Tickets bei Bedarf nachladen, nicht auf Vorrat.
4. Ergebnis wegschreiben: ADR bzw. Recherche-Bericht anlegen, Ticket auf `answered` mit `result:`, **eine Zeile** nach `## Decided`.
5. Nachziehen: neu entstandene Tickets anlegen und verdrahten; gelichteten Nebel in Tickets ueberfuehren und aus `## Fog` entfernen. Zeigt die Antwort, dass ein Ticket jenseits des Ziels liegt → Out of Scope statt aufloesen. Kippt sie andere Tickets, werden die geaendert oder entfernt.

Andere Sessions koennen gleichzeitig an derselben Karte arbeiten. `claim` ist die einzige Absicherung dagegen.

## Abschluss

Die Karte schliesst, wenn kein Ticket mehr offen und der Nebel leer ist.

`status: done`, und `## The Path` kommt dazu: die **Synthese** — welcher Weg gefunden wurde und warum, mit Verweis auf die tragenden Entscheidungen. Keine Wiederholung ihrer Inhalte; das ist dasselbe Verhaeltnis, das `design.md` zu den ADRs hat.

Daraus folgt eins von zwei Dingen:

- **Ein Change.** `docs/changes/{YYYY-MM-DD}-{slug}/` anlegen (Skill `spec`, Phase 1), die Karte im Proposal unter `origin:` nennen.
- **Kein Change.** Auch das ist ein Ergebnis. `## The Path` haelt fest, warum nicht gebaut wird — und ist der Grund, warum die Wegfindung eine eigene Station ist: sonst haette dieses Ergebnis keinen Ort.

Die Karte bleibt danach liegen. Sie wandert **nicht** ins `archive/` — dort liegen Changes, und das Proposal verweist auf sie.

## Werkzeuge

Das Original verweist auf Skills, die es hier nicht gibt. Ersatz:

| Original | Hier |
|---|---|
| `/grilling` | Skill `meeting` fuer Termine mit Dritten; `grill-me` fuer das Durchfragen einer eigenen Idee |
| `/domain-modeling` | Skills `docs` und `spec` — die Begriffsregel „ein Begriff, eine Bedeutung" steht dort bereits |
| `/prototype` | mermaid in der `.md` fuer alles, was sich mit dem Code aendert; `diagram-design` fuer Bilder, die gezeigt werden |
| `/research` | Sub-Agent per `Agent`-Tool, Modell nach der Routing-Tabelle des Users. Der Agent bekommt die Frage und liefert den Bericht — er entscheidet nicht. |
| `/setup-matt-pocock-skills` | entfaellt, der Ort steht fest (`docs/wayfinding/`) |

Auf welcher Ebene die Karte liegt, entscheidet die Ablageregel der CLAUDE.md-Hierarchie — dieselbe Frage wie fuer jede andere Note.

## Antipattern

- **Change aufmachen, um die Fragen im Proposal zu parken.** Das war der Zustand vor diesem Skill. `## Open Questions` im Proposal ist fuer bewusst Offengelassenes — etwa weil die Antwort beim Kunden liegt —, nicht fuer Ungeklaertes. Test: haengt ein Slice daran, wie die Frage ausgeht, gehoert sie in eine Karte.
- **Die Antwort in der Karte lassen.** Erzeugt die zweite Wahrheit. Die Karte verweist, sie speichert nicht.
- **Nebel vorschneiden.** Ticketfoermige Stuecke aus etwas machen, das noch keine Form hat. Sie sind spaeter falsch geschnitten und werden trotzdem abgearbeitet.
- **Mehr als ein Ticket je Session.** Die Antwort auf Ticket 1 aendert oft Ticket 2. Wer beide in einer Session zieht, beantwortet das zweite auf veraltetem Stand.
- **Sich selbst grillen.** Bei `conversation` und `draft` beantwortet der Agent die Fragen des Menschen nicht. Ein Ticket, das so „aufgeloest" wurde, ist offen.
- **Bauen.** Siehe oben. Der Drang dazu ist das Signal fuer den Abschluss, nicht die Erlaubnis dafuer.
