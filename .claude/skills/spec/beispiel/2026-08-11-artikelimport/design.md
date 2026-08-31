---
type: change
title: Design Teilimport
updated: 2026-08-11
---

## Approach

Der Import laeuft zweiphasig ueber dieselbe Pruefroutine: Phase 1 (Vorschau)
prueft und schreibt nicht, Phase 2 (Import) prueft und schreibt. Damit kann
die Vorschau nicht von dem abweichen, was der Import spaeter tut — der
haeufigste Fehler bei getrennten Implementierungen.

Zeilen werden einzeln in eigener Transaktion uebernommen. Keine Sammel-
transaktion ueber die Datei: sie wuerde das Abbruchverhalten durch die
Hintertuer zurueckbringen.

## Test-Seams

| Requirement | Seam | Begruendung bei Abweichung |
|---|---|---|
| Artikelstammdaten koennen als CSV importiert werden | Integrationstest Webschicht | — |
| Artikel tragen eine Warengruppe | Integrationstest Webschicht | — |
| Vor dem Import kann eine Vorschau erzeugt werden | Integrationstest Webschicht | — |
| Zeilenweise Transaktionsgrenze | Unit-Test Importer | Transaktionsverhalten ist ueber die Webschicht nicht beobachtbar |

## Rejected Alternatives

- **Vorschau als eigener Codepfad** — schneller zu bauen, aber sie darf
  nicht anders urteilen als der Import. Getrennte Pfade driften.
- **Fehlerhafte Zeilen in eine Quarantaenetabelle** — braucht eine Oberflaeche
  zum Nacharbeiten, und die ist ausdruecklich nicht im Scope.

## Risks

- 4.000 Einzeltransaktionen sind langsamer als eine Sammeltransaktion.
  Merkbar an der Importdauer; Messung gehoert in Slice 02.
