---
title: Identifiers Framework
impact: MEDIUM
tags: uuid, uuidv7, ulid, ksuid, tsid, identifiers
---

# Identifiers Framework

Dieser Skill beschreibt das Identifiers Framework - einheitliche API fuer UUID, UUIDv7, ULID, KSUID, TSID mit Codec-Support.

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
        <artifactId>java-identifiers</artifactId>
        <version>0.2.1</version>
    </dependency>
</dependencies>
```

---

### Unterstützte ID-Typen

| Typ | Methode | Beschreibung |
|-----|---------|--------------|
| **UUIDv7** | `Identifiers.UUIDv7()` | Zeitbasiert, sortierbar (empfohlen) |
| **UUID** | `Identifiers.UUID()` | Standard UUIDv4 |
| **ULID** | `Identifiers.ULID()` | Lexicographically Sortable |
| **KSUID** | `Identifiers.KSUID()` | K-Sortable Unique Identifier |
| **TSID** | `Identifiers.TSID()` | Time-Sorted Unique Identifier |

---

### ID Generierung

```java
import static com.github.zrdj.java.identifiers.Identifiers.*;

// UUIDv7 - Empfohlen für Datenbank-IDs
UUID id = UUIDv7();

// Standard UUID (v4)
UUID randomId = UUID();

// ULID
ULID ulid = ULID();
```

---

### Codecs für Enkodierung

```java
import static com.github.zrdj.java.identifiers.Codecs.*;

final UUID id = Identifiers.UUIDv7();
final Codec<UUID> base32 = UUIDBase32();

String encoded = base32.encode(id);
UUID decoded = base32.decode(encoded);
```

---

### Verwendung in Datenbank-Kontext

```java
public class ApplicationDatabase {
    private final DSLContext _dsl;

    public UUID generateId() {
        return Identifiers.UUIDv7();
    }
}
```

---

### Best Practices

1. **UUIDv7 für Datenbank-PKs** - Zeitbasiert, sortierbar, bessere Index-Performance
2. **Statischer Import** - `Identifiers.*` für sauberen Code
3. **Codecs für URLs** - Base32 für URL-sichere Darstellung

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt (JitPack)
- [ ] UUIDv7 fuer neue Datenbank-IDs
- [ ] Statischer Import konfiguriert
- [ ] Codec fuer URL-Darstellung (optional)
