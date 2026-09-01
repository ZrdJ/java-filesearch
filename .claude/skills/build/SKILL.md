---
name: build
version: 1
description: Bauen, testen, linten und typechecken — immer ueber den Devcontainer, nie nativ. Findet die projektspezifischen Befehle in der Repo-CLAUDE.md statt sie zu raten. Triggers auf bauen, build, compile, test, lint, typecheck, verify, "laeuft das durch", "vor dem Push", CI lokal, Devcontainer, ./dev.
# GENERIERT aus personal/skills-ref/build/ — nicht hier editieren; Aenderungen gehoeren nach ~/.claude/skills-ref/build/.
source: personal-provider-ref
ref-hash: sha256:00d4aeafdd29dd31bf449c357551de121d9bc7fefe23ca18efd8804229a0f51e
---

# build

Lokale CI-Simulation: dieselben Schritte wie in der Pipeline, bevor Code weggeht.

Dieser Skill traegt das **Konzept**. Die konkreten Befehle dieses Repos stehen nicht hier — siehe [Woher die Befehle kommen](#woher-die-befehle-kommen).

## Zwei Regeln, die nicht verhandelbar sind

**1. Die KI baut NIE nativ.** Build, Test, Lint, Typecheck, Verify und Package-Install laufen ausschliesslich ueber den Devcontainer — in **beiden** Kontexten, Host und Sandbox. Direkte Aufrufe nativer Toolchains (`mvn`, `mvnw`, `npm`, `pnpm`, `yarn`, `go build`, `go test`, `gradle`, `gradlew`, `cargo`, `dotnet`) und erst recht SDK-Installs (`mise use --global`, `nvm`, `sdkman`, `asdf`, `go install …@latest`) sind **User-only**.

Der Grund ist nicht Bequemlichkeit: Build-Toolchains sind der groesste Supply-Chain-Vektor, den es gibt. Ein `postinstall`-Script, ein Maven-Plugin, ein crates.io-Build-Script — alles laeuft mit vollen Nutzerrechten und sieht dann `~/.ssh`, `~/.gitconfig`, Browser-Profile, Keychain. Container existieren, **damit** das in einer Wegwerf-Umgebung passiert. Nativ auszuweichen „nur kurz zum Verifizieren" hebt genau den Schutz auf, fuer den der Container da ist.

**2. Am Host startet die KI die Anwendung nicht.** Bauen ja, hochfahren nein. `./dev dev|run|start|serve|watch`, `docker compose up`, jeder Dev-Server, jeder Long-running-Prozess: am Host **User-Vorbehalt**. Er hat die Anwendung in seiner IDE laufen; ein zweiter Start kollidiert um Ports, Datenbank-Zustand und Log-Ausgabe. In der **Sandbox** ist App-Start erlaubt, mit `run_in_background` und Timeout.

### Die Trennlinie

| Kommando-Klasse | Host | Sandbox |
|---|---|---|
| `compile` · `build` · `test` · `lint` · `typecheck` · `verify` · `package` | **ja**, via Devcontainer | ja |
| Codegen, das durchlaeuft und endet | **ja** | ja |
| `dev` · `run` · `start` · `serve` · `watch` · `compose up` | **nein — User** | ja (`run_in_background`) |
| Browser-Smoke-Test gegen selbst gestartete Instanz | **nein — User** | ja |

Merkmal: **endet der Befehl von selbst?** Dann ist es Verifikation → erlaubt. Laeuft er, bis jemand abbricht? Dann ist es App-Start → am Host User-Vorbehalt.

Braucht eine Verifikation zwingend eine laufende Instanz: **den User fragen**, ob seine laeuft und was sie sagt. Nicht selbst starten.

## Woher die Befehle kommen

In dieser Reihenfolge, die erste Quelle gewinnt:

1. **`CLAUDE.md` dieses Repos → Abschnitt `## Bauen und Testen`.** Dort stehen die Befehle, das CI-Aequivalent und die Eigenheiten. Das ist die deklarierte Stelle — sie wird gelesen, nicht uebersprungen.
2. **`./dev` ohne Argument.** Listet alle Subcommands. Das ist die Quelle, wenn CLAUDE.md schweigt oder unvollstaendig ist.
3. **Kein `./dev`, aber `.devcontainer/`** → `devcontainer up --workspace-folder .` einmalig, danach `devcontainer exec --workspace-folder . sh -c '<cmd>'`.
4. **Nichts davon vorhanden** → es gibt (noch) keinen definierten Build. Das wird **gesagt**, nicht durch einen geratenen Befehl ueberspielt.

**Raten ist verboten.** Nicht annehmen, dass es `npm run build` ist — es kann `pnpm`, `yarn`, `vite`, `vinxi` oder ein eigenes Target sein. Nicht annehmen, dass `test` existiert. Ein falsch geratener Befehl, der zufaellig durchlaeuft, ist schlimmer als eine Rueckfrage.

**Dieser Skill wird nicht um Projekt-Befehle erweitert.** Er ist eine generierte Kopie aus `skills-ref/` — eine Aenderung hier erreicht kein anderes Repo und blockiert den naechsten Sync. Projekt-Fakten gehoeren in `CLAUDE.md` → `## Bauen und Testen`.

## Pre-flight

```bash
docker info >/dev/null 2>&1 && echo "Daemon OK"
devcontainer --version                     # nur noetig fuer direkten devcontainer exec
```

Ohne laufenden Docker-Daemon kein Build — der Container **ist** das Build-Backend. Fehlt die Devcontainer-CLI, wird sie installiert (Standalone-Installer, nicht per npm), **nicht** auf nativen Build ausgewichen.

Nicht mehr pruefen oder installieren: SDKs am Host. Die Toolchain lebt im Container.

## Ausfuehren

`./dev <command>` im Repo-Root ist der Standardweg; das Skript ist container-aware und entscheidet selbst, ob es nativ laeuft (im Container) oder `devcontainer exec` wrappt (am Host).

Ohne `./dev`:

```bash
devcontainer exec --workspace-folder . sh -c '<cmd>'
```

Native Befehle in Repo-Doku sind **Referenz fuer den Inhalt**, kein Ausfuehrungsweg.

## Verifikation

- Alle Befehle mit Exit Code 0
- Keine Lint- oder Test-Fehler
- Lockfiles synchron und ohne Diff nach dem Lauf (`go.sum`, `package-lock.json`, `pnpm-lock.yaml`)
- Keine unaufgeloesten Abhaengigkeiten

Erzeugt ein Build-Schritt Diffs in getrackten Dateien (typisch bei `go mod tidy` oder Lockfile-Updates), gehoeren die committet — nicht verworfen.

## Troubleshooting

| Problem | Ursache | Loesung |
|---|---|---|
| `command not found: devcontainer` | CLI fehlt am Host | Standalone-Installer, **nicht** nativ ausweichen |
| Build „will" nativ laufen | Versuchung, schnell zu verifizieren | STOP. Nativ ist User-only, ohne Ausnahme |
| Kein `./dev`, kein `.devcontainer/` | Repo hat noch kein Build-Setup | melden, nicht improvisieren |
| Testcontainers-Timeout | Ryuk ueber `172.17.0.1` nicht erreichbar | `TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal` + `--add-host=host.docker.internal:host-gateway` |
| Lockfile-Update schlaegt fehl | Lockfile veraltet | im Container regenerieren, dann committen |
| Container-Volume nicht beschreibbar | Named Volume gehoert `root` | `chown` im `post-create.sh` des Repos |

## Zum Schluss

- **Build gruen vor der Uebergabe.** Am Host committet und pusht der User — der gruene Build ist trotzdem Bringschuld, bevor uebergeben wird.
- **Push nie aus dem Container.** Der Devcontainer haelt keine Credentials und ist per Hook geblockt.
- **Fehlschlag wird berichtet**, mit Ausgabe. Nicht umgehen, nicht `--no-verify`, nicht „lief lokal aber".
