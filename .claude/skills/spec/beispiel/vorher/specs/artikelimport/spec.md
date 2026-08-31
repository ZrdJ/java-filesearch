---
type: spec
title: Artikelimport
updated: 2026-05-14
---

## Purpose

Ermoeglicht der Sachbearbeitung, Artikelstammdaten aus dem Lieferantensystem
als CSV in den Shop zu uebernehmen, statt sie einzeln von Hand anzulegen —
bei einem Sortimentswechsel mit tausenden Zeilen der einzige praktikable Weg.

## Requirements

### Requirement: Artikelstammdaten koennen als CSV importiert werden

Das System muss CSV-Dateien mit Artikelstammdaten einlesen und die
enthaltenen Artikel anlegen oder aktualisieren.

#### Scenario: Import einer gueltigen Datei

- **WENN** eine CSV mit 500 gueltigen Artikelzeilen hochgeladen wird
- **DANN** werden alle 500 Artikel angelegt

#### Scenario: Datei mit fehlerhafter Zeile

- **WENN** eine CSV hochgeladen wird, in der eine Zeile fehlerhaft ist
- **DANN** wird der Import abgebrochen
- **UND** keine Zeile der Datei wird uebernommen

### Requirement: Artikel tragen eine Warengruppe

Ein Artikel kann einer Warengruppe zugeordnet werden. Die Zuordnung ist
optional.

#### Scenario: Import ohne Warengruppe

- **WENN** eine Artikelzeile keine Warengruppe nennt
- **DANN** wird der Artikel ohne Warengruppe angelegt

### Requirement: Der Importverlauf kann als Rohprotokoll heruntergeladen werden

Nach einem Import kann die unveraenderte Ausgabe des Importvorgangs als
Textdatei geladen werden.

#### Scenario: Protokoll nach Import

- **WENN** ein Import abgeschlossen ist
- **DANN** kann die Textdatei ueber die Importuebersicht geladen werden
