# Monorepo-Struktur

Dieser Skill definiert die Basis-Projektstruktur fuer neue Entwicklungsprojekte.

---

## Basis-Struktur

```
{projekt}/
├── docs/                          # Astro Starlight Dokumentation
│   ├── src/
│   │   └── content/
│   │       └── docs/
│   │           ├── index.mdx
│   │           ├── vision/              # Warum bauen wir das?
│   │           ├── requirements/        # Was muss das System koennen?
│   │           ├── architektur/         # SOLL — wie soll es aufgebaut sein?
│   │           ├── roadmap/             # Stufenplan — was, in welcher Reihenfolge?
│   │           ├── entwicklung/         # Arbeitsartefakte (Specs, Plans, Tracker)
│   │           │   ├── specs/           # Design Specs vor Implementierung
│   │           │   ├── plans/           # Implementation Plans vor Implementierung
│   │           │   └── implementierung/ # Fortschritts-Tracker + Entscheidungs-Logs
│   │           └── systemdokumentation/ # IST — was ist tatsaechlich gebaut?
│   ├── astro.config.mjs
│   └── package.json
├── CLAUDE.md                      # AI-Kontext fuer Claude Code
├── README.md                      # Projekt-Uebersicht
└── .gitignore
```

**Kerntrennung:** `architektur/` = SOLL, `systemdokumentation/` = IST, `roadmap/` = Reihenfolge, `entwicklung/` = Arbeit daran. Siehe `docs-maintenance.md` fuer Lifecycle-Regeln.

---

## Astro Starlight Setup

### Initialisierung

```bash
npm create astro@latest docs -- --template starlight
```

### Konfiguration (astro.config.mjs)

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: '{Projektname}',
      defaultLocale: 'de',
      locales: {
        de: { label: 'Deutsch' },
      },
      sidebar: [
        { label: 'Uebersicht', link: '/' },
        { label: 'Vision', autogenerate: { directory: 'vision' } },
        { label: 'Requirements', autogenerate: { directory: 'requirements' } },
        { label: 'Architektur (SOLL)', autogenerate: { directory: 'architektur' } },
        { label: 'Roadmap', autogenerate: { directory: 'roadmap' } },
        { label: 'Systemdokumentation (IST)', autogenerate: { directory: 'systemdokumentation' } },
        { label: 'Entwicklung', autogenerate: { directory: 'entwicklung' } },
      ],
    }),
  ],
});
```

---

## CLAUDE.md Template

```markdown
# {Projektname}

## Projekt-Status
- Phase: Requirements Engineering
- Aktuelle Arbeit: Vision definieren
- TODO-Tracker: `docs/src/content/docs/entwicklung/implementierung/{stufe-X}-uebersicht.md` (sobald Implementierung laeuft)

## Struktur
- `docs/` - Projektdokumentation (Astro Starlight) — **einzige Wahrheit**

## Dokumentations-Pflicht
- Architektur-Entscheidungen (SOLL): `docs/src/content/docs/architektur/`
- Ist-Zustand des Systems (IST): `docs/src/content/docs/systemdokumentation/`
- Design Specs (vor Implementierung): `docs/src/content/docs/entwicklung/specs/`
- Implementation Plans (vor Implementierung): `docs/src/content/docs/entwicklung/plans/`
- Fortschritt + Entscheidungs-Logs: `docs/src/content/docs/entwicklung/implementierung/`
- Abweichungen VOR der Implementierung abstimmen und dokumentieren
- Keine eigenmaechtigen Architektur-Entscheidungen

## Konventionen
- Dokumentation: Deutsch, keine Umlaute in Dateinamen
- Commits: PascalCase-Praefixe (`Add:`, `Fix:`, `Update:`, `Refactor:`, `Remove:`, `Docs:`, `Test:`, `Chore:`) — siehe `/git` Skill → `commit-konventionen.md`

## Naechste Schritte
1. Vision-Statement fertigstellen
2. Stakeholder identifizieren
3. User Stories erfassen
```

---

## Docs-Ordner-Struktur

### vision/

| Datei | Inhalt |
|-------|--------|
| `index.md` | Vision-Statement, Elevator Pitch |
| `stakeholder.md` | Stakeholder-Analyse |
| `ziele.md` | Geschaeftsziele, Erfolgskriterien |

### requirements/

| Datei | Inhalt |
|-------|--------|
| `index.md` | Uebersicht, Priorisierung |
| `user-stories.md` | Epics und User Stories |
| `nfr.md` | Non-Functional Requirements |
| `constraints.md` | Technische und organisatorische Einschraenkungen |

### architektur/

| Datei | Inhalt |
|-------|--------|
| `index.md` | System-Ueberblick |
| `kontext.md` | System-Kontext-Diagramm |
| `komponenten.md` | Komponenten-Diagramm |
| `technologie-stack.md` | Technologie-Entscheidungen |
| `adr/` | Architecture Decision Records |

### roadmap/

| Datei | Inhalt |
|-------|--------|
| `index.md` | Stufenplan — Stufen/Meilensteine mit Feature-Checklisten |

Eine Seite reicht meist. Jede Stufe ist ein verkaufbares/ausrollbares Produkt-Increment mit Ziel, Zielgruppe und Feature-Checkliste.

### entwicklung/

Arbeitsartefakte rund um Features. Hier landen **alle Claude-Plans und Design-Entscheidungen** vor der Implementierung.

| Pfad | Inhalt |
|------|--------|
| `index.md` | Uebersicht ueber Specs / Plans / Implementierung |
| `specs/index.md` | Chronologische Liste aller Design Specs |
| `specs/{YYYY-MM-DD}-{feature}-design.md` | Technisches Design vor Implementierung |
| `plans/index.md` | Chronologische Liste aller Implementation Plans |
| `plans/{YYYY-MM-DD}-{feature}.md` | Schritt-fuer-Schritt Plan mit Aufgaben |
| `implementierung/index.md` | Uebersicht pro Stufe/Milestone |
| `implementierung/{stufe-1}-uebersicht.md` | **TODO-Tracker** — Entscheidungs-Log + Feature-Fortschritt |

### systemdokumentation/

IST-Zustand des laufenden Systems. Keine Plaene, keine Specs — nur was **tatsaechlich** gebaut ist.

| Datei | Inhalt |
|-------|--------|
| `index.md` | Uebersicht ueber dokumentierte Teilsysteme |
| `{subsystem}.md` | Pro Feature/Teilsystem eine Seite (Flow, Datenmodell, API, Code-Struktur) |

Wird nach jedem Feature-Abschluss aktualisiert. Siehe `docs-maintenance.md`.

---

## Spaetere Erweiterung

Nach Abschluss des Requirements Engineerings wird die Struktur erweitert:

```
{projekt}/
├── docs/                    # Bereits vorhanden
├── {projekt}-backend/       # Backend-Projekt
├── {projekt}-frontend/      # Frontend-Projekt
├── {projekt}-shared/        # Geteilter Code (optional)
├── CLAUDE.md
└── README.md
```

---

## Naming-Konventionen

| Element | Konvention | Beispiel |
|---------|------------|----------|
| Projekt-Root | kebab-case | `mein-projekt` |
| Subprojekte | `{projekt}-{typ}` | `mein-projekt-backend` |
| Docs-Dateien | kebab-case, keine Umlaute | `user-stories.md` |
| Ordner | kebab-case | `architektur/` |

---

## Git-Initialisierung

```bash
# Repo erstellen
git init
git add .
git commit -m "Docs: Initiales Projekt-Setup"

# Branch-Strategie
git branch develop
git checkout develop
```

### .gitignore Template

```gitignore
# Dependencies
node_modules/

# Build
dist/
.astro/

# IDE
.idea/
.vscode/
*.iml

# OS
.DS_Store
Thumbs.db

# Env
.env
.env.local
```

---

## Workflow-Checkliste

- [ ] Projekt-Verzeichnis erstellen
- [ ] docs/ mit Starlight initialisieren
- [ ] CLAUDE.md anlegen (inkl. Verweis auf Dokumentations-Pflicht)
- [ ] README.md schreiben
- [ ] .gitignore konfigurieren
- [ ] Git initialisieren
- [ ] Docs-Struktur anlegen: `vision/`, `requirements/`, `architektur/`, `roadmap/`, `entwicklung/{specs,plans,implementierung}/`, `systemdokumentation/`
- [ ] Jeder Bereich hat `index.md` mit Tabellen-Overview (siehe `markdown` Skill → Page-Level-Index-Pattern)
- [ ] Build zur Verifikation: `npm run build` im `docs/`-Ordner
