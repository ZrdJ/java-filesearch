---
title: Import Order
impact: MEDIUM
tags: imports, organization
---

# Import-Reihenfolge

Dieser Skill beschreibt die Konventionen fuer Import-Statements in Java.

---

### Reihenfolge

1. Projekt-eigene Imports (`net.example.*`)
2. Externe Libraries (`org.*`, `com.*`)
3. `javax.*` / `jakarta.*`
4. `java.*`

### Regeln

- Jede Gruppe alphabetisch sortiert
- Leerzeile zwischen Gruppen
- Keine Wildcard-Imports (`*`)
- Static Imports am Anfang (eigene Gruppe)

### Beispiel

```java
package net.example.project.feature.product;

import net.example.project.feature.other.OtherClass;
import net.example.project.common.util.StringUtils;

import org.eclipse.collections.api.list.ImmutableList;
import org.jusecase.inject.Component;

import javax.inject.Inject;

import java.util.Optional;
import java.util.UUID;
```

### EditorConfig-Einstellung

```ini
ij_java_imports_layout = $*, |, *, |, javax.**, |, java.**
ij_java_class_count_to_use_import_on_demand = 999
ij_java_names_count_to_use_import_on_demand = 999
```

---

## Checkliste

- [ ] Projekt-Imports zuerst
- [ ] Externe Libraries danach
- [ ] javax/jakarta vor java
- [ ] Keine Wildcard-Imports
- [ ] Alphabetisch sortiert
