# Requirements Engineering

Dieser Skill definiert den Requirements-Engineering-Prozess fuer neue Projekte.

---

## Uebersicht

Requirements Engineering ist der **erste und wichtigste Schritt** bei jedem neuen Projekt. Ohne klare Requirements gibt es keinen Code.

### RE-Phasen

```
Vision → Stakeholder → User Stories → NFRs → Constraints → Validierung
```

---

## 1. Vision

### Vision-Statement

Ein praegnanter Satz, der das "Warum" des Projekts beschreibt.

**Template:**

```markdown
# Vision

## Elevator Pitch

Fuer {Zielgruppe}
die {Problem/Beduerfnis} haben,
ist {Produktname}
eine {Produktkategorie},
die {Hauptnutzen} bietet.
Anders als {Alternativen}
bietet unser Produkt {Differenzierung}.

## Langfristige Vision

In 3 Jahren wird {Produktname} ...
```

### Geschaeftsziele

| Ziel | Metrik | Zielwert |
|------|--------|----------|
| Beispiel: Kundenzufriedenheit | NPS | > 50 |
| Beispiel: Marktanteil | % | 15% in DACH |

---

## 2. Stakeholder-Analyse

### Stakeholder-Matrix

| Stakeholder | Rolle | Interesse | Einfluss | Beduerfnisse |
|-------------|-------|-----------|----------|--------------|
| Beispiel: Endbenutzer | Primaer | Hoch | Mittel | Einfache Bedienung |
| Beispiel: Admin | Sekundaer | Mittel | Hoch | Verwaltbarkeit |

### Stakeholder-Priorisierung

- **Primaer**: Direkte Nutzer des Systems
- **Sekundaer**: Indirekt betroffen (Admins, Support)
- **Tertiaer**: Externe Stakeholder (Regulatoren, Partner)

---

## 3. User Stories

### Epic-Struktur

```markdown
## Epic: {Epic-Name}

Als {Rolle}
moechte ich {Ziel}
damit {Nutzen}

### User Stories

- [ ] US-001: Als {Rolle} moechte ich {Aktion} damit {Nutzen}
- [ ] US-002: Als {Rolle} moechte ich {Aktion} damit {Nutzen}
```

### User Story Template

```markdown
### US-{ID}: {Kurztitel}

**Als** {Rolle}
**moechte ich** {Aktion/Feature}
**damit** {Nutzen/Wert}

**Akzeptanzkriterien:**
- [ ] Kriterium 1
- [ ] Kriterium 2
- [ ] Kriterium 3

**Prioritaet:** {Must|Should|Could|Won't}
**Abhaengigkeiten:** US-XXX, US-YYY
```

### MoSCoW-Priorisierung

| Prioritaet | Bedeutung | Anteil |
|------------|-----------|--------|
| **Must** | Unverzichtbar fuer MVP | ~60% |
| **Should** | Wichtig, aber nicht kritisch | ~20% |
| **Could** | Nice-to-have | ~15% |
| **Won't** | Nicht in dieser Version | ~5% |

---

## 4. Non-Functional Requirements (NFRs)

### NFR-Kategorien

| Kategorie | Beispiel-Anforderung |
|-----------|---------------------|
| **Performance** | Seitenaufbau < 2 Sekunden |
| **Skalierbarkeit** | 10.000 gleichzeitige Nutzer |
| **Verfuegbarkeit** | 99.9% Uptime |
| **Sicherheit** | OWASP Top 10 Compliance |
| **Wartbarkeit** | Modulare Architektur |
| **Portabilitaet** | Docker-basiertes Deployment |
| **Compliance** | DSGVO-konform |
| **Accessibility** | WCAG 2.1 AA |

### NFR-Template

```markdown
### NFR-{ID}: {Kategorie} - {Kurztitel}

**Anforderung:** {Beschreibung}
**Metrik:** {Messbare Groesse}
**Zielwert:** {Konkreter Wert}
**Testmethode:** {Wie wird verifiziert?}
**Prioritaet:** {Must|Should|Could}
```

---

## 5. Constraints (Einschraenkungen)

### Technische Constraints

| Constraint | Begruendung |
|------------|-------------|
| Java 21+ | LTS-Version, Team-Expertise |
| PostgreSQL | Bestehende Infrastruktur |
| Docker | Container-Deployment |

### Organisatorische Constraints

| Constraint | Begruendung |
|------------|-------------|
| Budget: X EUR | Projektbudget |
| Timeline: 6 Monate | Go-Live-Termin |
| Team: 3 Entwickler | Verfuegbare Ressourcen |

### Regulatorische Constraints

| Constraint | Begruendung |
|------------|-------------|
| DSGVO | EU-Datenschutz |
| BSI Grundschutz | Sicherheitsanforderungen |

---

## 6. Validierung

### Review-Checkliste

- [ ] Alle Stakeholder identifiziert?
- [ ] Vision klar formuliert?
- [ ] User Stories vollstaendig?
- [ ] Akzeptanzkriterien definiert?
- [ ] NFRs messbar?
- [ ] Constraints dokumentiert?
- [ ] Priorisierung abgestimmt?
- [ ] Abhaengigkeiten identifiziert?

### Validierungsmethoden

| Methode | Wann anwenden |
|---------|---------------|
| Review | Nach jedem Artefakt |
| Walkthrough | Bei komplexen Features |
| Prototyping | Bei UI-Anforderungen |
| Stakeholder-Interview | Bei Unklarheiten |

---

## Artefakte-Uebersicht

Nach Abschluss des RE sollten folgende Dokumente existieren:

```
docs/src/content/docs/
├── vision/
│   ├── index.md          # Vision-Statement
│   ├── stakeholder.md    # Stakeholder-Analyse
│   └── ziele.md          # Geschaeftsziele
├── requirements/
│   ├── index.md          # Uebersicht, Priorisierung
│   ├── user-stories.md   # Epics und User Stories
│   ├── nfr.md            # Non-Functional Requirements
│   └── constraints.md    # Einschraenkungen
```

---

## Wann ist RE abgeschlossen?

Requirements Engineering ist abgeschlossen, wenn:

1. **Vision** - Stakeholder haben zugestimmt
2. **User Stories** - MVP ist definiert und priorisiert
3. **NFRs** - Qualitaetsanforderungen sind messbar
4. **Constraints** - Rahmenbedingungen sind dokumentiert
5. **Review** - Alle Artefakte sind validiert

**Erst dann** beginnt die Architektur-Phase!
