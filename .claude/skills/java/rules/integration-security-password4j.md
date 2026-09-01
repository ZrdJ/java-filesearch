---
title: Password4j Hashing
impact: HIGH
tags: password, hashing, argon2, bcrypt, scrypt, security
---

# Password4j

Dieser Skill beschreibt Password4j - sichere Passwort-Hashing-Bibliothek mit Argon2, BCrypt, SCrypt, PBKDF2.

### Maven

```xml
<properties>
    <password4j.version>1.8.4</password4j.version>
</properties>

<dependencies>
    <dependency>
        <groupId>com.password4j</groupId>
        <artifactId>password4j</artifactId>
        <version>${password4j.version}</version>
    </dependency>
</dependencies>
```

---

### Unterstützte Algorithmen

| Algorithmus | Empfehlung |
|-------------|------------|
| **Argon2** | Bevorzugt für neue Projekte |
| **BCrypt** | Bewährter Standard |
| **SCrypt** | Memory-hard Alternative |
| **PBKDF2** | Legacy-Kompatibilität |

---

### Password Hashen

```java
// Mit Argon2 (empfohlen)
Hash hash = Password.hash("myPassword")
    .addSalt()
    .addPepper()
    .withArgon2();

String hashString = hash.getResult();

// Mit BCrypt
Hash hash = Password.hash("myPassword")
    .addSalt()
    .withBcrypt();
```

---

### Password Verifizieren

```java
// Salt ist im Hash enthalten
boolean valid = Password.check("userInput", storedHash)
    .addPepper()
    .withArgon2();

// Mit explizitem Salt
boolean valid = Password.check("userInput", storedHash)
    .addSalt(storedSalt)
    .addPepper()
    .withPbkdf2();
```

---

### Konfiguration (psw4j.properties)

```properties
# Argon2
hash.argon2.memory=65536
hash.argon2.iterations=3
hash.argon2.length=32
hash.argon2.parallelism=4
hash.argon2.type=id

# BCrypt
hash.bcrypt.minor=b
hash.bcrypt.rounds=12

# Global Pepper
global.pepper=<secret-pepper-value>
```

---

### SystemChecker für optimale Parameter

```java
// Finde optimale Argon2-Parameter für 500ms
Argon2Function optimal = SystemChecker.findArgon2Parameters(
    500,          // max Zeit in ms
    65536,        // memory in KB
    4             // parallelism
);
```

---

### Best Practices

1. **Argon2id** - Bevorzugter Algorithmus
2. **Pepper extern speichern** - Config/Environment, nicht DB
3. **Salt automatisch** - Argon2/BCrypt generieren Salt
4. **Parameter anpassen** - `SystemChecker` nutzen

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt
- [ ] Algorithmus gewaehlt (Argon2 empfohlen)
- [ ] Pepper in Config/Environment
- [ ] psw4j.properties konfiguriert
- [ ] Hash-Methode implementiert
- [ ] Verify-Methode implementiert
