# Phase 3 — verify

Code gegen Spec pruefen. Der Schritt, der die ganze Kette traegt: ohne ihn ist die Spec eine Absichtserklaerung, die niemand je gegengelesen hat.

Laeuft **vor** dem Archivieren, darf aber jederzeit vorher schon laufen — nach jedem Slice ist besser als einmal am Ende.

## Zwei Achsen, getrennt halten

**Spec-Achse** — stimmt der Code mit dem ueberein, was gefordert war? Laeuft immer.

**Standards-Achse** — haelt der Code die Konventionen des Repos ein? Laeuft **nur, wenn kein Werkzeug sie erzwingt.**

Erkennungsschritt zuerst: gibt es ArchUnit-Tests, Custom-Lint-Regeln, Layer-Tests, einen Formatter im Gate? Dann erzwingt das Tooling die Standards, die Achse wird **uebersprungen** und das wird gesagt — nicht stillschweigend doch geprueft. Doppelte Pruefung kostet Zeit und erzeugt Funde, die das Gate ohnehin blockt.

Die beiden Achsen werden **nicht** zu einer Liste gemischt. Sonst maskiert die eine die andere: zwanzig Formatierungsfunde begraben den einen fehlenden Fehlerfall.

## Spec-Achse — drei Sorten Fund

### 1. Fehlt

Eine Anforderung oder ein Szenario aus der Delta-Spec, fuer die es im Code nichts gibt.

```markdown
FEHLT — specs/artikelimport/spec.md → "Scenario: Datei mit fehlerhaften Zeilen"
  Gefordert: die uebrigen Zeilen werden importiert, Zeile 12 landet im
  Fehlerprotokoll, der Import bricht nicht ab.
  Gefunden: ImportService bricht beim ersten Fehler ab (import_service.ts:88),
  kein Fehlerprotokoll.
```

### 2. Zu viel (Scope-Creep)

Verhalten im Code, das **keine** Anforderung fordert. Der haeufigste und teuerste Fund — er kostet Pflegeaufwand, ohne dass ihn eine Anforderung rechtfertigt.

```markdown
ZU VIEL — kein Bezug in specs/
  Gefunden: automatischer Import per Cron (scheduler.ts:12).
  Das Proposal nennt "Automatischer Import per Zeitplan" ausdruecklich
  unter "Out of Scope".
```

Zwei Ausgaenge, beide bewusst: entweder raus, oder die Anforderung wird nachgetragen (dann ist es ein Richtungswechsel und gehoert ins `proposal.md`). Nie „lassen wir mal drin".

### 3. Sieht implementiert aus, ist es aber nicht

Der gefaehrlichste Fund. Es gibt Code, der die Anforderung zu erfuellen scheint, tut es aber nicht — falscher Randfall, vertauschte Bedingung, Fehler wird geschluckt.

```markdown
FALSCH — specs/artikelimport/spec.md → "Scenario: Zeile ohne Artikelnummer"
  Gefordert: Zeile wird abgewiesen, Grund "Artikelnummer fehlt" im Protokoll.
  Gefunden: die Zeile wird abgewiesen, der Grund ist aber hart auf
  "Validierungsfehler" gesetzt (validator.ts:44) — der geforderte Grund
  steht nirgends.
```

## Regel fuer jeden Fund

**Jeder Fund zitiert seine Spec-Zeile** (Datei + Anforderungs- oder Szenario-Titel) und die Code-Stelle (Datei:Zeile). Ein Fund ohne beides ist eine Meinung und wird nicht berichtet.

Umgekehrt: laesst sich ein Verdacht nicht an eine Spec-Zeile binden, ist er entweder Scope-Creep (Sorte 2) oder gehoert gar nicht in diesen Schritt — dann ist es normales Code-Review, nicht `verify`.

## Was verify NICHT ist

- **Kein Code-Review** auf Lesbarkeit, Benennung, Struktur. Dafuer gibt es `/code-review`.
- **Kein Test-Ersatz.** Ein gruener Test ist ein staerkerer Beleg als jede Lektuere. Wo ein Test existiert, ist er die Antwort; `verify` prueft, ob er das Richtige testet.
- **Keine Bugsuche.** Ein Bug, der keine Anforderung verletzt, gehoert nicht in diesen Bericht.

## Ergebnis

Eine Liste, nach Sorte gruppiert, jeder Fund mit Zitat. Dann eine Entscheidung je Fund:

| Fund | Ausgang |
|---|---|
| FEHLT | umsetzen, oder Anforderung streichen (= Richtungswechsel) |
| ZU VIEL | entfernen, oder Anforderung nachtragen (= Richtungswechsel) |
| FALSCH | korrigieren |

**Keine offene Zeile darf ins Archiv.** Ist ein Fund bewusst nicht behoben, wird er zur Anforderung mit `Previously:`-Notiz oder zu einer Entscheidung unter `project/decisions/` — aber nicht zu einem stillen Rest.

## Bei null Funden

Das ist ein moegliches und gutes Ergebnis — es wird berichtet, nicht durch gesuchte Funde ersetzt. Sind die Anforderungen alle durch gruene Tests belegt, ist die Aussagekraft hoch; steht keiner unter Test, ist „null Funde" schwach und das gehoert dazugesagt.
