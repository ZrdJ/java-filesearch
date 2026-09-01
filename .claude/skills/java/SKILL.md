---
name: java
description: Umfassende Java-Entwicklungsrichtlinien für Backend-Projekte. Enthält Konventionen, Integrationen (PostgreSQL, Javalin, Jackson, Log4j2), Patterns (Clean Architecture, Repository) und Build-Konfiguration (Maven). Triggers auf Java-Code, REST APIs, Datenbank, jOOQ, Flyway, DTOs, Records, Logging, Properties, Identifiers, Security.
# GENERIERT aus personal/skills-ref/java/ — nicht hier editieren; Aenderungen gehoeren nach ~/.claude/skills-ref/java/.
source: personal-provider-ref
ref-hash: sha256:8a4c909743dc64a6c65624290ae533a0c33027f19ad593362f2e0606491304d9
---

# Java Development Guide

Vollständige Entwicklungsrichtlinien für Java-Backend-Projekte.

## Quick Reference

| Thema | Konvention |
|-------|------------|
| **Klassen/Records** | PascalCase, Suffix: `*Dto`, `*Repository`, `*Service` |
| **Methoden** | camelCase, Prefix: `find*`, `create*`, `update*`, `delete*` |
| **Private Felder** | `_underscorePrefix` |
| **Null-Handling** | `Optional<T>` statt null |
| **Collections** | Eclipse Collections (immutable) |
| **JSON** | Jackson mit Field-Visibility |
| **Database** | jOOQ + Flyway + HikariCP |
| **HTTP Server** | Javalin |
| **Logging** | Log4j2 + SLF4J (JSON) |
| **IDs** | UUIDv7 |
| **Build** | Maven Multi-Module |

## Rules by Priority

### Conventions (Immer anwenden)

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [convention-naming](rules/convention-naming.md) | HIGH | Klassen, Interfaces, Methoden, Variablen |
| [convention-dtos](rules/convention-dtos.md) | HIGH | Records, Klassen-DTOs, Sealed Classes |
| [convention-null-handling](rules/convention-null-handling.md) | HIGH | Optional, var, final |
| [convention-formatting](rules/convention-formatting.md) | MEDIUM | Einrückung, Klammern, Leerzeilen |
| [convention-imports](rules/convention-imports.md) | MEDIUM | Import-Reihenfolge |

### Integrations (Bei Bedarf)

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [integration-database-postgres](rules/integration-database-postgres.md) | CRITICAL | jOOQ, Flyway, HikariCP, Auditing |
| [integration-http-server-javalin](rules/integration-http-server-javalin.md) | CRITICAL | REST Endpoints, Exception Handler |
| [integration-json-jackson](rules/integration-json-jackson.md) | HIGH | ObjectMapper, Annotations, SubTypes |
| [integration-logging-log4j2](rules/integration-logging-log4j2.md) | HIGH | Structured JSON Logging, MDC |
| [integration-collections-eclipse](rules/integration-collections-eclipse.md) | HIGH | ImmutableList, ImmutableMap |
| [integration-identifiers](rules/integration-identifiers.md) | HIGH | UUIDv7, ULID, Codecs |
| [integration-configuration-properties](rules/integration-configuration-properties.md) | MEDIUM | Typisierte Properties |
| [integration-http-client-retrofit](rules/integration-http-client-retrofit.md) | MEDIUM | REST Client mit OkHttp |
| [integration-dependency-injection](rules/integration-dependency-injection.md) | MEDIUM | JUseCase Inject, AspectJ |
| [integration-security-password4j](rules/integration-security-password4j.md) | MEDIUM | Argon2, BCrypt Hashing |
| [integration-security-password-policy](rules/integration-security-password-policy.md) | MEDIUM | Passay Validierung |
| [integration-sqids](rules/integration-sqids.md) | LOW | Kurze URL-sichere IDs |
| [integration-primitives](rules/integration-primitives.md) | LOW | Bytes, Hashing, Codecs |
| [integration-filesearch](rules/integration-filesearch.md) | LOW | Dateisystem-Suche |
| [integration-useragent-parser](rules/integration-useragent-parser.md) | LOW | Browser/OS Erkennung |
| [integration-ip-geolocation](rules/integration-ip-geolocation.md) | LOW | MaxMind GeoLite2 |
| [integration-database-dynamodb](rules/integration-database-dynamodb.md) | LOW | AWS DynamoDB |

### Patterns (Architektur)

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [pattern-clean-architecture](rules/pattern-clean-architecture.md) | CRITICAL | UseCases, Domain Layer |
| [pattern-repository](rules/pattern-repository.md) | HIGH | Interface + jOOQ Implementierung |

### Build (Projekt-Setup)

| Rule | Impact | Beschreibung |
|------|--------|--------------|
| [build-maven-multimodule](rules/build-maven-multimodule.md) | HIGH | Parent POM, Module |
| [build-maven](rules/build-maven.md) | MEDIUM | Single-Module Setup |
| [build-bootstrap-rest-api](rules/build-bootstrap-rest-api.md) | MEDIUM | REST API Grundgerüst |

## Workflow-Checkliste

### Neues Projekt

- [ ] Maven-Struktur anlegen (Single oder Multi-Module)
- [ ] `.editorconfig` aus Template kopieren
- [ ] Dependencies in pom.xml eintragen
- [ ] log4j2.xml konfigurieren
- [ ] application.properties anlegen

### Neue Klasse

- [ ] Package-Struktur beachten (feature/{domain}/...)
- [ ] Naming-Konventionen einhalten
- [ ] `final` und `var` verwenden
- [ ] `Optional<T>` statt null
- [ ] Private Felder mit `_underscorePrefix`

### Neues Feature

- [ ] UseCase mit korrektem Interface anlegen
- [ ] DTO im api-Package erstellen
- [ ] Repository-Interface definieren
- [ ] jOOQ-Implementierung schreiben
- [ ] Javalin Route registrieren

## Wichtige Hinweise

- **Build zur Verifikation** - immer ueber den Devcontainer: `./dev compile`/`./dev verify` (Baunach), sonst `devcontainer exec --workspace-folder . sh -c 'mvn clean verify'`. **Nie nativ `mvn`/`./mvnw`** — das ist User-only (siehe `~/.claude/CLAUDE.md` → Verbote, [[build]])
- **Sandbox deaktivieren** - der Build-Befehl (`./dev` bzw. `devcontainer exec`) immer mit `dangerouslyDisableSandbox: true` ausfuehren (Netzwerkzugriff auf Maven Central, JitPack etc. noetig)
- **DTOs aus api-Package** - Niemals Repository-Records direkt zurueckgeben
- **Eclipse Collections** - Immer immutable Collections verwenden
- **UUIDv7** - Fuer alle neuen IDs verwenden

## References (Templates)

| Template | Beschreibung |
|----------|--------------|
| [usecase-template.java](references/usecase-template.java) | UseCase mit Request/Response |
| [repository-template.java](references/repository-template.java) | Interface + jOOQ-Implementierung |
| [dto-template.java](references/dto-template.java) | Record DTO mit jOOQ-Konstruktor |

## Ressourcen

- [editorconfig.template](editorconfig.template) - IDE-Konfiguration
