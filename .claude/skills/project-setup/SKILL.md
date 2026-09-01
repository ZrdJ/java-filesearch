---
name: project-setup
description: Neues Entwicklungsprojekt initialisieren und Doku pflegen. Monorepo mit Docs-First-Ansatz (Astro Starlight), Requirements Engineering, Vision, Roadmap. Trennt SOLL (Architektur) von IST (Systemdokumentation), haelt Claude-Plans + TODO-Tracker im Repo. Erst nach RE werden konkrete Front-/Backend-Projekte abgeleitet.
# GENERIERT aus personal/skills-ref/project-setup/ — nicht hier editieren; Aenderungen gehoeren nach ~/.claude/skills-ref/project-setup/.
source: personal-provider-ref
ref-hash: sha256:e76621a3e67f774476a1cea4ae44d2699624b4a687dc6239d9e3ec949d404e90
---

# Project Setup Guide

Vollstaendige Richtlinien fuer das Aufsetzen neuer Entwicklungsprojekte mit Docs-First-Ansatz.

## Quick Reference

| Thema | Konvention |
|-------|------------|
| **Struktur** | Monorepo mit docs/ als erstem Ordner |
| **Docs Framework** | Astro Starlight |
| **Docs-Bereiche** | `vision/` `requirements/` `architektur/` (SOLL) `roadmap/` `systemdokumentation/` (IST) `entwicklung/` (specs/plans/implementierung) |
| **Kerntrennung** | SOLL vs IST — `architektur/` = Ziel, `systemdokumentation/` = Stand |
| **Claude-Plans** | Landen unter `entwicklung/plans/{YYYY-MM-DD}-{feature}.md` |
| **TODO-Tracker** | `entwicklung/implementierung/{stufe-X}-uebersicht.md` mit Entscheidungs- + Fortschritts-Tabelle |
| **Index-Pattern** | Jedes Verzeichnis hat `index.md` mit `## In diesem Abschnitt` + Tabelle (siehe `markdown` Skill) |
| **Erster Schritt** | Requirements Engineering |
| **Reihenfolge** | Vision → Requirements → Roadmap → Projekte |
| **Projektnamen** | `{projekt}-backend`, `{projekt}-frontend`, `{projekt}-docs` |
| **Git** | Ein Repo fuer Monorepo, spaeter ggf. aufteilen |

## Philosophie

> **"Erst verstehen, dann bauen."**

Neue Projekte starten NICHT mit Code, sondern mit Dokumentation:

1. **Vision** - Was wollen wir erreichen?
2. **Requirements** - Was muss das System koennen?
3. **Architektur** - Wie soll es aufgebaut sein?
4. **Roadmap** - In welcher Reihenfolge bauen wir?
5. **Implementierung** - Jetzt erst Code!

## Rules by Category

### Initialisierung

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [monorepo-structure](rules/monorepo-structure.md) | CRITICAL | Basis-Projektstruktur mit docs/ (inkl. entwicklung/ + systemdokumentation/) |

### Requirements Engineering

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [requirements-engineering](rules/requirements-engineering.md) | CRITICAL | Vision, Stakeholder, User Stories, NFRs |

### Projektableitung

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [project-derivation](rules/project-derivation.md) | HIGH | Konkrete Projekte aus Requirements ableiten |

### Doku-Lifecycle

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [docs-maintenance](rules/docs-maintenance.md) | CRITICAL | SOLL/IST-Trennung, Feature-Lifecycle, TODO-Tracker, Index-Pattern, Session-Start-Protokoll |

## Workflow-Checkliste

### Phase 1: Initialisierung

- [ ] Monorepo erstellen
- [ ] docs/ mit Astro Starlight initialisieren
- [ ] CLAUDE.md anlegen
- [ ] Git initialisieren

### Phase 2: Requirements Engineering

- [ ] Vision-Statement schreiben
- [ ] Stakeholder identifizieren
- [ ] User Stories erfassen
- [ ] Non-Functional Requirements definieren
- [ ] Constraints dokumentieren

### Phase 3: Architektur

- [ ] System-Kontext-Diagramm erstellen
- [ ] Komponenten identifizieren
- [ ] Technologie-Stack evaluieren
- [ ] Architektur-Entscheidungen (ADRs) dokumentieren

### Phase 4: Roadmap

- [ ] Meilensteine definieren
- [ ] MVP abgrenzen
- [ ] Abhaengigkeiten identifizieren
- [ ] Release-Planung

### Phase 5: Projektableitung

- [ ] Projektstruktur aus Architektur ableiten
- [ ] Frontend-/Backend-Projekte anlegen
- [ ] Build-Konfiguration einrichten
- [ ] CI/CD planen

### Phase 6: Implementierung + Doku-Pflege (laufend)

Details in `rules/docs-maintenance.md`.

- [ ] Pro Stufe einen TODO-Tracker unter `entwicklung/implementierung/{stufe-X}-uebersicht.md`
- [ ] Pro Feature: Spec in `entwicklung/specs/`, Plan in `entwicklung/plans/`
- [ ] Nach Feature-Abschluss: `systemdokumentation/{subsystem}.md` aktualisieren
- [ ] Fortschritts-Tabelle auf `Fertig` setzen, Entscheidungen loggen
- [ ] Build im `docs/` gruen — via Devcontainer (`./dev build`, sonst `devcontainer exec --workspace-folder . sh -c 'npm run build'`), nie nativ `npm` (User-only)

## Wichtige Hinweise

- **Kein Code ohne Requirements** - Erst RE abschliessen
- **Docs leben im Repo** - Keine externen Wikis
- **CLAUDE.md pflegen** - Fuer AI-gestuetzte Entwicklung
- **ADRs schreiben** - Entscheidungen dokumentieren
- **SOLL vs IST konsequent trennen** - `architektur/` = Ziel, `systemdokumentation/` = Stand
- **Claude-Plans gehoeren ins Repo** - unter `entwicklung/plans/`, nicht ephemer im Chat
