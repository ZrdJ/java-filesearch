---
title: Sqids Short IDs
impact: MEDIUM
tags: sqids, short-ids, url-safe, slugs
---

# Sqids

Dieser Skill beschreibt Sqids - kurze, URL-sichere IDs aus Zahlen.

### Maven

```xml
<properties>
    <sqids.version>0.1.0</sqids.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.sqids</groupId>
        <artifactId>sqids</artifactId>
        <version>${sqids.version}</version>
    </dependency>
</dependencies>
```

---

### Grundlagen

```java
Sqids sqids = Sqids.builder().build();

// Encode: Zahlen -> Short-ID
String id = sqids.encode(Arrays.asList(1L, 2L, 3L)); // "86Rf07"

// Decode: Short-ID -> Zahlen
List<Long> numbers = sqids.decode(id); // [1, 2, 3]

// Einzelne Zahl
String id = sqids.encode(Arrays.asList(12345L)); // "X1fqB"
```

---

### Konfiguration

```java
// Mindestlänge
Sqids sqids = Sqids.builder()
    .minLength(10)
    .build();

// Benutzerdefiniertes Alphabet
Sqids sqids = Sqids.builder()
    .alphabet("FxnXM1kBN6cuhsAvjW3Co7l2RePyY8DwaU04Tzt9fHQrqSVKdpimLGIJOgb5ZE")
    .build();

// Blocklist (Wörter ausschließen)
Sqids sqids = Sqids.builder()
    .blockList(new HashSet<>(Arrays.asList("badword1", "badword2")))
    .build();
```

---

### Use Cases

```java
// UUID-basierte DB-ID -> öffentliche Short-ID
public String toPublicId(long internalId) {
    return sqids.encode(Arrays.asList(internalId));
}

public long fromPublicId(String publicId) {
    List<Long> decoded = sqids.decode(publicId);
    if (decoded.isEmpty()) {
        throw new IllegalArgumentException("Invalid ID");
    }
    return decoded.get(0);
}

// Composite IDs
String id = sqids.encode(Arrays.asList(userId, orderId, timestamp));
```

---

### Best Practices

1. **Nicht für Security** - IDs sind reversibel, nicht für Auth-Tokens
2. **Konsistente Instanz** - Gleiche Sqids-Config für encode/decode
3. **Alphabet shuffeln** - Für App-spezifische IDs
4. **minLength** - Für konsistente URL-Längen

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt
- [ ] Sqids-Instanz konfiguriert
- [ ] Alphabet angepasst (optional)
- [ ] minLength gesetzt (optional)
- [ ] encode/decode Methoden implementiert
