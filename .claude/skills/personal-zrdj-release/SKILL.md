---
name: jitpack-release
description: JitPack-basierte Releases fuer Open-Source Java-Projekte. GitHub Release triggert automatisch JitPack Build und README Update.
# GENERIERT aus personal/skills-ref/personal-zrdj-release/ — nicht hier editieren, Aenderungen gehoeren in die Referenz.
source: personal-provider-ref
ref-hash: sha256:50c8f08a869c653f5fb7eef238fca43f7d0c3fb6a646757199ae3ce95da42c1e
---

# JitPack Release

Automatisierte Releases fuer Java-Bibliotheken via JitPack.

## Quick Reference

| Thema | Konvention |
|-------|------------|
| **Package Registry** | JitPack (`com.github.{owner}`) |
| **Trigger** | GitHub Release (published) |
| **Versionierung** | SemVer ohne `v`-Praefix (z.B. `0.5.0`) |
| **Automatisierung** | `release.yml` Workflow |

## Rules by Category

### Workflow

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [release-workflow](rules/release-workflow.md) | HIGH | GitHub Actions fuer JitPack |
| [release-erstellen](rules/release-erstellen.md) | HIGH | Release-Prozess Schritt fuer Schritt |

### Konfiguration

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [jitpack-config](rules/jitpack-config.md) | MEDIUM | jitpack.yml und pom.xml |
| [dependency-einbindung](rules/dependency-einbindung.md) | LOW | Nutzung als Maven-Dependency |

## Workflow-Checkliste

### Release erstellen

- [ ] Version in `pom.xml` erhoehen
- [ ] Aenderungen committen und pushen
- [ ] GitHub Release erstellen (Tag = Version ohne `v`)
- [ ] Warten auf `release.yml` Workflow (JitPack Build + README Update)
- [ ] JitPack Build-Status pruefen: `https://jitpack.io/#Owner/Repo`

### Neues Projekt fuer JitPack einrichten

- [ ] `release.yml` Workflow erstellen
- [ ] README mit JitPack Badge und Dependency-Beispiel
- [ ] Ersten Release erstellen

## Wichtige Hinweise

- **Kein Token noetig** - JitPack baut oeffentliche Repos ohne Authentifizierung
- **Erster Abruf langsam** - JitPack baut erst bei erstem Request, daher Workflow vorab triggern
- **Tag = Version** - Kein `v`-Praefix, direkt `0.5.0`
