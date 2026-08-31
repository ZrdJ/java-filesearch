# Phase 4 — archive

Das Delta in die Ist-Spec einarbeiten und den Change wegraeumen. Ohne CLI ist das Handarbeit, und es ist der Schritt, an dem das Modell kaputtgeht, wenn er schlampig laeuft: eine nicht eingearbeitete Aenderung heisst, dass `specs/` ab sofort luegt — ohne dass irgendwo eine Fehlermeldung erscheint.

## Gate — erst wenn alles davon stimmt

- [ ] Alle Slices in `tasks.md` sind `done` oder `dropped` (mit Begruendung)
- [ ] Phase 3 (`verify`) ist gelaufen, **keine** offene Zeile
- [ ] Jede Anforderung des Changes hat ein gruenes Szenario **oder** eine Notiz, warum nicht
- [ ] Test-/Build-Gate des Repos ist gruen
- [ ] Slice-Tabelle und `git log` stimmen ueberein (naechster Abschnitt)
- [ ] MODIFIED/REMOVED-Kennungen treffen Anforderungen der Ist-Spec

Ein Haken fehlt → nicht archivieren. Der Change bleibt `active`, das ist kein Makel.

## Slice-Tabelle gegen `git log` abgleichen

**In beide Richtungen**, das ist der Punkt:

```bash
git log --oneline origin/main
```

| Befund | Bedeutung | Was tun |
|---|---|---|
| Slice `open`, Code liegt auf dem Default-Branch | Tabelle ist stale | Status nachziehen |
| Slice `done`, kein Commit dafuer | Status ist geraten, nicht beobachtet | pruefen und korrigieren |

Der Status in `tasks.md` ist **Anzeige, nicht Wahrheit**. Wahrheit ist: ein Slice ist fertig, wenn seine Commits auf dem Default-Branch sind. Dieser Abgleich ist die einzige Stelle, an der die Tabelle nicht still falsch werden kann — deshalb faellt er nicht weg, auch wenn „eh klar ist", dass alles fertig ist.

## Der Merge — Marker fuer Marker

Ziel ist `docs/specs/{capability}/spec.md`, Quelle `docs/changes/{slug}/specs/{capability}/spec.md`. Je Faehigkeit einmal.

**Existiert die Ist-Spec noch nicht** (neue Faehigkeit): aus `templates/spec.md` anlegen, dann weiter.

### `## ADDED Requirements`

Jede Anforderung darunter ans **Ende** der `## Requirements` in der Ist-Spec anhaengen — Marker-Ueberschrift selbst **nicht** mitkopieren, Kennungszeile dagegen schon. In der Ist-Spec gibt es kein `ADDED`, dort steht nur, was gilt.

Vorher pruefen: existiert die Kennung bereits? Dann war es faelschlich als ADDED markiert und ist in Wahrheit MODIFIED.

### `## MODIFIED Requirements`

Anforderung mit **derselben Kennung** in der Ist-Spec suchen und **vollstaendig ersetzen** — Ueberschrift, Kennungszeile, Fliesstext, alle Szenarien.

**Gesucht wird ueber die Kennung, nicht ueber den Titel.** Der Titel darf sich geaendert haben; das ist der Zweck der Kennung. Verglichen wird der Teil vor der Revision (`req~{capability}.{kurzname}`), damit eine erhoehte Revision den Treffer nicht verhindert.

- Die Zeile `Previously: …` aus dem Delta wird **nicht** mitkopiert. Sie hat ihren Zweck beim Review erfuellt; in der Ist-Spec waere sie Historie, und Historie steht im Archiv.
- Kennung nicht gefunden → **stoppen**. Nicht als ADDED anhaengen; das erzeugt eine Dublette, und ab da gibt es zwei widersprechende Anforderungen. Ursache klaeren: Tippfehler im Delta, oder wurde die Anforderung zwischenzeitlich von einem anderen Change entfernt?

### `## REMOVED Requirements`

Anforderung mit dieser Kennung aus der Ist-Spec **loeschen**, samt Szenarien. Der Grund aus dem Delta wandert **nicht** in die Ist-Spec — er bleibt im archivierten Change, und dorthin fuehrt die Spur.

**Traegt der Delta-Block eine Zeile `Superseded by:`, bleibt ein Grabstein** an der Stelle der geloeschten Anforderung:

```markdown
### Superseded: Ohne Anmeldung kein Zugriff
`req~zugang.ohne-anmeldung-kein-zugriff~1`
Superseded by: `req~zugang.rolle-entscheidet-ueber-zugriff~1`
```

Der Grabstein macht den alten Verweis **nicht** wieder gueltig. Ein Test, der auf die abgeloeste Kennung zeigt, bricht den Lauf weiterhin — der Grabstein sorgt nur dafuer, dass die Fehlermeldung sein Ziel nennt. Ohne `Superseded by:` faellt die Anforderung ersatzlos weg und hinterlaesst nichts.

Kennung nicht gefunden → pruefen, ob sie ein frueherer Change schon entfernt hat. Dann ist es kein Fehler, nur eine ueberfluessige Zeile im Delta.

### Danach

Ist-Spec einmal ganz lesen. Zwei Dinge, die der mechanische Merge nicht sieht:

- **Widersprueche** zwischen einer neuen und einer alten Anforderung
- **Begriffsdrift** — die neue Anforderung sagt „Warengruppe", eine alte sagt an derselben Stelle „Kategorie"

Beides jetzt aufloesen. Spaeter findet es niemand mehr.

## Verschieben

```
docs/changes/{slug}/  →  docs/archive/{YYYY-MM}/{slug}/
```

`{YYYY-MM}` ist der Monat des **Archivierens**, nicht der des Anlegens. Im `proposal.md`: `status: fulfilled`, `updated:` auf heute.

Der Change wird **vollstaendig** verschoben, inklusive Delta-Spec. Sie ist ab jetzt Historie und wird nie wieder angefasst — aber sie ist der Beleg dafuer, wie die Ist-Spec zu ihrem heutigen Stand kam.

## Nachziehen

- [ ] `docs/project/worklog/{YYYY-MM-DD}.md` — ein Eintrag, was der Change gebracht hat
- [ ] Offene Ausloeser-Referenzen abhaken, die auf diesen Change zeigten — je nachdem, was die Ebene zur Herkunfts-Verfolgung nutzt (z. B. ein Meeting-Skill, ein Tracker, ein Issue)
- [ ] Entstand unterwegs eine Entscheidung, die jemand spaeter hinterfragt → `docs/project/decisions/`

## Wenn ein Change nicht kommt

Nicht archivieren, sondern verwerfen:

1. `status: rejected` im `proposal.md`, Begruendung als Abschnitt darunter — **dauerhaft** begruendet, nicht „gerade keine Zeit" (das ist eine Verschiebung, dann bleibt der Change `draft`).
2. Eine Note unter `docs/project/decisions/` mit `status: rejected`. **Dort** wird beim naechsten Mal gesucht, nicht im Archiv.
3. Verzeichnis nach `docs/archive/{YYYY-MM}/{slug}/` verschieben.
4. **Kein Merge.** Die Ist-Spec bleibt unveraendert — es wurde ja nichts gebaut.
