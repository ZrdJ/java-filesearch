## ADDED Requirements

### Requirement: Vor dem Import kann eine Vorschau erzeugt werden

Das System muss eine hochgeladene Datei pruefen und das Ergebnis anzeigen,
ohne Artikel zu schreiben.

#### Scenario: Vorschau einer gemischten Datei

- **WENN** eine CSV mit 4.000 Zeilen hochgeladen wird, von denen 12 fehlerhaft sind
- **DANN** weist die Vorschau 3.988 uebernehmbare und 12 fehlerhafte Zeilen aus
- **UND** kein Artikel wird angelegt oder geaendert

#### Scenario: Import nach Vorschau abbrechen

- **WENN** die Vorschau angezeigt wird und der Vorgang abgebrochen wird
- **DANN** wird kein Artikel angelegt oder geaendert

## MODIFIED Requirements

### Requirement: Artikelstammdaten koennen als CSV importiert werden

Das System muss CSV-Dateien mit Artikelstammdaten einlesen und die
enthaltenen Artikel anlegen oder aktualisieren. Fehlerhafte Zeilen werden
uebersprungen, nicht die Datei verworfen.

#### Scenario: Import einer gueltigen Datei

- **WENN** eine CSV mit 500 gueltigen Artikelzeilen hochgeladen wird
- **DANN** werden alle 500 Artikel angelegt
- **UND** das Fehlerprotokoll weist 0 Fehler aus

#### Scenario: Datei mit fehlerhaften Zeilen

- **WENN** eine CSV hochgeladen wird, in der Zeile 12 eine unbekannte Warengruppe nennt
- **DANN** werden die uebrigen Zeilen importiert
- **UND** Zeile 12 wird mit Grund "Warengruppe unbekannt" im Fehlerprotokoll ausgewiesen
- **UND** der Import wird nicht abgebrochen

#### Scenario: Datei ohne eine einzige gueltige Zeile

- **WENN** eine CSV hochgeladen wird, in der jede Zeile fehlerhaft ist
- **DANN** wird kein Artikel angelegt
- **UND** das Fehlerprotokoll weist jede Zeile mit Grund aus

Previously: eine einzige fehlerhafte Zeile brach den gesamten Import ab, keine
Zeile der Datei wurde uebernommen.

### Requirement: Artikel tragen eine Warengruppe

Jeder Artikel muss einer bekannten Warengruppe zugeordnet sein. Beim Import
ist die Angabe verpflichtend.

#### Scenario: Import ohne Warengruppe

- **WENN** eine Artikelzeile keine Warengruppe nennt
- **DANN** wird die Zeile abgewiesen
- **UND** der Grund "Warengruppe fehlt" steht im Fehlerprotokoll

#### Scenario: Import mit unbekannter Warengruppe

- **WENN** eine Artikelzeile eine Warengruppe nennt, die es nicht gibt
- **DANN** wird die Zeile abgewiesen
- **UND** der Grund "Warengruppe unbekannt" steht im Fehlerprotokoll

Previously: die Zuordnung war optional, Artikel ohne Warengruppe wurden
angelegt.

## REMOVED Requirements

### Requirement: Der Importverlauf kann als Rohprotokoll heruntergeladen werden

Reason: abgeloest durch das strukturierte Fehlerprotokoll, das jede
abgewiesene Zeile mit Nummer und Grund ausweist. Das Rohprotokoll war der
Behelf, solange es das nicht gab.
