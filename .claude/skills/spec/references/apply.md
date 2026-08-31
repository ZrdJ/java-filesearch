# Phase 2 — apply

Slices abarbeiten. Der Change ist auf `status: active`, `tasks.md` ist gefuellt.

## Was als naechstes dran ist

Nicht pflegen, sondern **ableiten**: die niedrigste Nummer in `tasks.md`, die `open` ist und deren `Blocked by`-Eintraege `done` sind. Gibt es keine, ist entweder alles fertig oder die Blockade-Kanten sind falsch gesetzt.

## Ein Slice

1. **Seam klaeren.** Wo wird verifiziert? Steht in `design.md` → Test-Seams. Steht dort nichts und die Repo-`CLAUDE.md` nennt auch keinen, wird er **ausgehandelt und eingetragen** — nicht angenommen. Ein Test am falschen Seam ist teurer als keiner: er bindet die Implementierung fest, ohne das Verhalten zu sichern.
2. **Umsetzen**, Test am vereinbarten Seam.
3. **Gate laufen lassen** — den Build-/Test-Einstieg, den die Repo-`CLAUDE.md` (oder eine Ebene darueber) als kanonisch nennt. Nennt sie keinen, wird er ausgehandelt und dort nachgetragen — nicht geraten.
4. **Status in `tasks.md`** nachziehen.
5. **`docs/project/worklog/{YYYY-MM-DD}.md`** ergaenzen, wenn etwas passiert ist, das **nicht im Diff steht**: eine Sackgasse, eine Kundenaussage am Telefon, ein Grund fuer einen Umweg. Steht es im Diff, gehoert es nicht ins Log.

## Richtungswechsel — anhaengen, nie ueberschreiben

Aendert sich das Ziel mitten im Change, wird der urspruengliche Text **nicht** korrigiert. Stattdessen ans `proposal.md`:

```markdown
## Richtungswechsel

- 2026-08-20 — Dubletten werden nicht uebersprungen, sondern zusammengefuehrt.
  Ausloeser: Jour fixe 2026-08-20 (Referenz nach dem Schema der jeweiligen Ebene —
  Themenblock-ID, Ticket, Protokoll-Link)
```

Danach die Delta-Spec entsprechend anpassen — **die** wird ueberschrieben, denn sie beschreibt das Ziel, nicht die Historie.

Warum die Trennung: wer spaeter nur das Endergebnis liest, versteht nicht, warum das System aussieht wie es aussieht. Der Richtungswechsel ist genau die Information, die sonst verloren geht — und die, nach der bei spaeteren Nachtragsdiskussionen gefragt wird.

Neue Anforderung mitten im Change: erst pruefen, ob sie in **diesen** Change gehoert oder ein eigener ist. Faustregel — bringt sie eine neue Faehigkeit, ist es ein eigener Change. Praezisiert sie eine bestehende, gehoert sie hierher.

## Slices, die sich als falsch erweisen

Kommt heraus, dass ein Slice nicht geht wie geplant:

- **Zuschnitt falsch** → Zeile umformulieren, Nummer behalten. Nummern werden nie neu vergeben.
- **Ueberfluessig** → Status auf `dropped`, mit einem Halbsatz warum. Nicht loeschen; sonst fehlt beim Archivieren eine Nummer und niemand weiss, ob sie vergessen wurde.
- **Zu gross** → hinten anhaengen statt einschieben. `01` wird zu `01` + `04`, mit `Blocked by 01` bei `04`.

## Wann Phase 2 endet

Wenn alle Slices `done` oder `dropped` sind. Dann Phase 3 — **nicht** direkt archivieren. Der Schritt, den man auslaesst, wenn es eilig ist, ist genau der, der die Drift verhindert.
