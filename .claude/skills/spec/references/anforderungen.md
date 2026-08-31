# Anforderungen und Szenarien schreiben

Gilt fuer `specs/` (Ist) und die Delta-Specs in `changes/` gleichermassen — es ist dieselbe Sprache, nur eine andere Zeitaussage.

## Aufbau

```markdown
### Requirement: {ein Satz, was moeglich ist}
`req~{capability}.{kurzname}~{revision}`

{1-3 Saetze Praezisierung. Was das System tut, aus Sicht dessen, der es benutzt.}

#### Scenario: {konkreter Fall}

- **WENN** {Ausloeser}
- **DANN** {beobachtbares Ergebnis}
- **UND** {weiteres beobachtbares Ergebnis}
```

- **Ueberschrift**: was **moeglich** ist, nicht wie es gebaut ist. „Artikel koennen als CSV importiert werden", nicht „CSV-Parser im Import-Service".
- **Kennung**: eigene Zeile in Backticks, direkt unter der Ueberschrift. Sie wird beim Anlegen von Hand vergeben und danach eingefroren — deshalb darf der Titel spaeter umformuliert werden, ohne dass etwas reisst. Wann die Revision steigt, was bei abgeloesten Anforderungen passiert und wie ein Test darauf verweist, steht im Skill `traceability`; hier wird es **nicht** wiederholt.
- **Fliesstext**: praezisiert, ersetzt aber kein Szenario.
- **Szenarien**: mindestens eins. Eine Anforderung ohne Szenario ist eine Absichtserklaerung und wird beim Verifizieren wertlos.

## Sprachwahl: Modalverben und Szenario-Schluesselwoerter

Beide sind **Inhalt**, keine Struktur — sie stehen im Satz, nicht um ihn herum (Entscheidung `2026-08-30-struktur-englisch-inhalt-je-ebene.md`). Sie folgen deshalb der Inhaltssprache der Ebene (`lang:` in deren `docs/README.md`, Default `en`) und **werden innerhalb eines Dokuments nicht gemischt**: entweder durchgehend `muss`/`wird`/`kann`/`WENN`/`DANN`/`UND`, oder durchgehend `must`/`will`/`can`/`WHEN`/`THEN`/`AND`.

Alle konkreten Beispiele in diesem Skill — hier, in `SKILL.md`, in `templates/` und in `beispiel/` — zeigen durchgehend den deutschen Fall (`lang: de`); bei `lang: en` gilt dieselbe Form auf Englisch, uebersetzt wird an den Beispielen selbst nichts.

### Modalverben — nur drei

| Erlaubt (de) | Erlaubt (en) | Bedeutung |
|---|---|---|
| `muss` | `must` | zwingend. Fehlt es, ist die Anforderung nicht erfuellt |
| `wird` | `will` | Zusicherung ueber das Verhalten. Praktisch wie `muss`/`must`, liest sich in Ablaufbeschreibungen besser |
| `kann` | `can` | Faehigkeit oder echte Option. **Nicht** als hoefliches `muss`/`must` verwenden |

**Verboten (de)**: `sollte`, `moeglichst`, `idealerweise`, `zeitnah`, `performant`, `benutzerfreundlich`, `robust`, `sinnvoll`, `gegebenenfalls`, `in der Regel`.
**Verboten (en)**: `should`, `where possible`, `ideally`, `promptly`, `performant`, `user-friendly`, `robust`, `reasonable`, `where applicable`, `typically`.

Der Grund ist nicht Stil. Diese Woerter machen eine Anforderung unpruefbar — beim Verifizieren laesst sich nicht feststellen, ob der Code sie erfuellt, und beim Kunden laesst sich nicht feststellen, ob geliefert wurde. Dieselbe Logik wie RFC 2119, auf den ganzen Text angewandt — in beiden Sprachen gleichermassen.

### Szenario-Schluesselwoerter

| Deutsch | Englisch | Bedeutung |
|---|---|---|
| `WENN` | `WHEN` | Ausloeser |
| `DANN` | `THEN` | beobachtbares Ergebnis |
| `UND` | `AND` | weiteres beobachtbares Ergebnis, an WENN/WHEN oder DANN/THEN angehaengt |

## Antipatterns

### Unpruefbar

```markdown
✗ Der Import sollte moeglichst schnell durchlaufen.
✓ Der Import einer Datei mit 10.000 Zeilen muss in unter 60 Sekunden abschliessen.
```

Wenn keine Zahl bekannt ist, ist das ein Ergebnis, kein Mangel: die Zahl gehoert in `## Open Questions` des Proposals und wird erfragt. Eine erfundene Zahl ist schlimmer als eine offene Frage.

### Implementierung statt Verhalten

```markdown
✗ Das System verwendet eine Queue fuer den Import.
✓ Waehrend ein Import laeuft, kann ein zweiter gestartet werden; beide laufen
  vollstaendig durch.
```

Wie es gebaut wird, gehoert in `design.md`. In der Spec steht, was beobachtbar ist — sonst ist jeder Refactor formal ein Spec-Bruch.

### Szenario ohne beobachtbares Ergebnis

```markdown
✗ WENN eine CSV hochgeladen wird
  DANN wird sie korrekt verarbeitet
✓ WENN eine CSV mit 500 gueltigen Artikelzeilen hochgeladen wird
  DANN werden 500 Artikel angelegt
  UND das Protokoll weist 500 Erfolge und 0 Fehler aus
```

„Korrekt" ist kein Ergebnis. Test: **koennte jemand, der das System nicht kennt, entscheiden ob DANN eingetreten ist?** Nein → umschreiben.

### Mehrere Anforderungen in einer

```markdown
✗ ### Requirement: Artikel koennen importiert, exportiert und geloescht werden
✓ drei Anforderungen
```

Sie werden zu unterschiedlichen Zeiten fertig, brauchen unterschiedliche Szenarien und werden einzeln geaendert. Zusammengefasst kann keine davon je auf „erfuellt" gehen.

### Synonymketten

```markdown
✗ Die Datei wird geprueft. … Nach der Validierung … … sobald die Verifikation
✓ durchgehend: geprueft
```

Ein Begriff, eine Bedeutung. Betrifft besonders Fachbegriffe des Kunden: heisst es beim Kunden „Warengruppe", heisst es in der Spec „Warengruppe" — auch wenn die Tabelle `category` heisst und der Endpoint `/categories`. Die Spec spricht die Sprache des Kunden, der Code seine eigene.

### Negativ-Anforderungen ohne Fall

```markdown
✗ Das System darf keine ungueltigen Daten annehmen.
✓ #### Scenario: Zeile ohne Artikelnummer
  - **WENN** eine Zeile ohne Artikelnummer eingelesen wird
  - **DANN** wird sie abgewiesen
  - **UND** der Grund "Artikelnummer fehlt" steht im Fehlerprotokoll
```

„Keine ungueltigen Daten" ist unendlich gross und damit nicht pruefbar. Jeder Ausschluss braucht seinen konkreten Fall.

## Wie viele Szenarien

Faustregel: **ein Szenario je Verzweigung, die dem Nutzer auffaellt.** Also mindestens der gute Fall und jeder Fehlerfall, der anders aussieht. Nicht: jede technische Verzweigung — Unit-Tests decken die ab, die Spec nicht.

Wenn eine Anforderung mehr als ~7 Szenarien braucht, ist sie meist mehrere Anforderungen.

## Was NICHT in die Spec gehoert

- **Technik** (Bibliotheken, Schema, Endpoint-Namen) → `design.md`
- **Aufwand, Termine, Preis** → `proposal.md` bzw. das Angebot
- **Reihenfolge der Umsetzung** → `tasks.md`
- **Warum wir uns so entschieden haben** → `project/decisions/`

Die Spec beantwortet genau eine Frage: **was kann das System, und woran erkennt man es.**
