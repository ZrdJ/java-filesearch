---
type: change
title: Slices Teilimport
updated: 2026-08-25
---

| # | Slice | Project | Blocked by | Status |
|---|---|---|---|---|
| 01 | Pruefroutine je Zeile, Gruende als Aufzaehlung | artikelimport | — | done |
| 02 | Import zeilenweise mit Fehlerprotokoll | artikelimport | 01 | done |
| 03 | Warengruppe als Pflichtfeld im Import | artikelimport | 01 | done |
| 04 | Vorschau-Endpoint auf derselben Pruefroutine | artikelimport | 01 | done |
| 05 | Vorschau-Maske mit Abbrechen | artikelimport | 04 | done |
| 06 | Rohprotokoll-Download entfernen | artikelimport | 02 | done |

Status: `open` · `in progress` · `done` · `dropped` (mit Halbsatz warum)

Slice 04 haengt an 01, nicht an 02 — die Vorschau braucht die Pruefroutine,
nicht den schreibenden Import. Deshalb konnten 02 und 04 parallel laufen.
