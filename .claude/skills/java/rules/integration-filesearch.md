---
title: Filesearch Framework
impact: LOW
tags: filesearch, files, filesystem, search
---

# Filesearch Framework

Dieser Skill beschreibt das Filesearch Framework - Fluent-API fuer Dateisystem-Suche mit Stream-Integration.

### Maven

```xml
<repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>

<dependencies>
    <dependency>
        <groupId>com.github.zrdj</groupId>
        <artifactId>java-filesearch</artifactId>
        <version>0.4.1</version>
    </dependency>
</dependencies>
```

---

### Import

```java
import static com.github.zrdj.java.filesearch.Search.search;
```

---

### Fluent Builder API

| Methode | Zweck |
|---------|-------|
| `search()` | Einstiegspunkt |
| `.directory(String)` | Zielverzeichnis |
| `.recursively()` | Rekursive Suche |
| `.notRecursively()` | Nur im Verzeichnis |
| `.byPath()` | Gibt `Path` zurück |
| `.byFile()` | Gibt `File` zurück |
| `.stream()` | Stream für Verarbeitung |

---

### Beispiele

```java
// Nicht-rekursiv
final List<Path> executables = search()
    .directory("/search/path")
    .notRecursively()
    .byPath()
    .stream()
    .filter(p -> p.getFileName().toString().endsWith(".exe"))
    .collect(Collectors.toList());

// Rekursiv
final List<Path> allJsonFiles = search()
    .directory("/project/root")
    .recursively()
    .byPath()
    .stream()
    .filter(p -> p.toString().endsWith(".json"))
    .collect(Collectors.toList());

// Große Dateien finden
final List<File> largeFiles = search()
    .directory("/data")
    .recursively()
    .byFile()
    .stream()
    .filter(f -> f.length() > 1024 * 1024) // > 1MB
    .collect(Collectors.toList());
```

---

### Best Practices

1. **Statischer Import** - `Search.search()`
2. **Path vs File** - `byPath()` bevorzugen
3. **Rekursion bewusst wählen** - Kann langsam sein

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt (JitPack)
- [ ] Statischer Import konfiguriert
- [ ] Directory festgelegt
- [ ] Rekursion beachtet
- [ ] Stream-Filter angewendet
