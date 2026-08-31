# Beispiel — ein Change von Ende zu Ende

Fiktiv, aber vollstaendig. Zeigt das Einzige, was sich in Prosa schlecht
erklaeren laesst: **wie aus Ist-Spec + Delta die neue Ist-Spec wird.**

## Lesereihenfolge

| # | Datei | Was man daran sieht |
|---|---|---|
| 1 | `vorher/specs/artikelimport/spec.md` | Ist-Zustand, drei Anforderungen |
| 2 | `2026-08-11-artikelimport/proposal.md` | Problem, Loesung, **Out of Scope**, `origin:` |
| 3 | `2026-08-11-artikelimport/specs/artikelimport/spec.md` | Delta mit allen drei Markern |
| 4 | `2026-08-11-artikelimport/design.md` | Technik + Test-Seams |
| 5 | `2026-08-11-artikelimport/tasks.md` | vertikale Slices |
| 6 | `nachher/specs/artikelimport/spec.md` | Ergebnis des Merges |

## Was der Merge gemacht hat

| Marker | Wirkung auf die Ist-Spec |
|---|---|
| `MODIFIED` „…als CSV importiert werden" | an Ort und Stelle **ersetzt**, `Previously:`-Zeile **nicht** uebernommen |
| `MODIFIED` „Artikel tragen eine Warengruppe" | ebenso ersetzt |
| `REMOVED` „Importverlauf … Rohprotokoll" | **geloescht**, Grund bleibt im archivierten Change |
| `ADDED` „Vorschau vor dem Import" | **ans Ende** angehaengt |

Die Reihenfolge der bestehenden Anforderungen bleibt erhalten — Ersetzen
verschiebt nichts. Nur Neues waechst hinten an.

## Was hier absichtlich fehlt

`vorher/` und `nachher/` sind eine Lernhilfe. Im echten `docs/` gibt es
sie nicht: dort existiert genau **eine** `specs/artikelimport/spec.md`,
und die Historie steht in `archive/`.
