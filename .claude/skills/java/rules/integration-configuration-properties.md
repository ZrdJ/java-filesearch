---
title: Properties Framework
impact: HIGH
tags: configuration, properties, environment, settings
---

# Properties Framework

Dieser Skill beschreibt das Properties Framework - typisiertes Konfigurationsmanagement mit composable Store-Architektur.

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
        <artifactId>java-properties</artifactId>
        <version>0.2.1</version>
    </dependency>
</dependencies>
```

---

### Hauptkomponenten

| Klasse/Interface | Zweck |
|------------------|-------|
| `ApplicationPropertyStore` | Property-Zugriff |
| `ApplicationProperty` | Typisierte Properties |
| `SystemPropertyStore` | JVM System Properties |
| `SystemEnvironmentStore` | Environment Variables |
| `PropertiesFileStore` | `.properties` Dateien |

---

### Property Definition (Enum)

```java
public enum DatabaseProperties implements ApplicationProperty {
    JdbcUrl("database.jdbc.url", false),
    Username("database.username", false),
    Password("database.password", true);

    private final String _key;
    private final boolean _secret;

    DatabaseProperties(final String key, final boolean secret) {
        _key = key;
        _secret = secret;
    }

    @Override
    public String key() { return _key; }

    @Override
    public boolean isSecret() { return _secret; }

    public RuntimeException exception() {
        return new IllegalStateException("Property not configured: " + _key);
    }
}
```

---

### Store Konfiguration

```java
public ApplicationPropertyStore createPropertyStore() {
    // Priorität: Properties File > System Properties > Environment
    return new PropertiesFileStore("application")
        .or(new SystemPropertyStore())
        .or(new SystemEnvironmentStore(
            new ChangeDotToUnderscoreProperty()
        ));
}
```

---

### Property-Zugriff

```java
@Component
public class DatabaseConfig {
    @Inject private ApplicationPropertyStore _store;

    public String jdbcUrl() {
        return _store.get(DatabaseProperties.JdbcUrl)
            .map(ApplicationPropertyValue::asString)
            .orElseThrow(DatabaseProperties.JdbcUrl::exception);
    }

    public int poolSize() {
        return _store.get(DatabaseProperties.PoolSize)
            .map(ApplicationPropertyValue::asInt)
            .orElse(10); // Default
    }
}
```

---

### Best Practices

1. **Enum für Properties** - Typsicherheit
2. **isSecret() Flag** - Verhindert Logging sensibler Werte
3. **Composable Stores** - Flexible Priorität
4. **Exception Helper** - `exception()` Methode im Enum

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt (JitPack)
- [ ] Properties Enum definiert
- [ ] isSecret() fuer sensible Werte
- [ ] Store-Kette konfiguriert
- [ ] application.properties angelegt
