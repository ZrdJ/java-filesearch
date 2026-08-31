{Delta-Spec eines Changes. Liegt unter changes/{slug}/specs/{capability}/spec.md.
Nicht verwechseln mit der Ist-Spec unter docs/specs/{capability}/spec.md.

Nur die Marker verwenden, die wirklich vorkommen — leere Marker weglassen.
Bei MODIFIED und REMOVED muss der Titel WORTGLEICH dem in der Ist-Spec
entsprechen, sonst schlaegt der Merge beim Archivieren fehl.}

## ADDED Requirements

### Requirement: {was moeglich ist}
`req~{capability}.{kurzname}~1`

{1-3 Saetze Praezisierung. Modalverben nur kann/wird/muss.}

#### Scenario: {konkreter Fall}

- **WENN** {Ausloeser}
- **DANN** {beobachtbares Ergebnis}
- **UND** {weiteres beobachtbares Ergebnis}

#### Scenario: {Fehlerfall}

- **WENN** {Ausloeser}
- **DANN** {beobachtbares Ergebnis}

## MODIFIED Requirements

### Requirement: {Titel — darf vom bisherigen abweichen}
`req~{capability}.{kurzname}~{revision}`

{VOLLSTAENDIGER neuer Text, nicht nur die Aenderung — beim Archivieren
wird ersetzt, nicht gepatcht.

Die Kennung ist dieselbe wie in der Ist-Spec; der Merge sucht ueber sie.
Revision nur erhoehen, wenn sich ein Szenario so aendert, dass die
Zusicherung eine andere ist — Regel im Skill `traceability`.}

#### Scenario: {…}

- **WENN** {…}
- **DANN** {…}

Previously: {ein Satz, was vorher galt. Wird beim Archivieren NICHT
mit in die Ist-Spec uebernommen.}

## REMOVED Requirements

### Requirement: {Titel}
`req~{capability}.{kurzname}~{revision}`

Reason: {warum sie wegfaellt}
Superseded by: `req~{capability}.{kurzname}~1`

{Die Zeile "Superseded by" nur setzen, wenn eine andere Anforderung
an ihre Stelle tritt. Faellt sie ersatzlos weg, bleibt die Zeile weg —
dann hinterlaesst sie keinen Grabstein.}
