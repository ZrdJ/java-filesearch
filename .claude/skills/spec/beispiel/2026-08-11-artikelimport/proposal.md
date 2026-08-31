---
type: change
title: Teilimport statt Abbruch, Warengruppe verpflichtend
updated: 2026-08-11
status: fulfilled
projects: [artikelimport]
origin: [rekonstruiert]
---

## Problem

Der Sortimentswechsel im Fruehjahr hat gezeigt, dass der Import in der
Praxis nicht durchlaeuft: eine einzige fehlerhafte Zeile bricht die ganze
Datei ab. Bei 4.000 Zeilen aus dem Lieferantensystem ist immer eine dabei.
Die Sachbearbeitung sucht den Fehler dann im Rohprotokoll, korrigiert die
Quelldatei und startet neu — im Schnitt sieben Durchlaeufe je Lieferung.

Zweitens sind Artikel ohne Warengruppe im Shop nicht auffindbar. Weil die
Zuordnung optional ist, faellt das erst beim Kunden auf.

## Solution

Der Import laeuft durch und uebernimmt alles, was gueltig ist. Fehlerhafte
Zeilen werden einzeln mit Grund ausgewiesen, statt die Datei zu verwerfen.
Die Sachbearbeitung sieht vor dem Import eine Vorschau mit der Zahl der
betroffenen Zeilen und kann abbrechen, bevor etwas geschrieben wird.

Artikel ohne Warengruppe werden beim Import abgewiesen — nicht mehr still
ohne Warengruppe angelegt.

## Out of Scope

- **Korrektur in der Oberflaeche.** Fehlerhafte Zeilen werden ausgewiesen,
  nicht editierbar gemacht. Korrigiert wird in der Quelldatei.
- **Automatischer Import per Zeitplan.** Bleibt manuell angestossen.
  Automatik erst, wenn der manuelle Weg im Betrieb steht.
- **Anlegen fehlender Warengruppen.** Der Import legt keine Warengruppen
  an; unbekannte fuehren zur Abweisung der Zeile.
- **Rueckgaengigmachen eines Imports.** Kein Undo. Dafuer gibt es die
  Vorschau.

## Open Questions

- Ab welcher Fehlerquote soll die Vorschau warnen statt nur zaehlen?
  → geklaert am 2026-08-11: keine Warnschwelle, die Zahl reicht
