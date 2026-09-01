# Projektableitung

Dieser Skill beschreibt, wie aus abgeschlossenen Requirements konkrete Projekte abgeleitet werden.

---

## Voraussetzungen

Bevor Projekte abgeleitet werden, MUESSEN folgende Artefakte existieren:

- [ ] Vision-Statement
- [ ] Stakeholder-Analyse
- [ ] User Stories (priorisiert)
- [ ] Non-Functional Requirements
- [ ] Constraints
- [ ] Architektur-Entscheidungen (ADRs)

**Ohne abgeschlossenes RE keine Projektableitung!**

---

## Ableitungsprozess

```
Requirements → Komponenten → Projekte → Build-Setup
```

### 1. Komponenten identifizieren

Aus den Requirements und der Architektur ergeben sich Komponenten:

| Komponenten-Typ | Indikator | Beispiel |
|-----------------|-----------|----------|
| **Frontend** | UI-Requirements, User Stories mit UI | Web-App, Mobile-App |
| **Backend** | Business-Logik, API-Anforderungen | REST-API, GraphQL |
| **Datenbank** | Persistenz-Anforderungen | PostgreSQL, Redis |
| **Shared** | Geteilte Typen, Validierung | API-Contracts, DTOs |
| **Docs** | Bereits vorhanden | Starlight-Docs |

### 2. Projektstruktur ableiten

```
{projekt}/
├── docs/                      # Existiert bereits
├── {projekt}-backend/         # Wenn Backend-Komponente
├── {projekt}-frontend/        # Wenn Frontend-Komponente
├── {projekt}-shared/          # Wenn geteilte Typen
├── {projekt}-mobile/          # Wenn Mobile-App
├── {projekt}-infra/           # Wenn eigene Infrastruktur
├── CLAUDE.md                  # Aktualisieren!
└── README.md                  # Aktualisieren!
```

---

## Projekt-Templates

### Backend (Java)

```
{projekt}-backend/
├── pom.xml
├── src/
│   └── main/
│       ├── java/
│       │   └── {package}/
│       │       ├── Application.java
│       │       └── feature/
│       └── resources/
│           └── application.properties
└── CLAUDE.md
```

**Referenz:** `/java` Skill fuer Details

### Frontend (Astro + Solid)

```
{projekt}-frontend/
├── package.json
├── astro.config.mjs
├── src/
│   ├── pages/
│   ├── components/
│   │   └── solid/
│   └── layouts/
└── CLAUDE.md
```

### Shared (TypeScript)

```
{projekt}-shared/
├── package.json
├── tsconfig.json
├── src/
│   ├── types/
│   │   └── api.ts
│   └── validation/
│       └── schemas.ts
└── CLAUDE.md
```

---

## CLAUDE.md aktualisieren

Nach Projektableitung CLAUDE.md im Root anpassen:

```markdown
# {Projektname}

## Projekt-Status
- Phase: Implementierung
- Aktuelle Arbeit: MVP Sprint 1

## Struktur
- `docs/` - Projektdokumentation (Astro Starlight)
- `{projekt}-backend/` - Java Backend (Javalin)
- `{projekt}-frontend/` - Web Frontend (Astro + Solid)

## Konventionen
- Backend: siehe `{projekt}-backend/CLAUDE.md`
- Frontend: siehe `{projekt}-frontend/CLAUDE.md`
- Commits: Conventional Commits

## Referenzierte Skills
- `/java` - Backend-Entwicklung
- `/baunach` - Feature-Entwicklung (falls Baunach-Projekt)
```

---

## Technologie-Stack-Entscheidungen

### Backend-Optionen

| Szenario | Empfehlung | Begruendung |
|----------|------------|-------------|
| REST API, Java-Team | Javalin + jOOQ | Leichtgewichtig, produktiv |
| Komplexe Geschaeftslogik | Clean Architecture | Testbarkeit, Wartbarkeit |
| Hohe Last | Virtuelle Threads (Java 21+) | Skalierbarkeit |

### Frontend-Optionen

| Szenario | Empfehlung | Begruendung |
|----------|------------|-------------|
| Content-lastig | Astro | SSG, Performance |
| Interaktive UI | Solid.js | Reaktivitaet, Bundle-Groesse |
| Formulare | Astro + Solid | SSG mit Islands |

### Datenbank-Optionen

| Szenario | Empfehlung | Begruendung |
|----------|------------|-------------|
| Standard OLTP | PostgreSQL | Zuverlaessig, Feature-reich |
| Zeitreihen | TimescaleDB | Hypertables, Kompression |
| Caching | Redis | In-Memory, schnell |

---

## MVP-Abgrenzung

### Was gehoert ins MVP?

- Alle **Must**-User-Stories
- Mindest-NFRs fuer Betrieb
- Keine **Should**/**Could** Features

### MVP-Checkliste

- [ ] Must-Stories identifiziert
- [ ] Technische Mindestanforderungen definiert
- [ ] Deployment-Pipeline geplant
- [ ] Monitoring-Konzept vorhanden
- [ ] Rollback-Strategie definiert

---

## Roadmap-Integration

### Meilenstein-Template

```markdown
## Meilenstein: {Name}

**Ziel:** {Was wird erreicht?}
**Deadline:** {Datum}
**Abhaengigkeiten:** {Vorherige Meilensteine}

### Enthalten
- US-001: {User Story}
- US-002: {User Story}

### Nicht enthalten
- US-010 (Should, naechster Meilenstein)
```

### Typische Meilensteine

| Meilenstein | Inhalt |
|-------------|--------|
| **M1: Fundament** | Projekt-Setup, CI/CD, Basis-Infrastruktur |
| **M2: MVP** | Must-Features, Go-Live-faehig |
| **M3: Enhancement** | Should-Features, UX-Verbesserungen |
| **M4: Scale** | Performance, Skalierung, Monitoring |

---

## Workflow-Checkliste

### Vor Projektableitung

- [ ] RE abgeschlossen und validiert
- [ ] Architektur dokumentiert
- [ ] Technologie-Stack entschieden
- [ ] MVP abgegrenzt

### Projektableitung

- [ ] Komponenten identifiziert
- [ ] Projektstruktur angelegt
- [ ] CLAUDE.md fuer jedes Subprojekt
- [ ] Build-Konfiguration (ohne auszufuehren!)
- [ ] Git-Struktur (Branches, Hooks)

### Nach Projektableitung

- [ ] Root CLAUDE.md aktualisiert
- [ ] README.md aktualisiert
- [ ] Roadmap mit Meilensteinen
- [ ] Erste Tickets/Issues erstellt

---

## Anti-Patterns

| Anti-Pattern | Problem | Loesung |
|--------------|---------|---------|
| "Einfach mal anfangen" | Unklare Requirements | RE zuerst abschliessen |
| Over-Engineering | Zu viele Projekte/Module | YAGNI - nur was benoetigt wird |
| Fehlende Docs | Wissen geht verloren | docs/ als erstes Projekt |
| Zu fruehes Optimieren | Verschwendete Zeit | MVP first, dann optimieren |
