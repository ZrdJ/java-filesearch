---
title: Primitives Framework
impact: MEDIUM
tags: bytes, text, hashing, codecs, encoding, crypto
---

# Primitives Framework

Dieser Skill beschreibt das Primitives Framework - erweiterte Primitive-Typen fuer Bytes, Text, Hashing und Encoding.

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
        <artifactId>java-primitives</artifactId>
        <version>0.3.1</version>
    </dependency>
</dependencies>
```

---

### Bytes

```java
// Erstellen
Bytes bytes = Bytes.of("Hello World");
Bytes bytes = Bytes.of(new byte[]{1, 2, 3});

// Zurück zu String
String text = bytes.asString();

// Größe
ByteSize size = bytes.size();
BigDecimal mb = size.megabytes();

// Encoding
Bytes encoded = bytes.encode(Codecs.Base64);
Bytes decoded = encoded.decode(Codecs.Base64);

// Hashing
Bytes hashed = bytes.hash(HashAlgorithms.SHA_256);

// AES Verschlüsselung
Bytes encrypted = bytes.encryptAES(key, salt);
Bytes decrypted = encrypted.decryptAES(key, salt);

// Sicher löschen
key.destroy();
```

---

### Text

```java
// Case-insensitive (Standard)
Text text = Text.caseInsensitive("Hello");
text.contains("HELLO"); // true

// Null-Safety
text.isNull();
text.isAbsent();  // null oder leer
text.isPresent(); // nicht null und nicht leer

String value = text.orElse("default");
```

---

### Codecs

| Codec | Verwendung |
|-------|------------|
| `Codecs.Base64` | Standard Base64 |
| `Codecs.Base64Url` | URL-sichere Base64 |
| `Codecs.Hex` | Hexadezimal |

---

### Hash-Algorithmen

| Algorithmus | Enum |
|-------------|------|
| SHA-256 | `HashAlgorithms.SHA_256` |
| SHA-512 | `HashAlgorithms.SHA_512` |
| SHA3-256 | `HashAlgorithms.SHA3_256` |

---

### Exception Handling

```java
// Checked als RuntimeException
Exceptions.rethrow(
    () -> Files.readString(path),
    e -> new RuntimeException("Read failed", e)
);

// Mit Fallback
String content = Exceptions.fallbackFunction(
    () -> Files.readString(path),
    e -> "default"
);
```

---

### Best Practices

1. **Bytes.destroy()** - Sensible Daten überschreiben
2. **Text für Null-Safety** - Statt String
3. **SHA-256+** - Keine MD5/SHA für Security

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt (JitPack)
- [ ] Bytes fuer Binaerdaten
- [ ] Text fuer Null-Safety
- [ ] Codecs fuer Encoding
- [ ] destroy() fuer sensible Daten
