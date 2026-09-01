---
title: Jackson JSON Serialization
impact: HIGH
tags: json, jackson, serialization, dto, records
---

# Jackson JSON

Dieser Skill beschreibt die ObjectMapper Konfiguration fuer JSON Serialisierung mit Jackson.

### Maven

```xml
<properties>
    <jackson.version>2.21.1</jackson.version>
    <jackson-annotation.version>2.21</jackson-annotation.version>
</properties>

<dependencies>
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>${jackson.version}</version>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.datatype</groupId>
        <artifactId>jackson-datatype-jdk8</artifactId>
        <version>${jackson.version}</version>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.datatype</groupId>
        <artifactId>jackson-datatype-jsr310</artifactId>
        <version>${jackson.version}</version>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.datatype</groupId>
        <artifactId>jackson-datatype-eclipse-collections</artifactId>
        <version>${jackson.version}</version>
    </dependency>
</dependencies>
```

---

### Architektur: JsonPlugin Interface + JacksonJsonPlugin

**PFLICHT:** Der ObjectMapper wird NIEMALS direkt in Services oder UseCases instanziiert. Stattdessen gibt es ein zentrales `JsonPlugin` Interface und eine `JacksonJsonPlugin` Implementierung, die per DI injiziert wird.

#### JsonPlugin Interface (im Framework-Package)

```java
public interface JsonPlugin {
    ObjectMapper getObjectMapper();
}
```

Das Interface definiert den Vertrag fuer JSON-Zugriff im gesamten Projekt. Es lebt im Framework-Package, damit Core-Klassen darauf zugreifen koennen ohne eine Abhaengigkeit auf die konkrete Jackson-Implementierung zu haben.

#### JacksonJsonPlugin (in Infrastructure/Config)

```java
public final class JacksonJsonPlugin implements JsonPlugin, JsonMapper {
    private final JavalinJackson _javalinJson = new JavalinJackson();

    public JacksonJsonPlugin() {
        final ObjectMapper mapper = _javalinJson.getMapper();
        mapper
            .registerModule(new ParameterNamesModule(JsonCreator.Mode.PROPERTIES))
            .registerModule(new Jdk8Module())
            .registerModule(new JavaTimeModule())
            .configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false)
            .setVisibility(PropertyAccessor.FIELD, JsonAutoDetect.Visibility.ANY)
            .setVisibility(PropertyAccessor.SETTER, JsonAutoDetect.Visibility.NONE)
            .setVisibility(PropertyAccessor.GETTER, JsonAutoDetect.Visibility.NONE)
            .setVisibility(PropertyAccessor.IS_GETTER, JsonAutoDetect.Visibility.NONE)
            .configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false)
            .enable(JsonGenerator.Feature.WRITE_BIGDECIMAL_AS_PLAIN);
    }

    @Override
    public ObjectMapper getObjectMapper() {
        return _javalinJson.getMapper();
    }

    // Delegiert alle JsonMapper-Methoden an JavalinJackson
    @Override
    public <T> T fromJsonStream(InputStream json, Type targetType) {
        return _javalinJson.fromJsonStream(json, targetType);
    }
    // ... weitere JsonMapper-Methoden
}
```

Die Klasse implementiert **zwei Interfaces:**
- `JsonPlugin` — fuer den Zugriff auf den ObjectMapper aus Services/UseCases
- `JsonMapper` (Javalin) — damit Javalin den gleichen Mapper fuer HTTP Request/Response nutzt

#### Registrierung in Application

```java
injector.add(new JacksonJsonPlugin());
```

#### Nutzung in Services/UseCases

```java
@Component
public class SomeService {
    @Inject
    private JacksonJsonPlugin _json;

    public void doSomething(String rawJson) {
        var node = _json.getObjectMapper().readTree(rawJson);
    }
}
```

---

### Anti-Pattern

- **NIEMALS** `new ObjectMapper()` in Services, UseCases oder Pollern
- **IMMER** `@Inject JacksonJsonPlugin` und `getObjectMapper()` verwenden
- Der zentrale ObjectMapper hat die korrekte Konfiguration (Module, Visibility, Datum-Format)
- Ein eigener `new ObjectMapper()` hat KEINE Module registriert und deshalb falsches Verhalten bei Dates, Optional, etc.

---

| Option | Wert | Beschreibung |
|--------|------|--------------|
| `FAIL_ON_EMPTY_BEANS` | false | Leere Objekte erlauben |
| `WRITE_DATES_AS_TIMESTAMPS` | false | ISO-8601 Format |
| Field Visibility | ANY | Alle Fields serialisieren |
| Getter Visibility | NONE | Getter ignorieren |

---

### Annotations

```java
// Property Mapping
public record ProductDto(
    @JsonProperty("product_id") UUID productId,
    @JsonProperty("product_name") String name
) {}

// Unbekannte Properties ignorieren (für externe APIs)
@JsonIgnoreProperties(ignoreUnknown = true)
public record ExternalApiResponse(
    @JsonProperty("data") List<Item> data
) {}

// Properties ausschließen
public record UserDto(
    UUID id,
    @JsonIgnore String passwordHash
) {}

// Bedingte Serialisierung
@JsonInclude(JsonInclude.Include.NON_NULL)
public record ProductDto(
    UUID id,
    String description  // Nur wenn nicht null
) {}
```

---

### Records vs Klassen

**Records (Standard):**
```java
@JsonIgnoreProperties(ignoreUnknown = true)
public record ProductPriceDto(
    @JsonProperty("price") BigDecimal price,
    @JsonProperty("rebate") BigDecimal rebate
) {}
```

**Klassen (nur bei DI-Injection):**
```java
@Component
public final class ProductImageDto {
    @JsonProperty("id") public final UUID id;
    @JsonProperty("url") public final String url;

    @Inject @JsonIgnore
    private StorageService _storageService;

    public ProductImageDto(ProductImageRecord record) {
        this.id = record.getId();
        this.url = _storageService.createPublicUrl(record);
    }
}
```

---

### SubType Vererbung (Polymorphe DTOs)

```java
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = PaymentSuccess.class, name = "success"),
    @JsonSubTypes.Type(value = PaymentFailure.class, name = "failure")
})
public abstract sealed class PaymentResult
    permits PaymentSuccess, PaymentFailure {}

public final class PaymentSuccess extends PaymentResult {
    @JsonProperty("transactionId") public String transactionId;
}

// Switch Statement
switch (result) {
    case PaymentSuccess s -> handleSuccess(s);
    case PaymentFailure f -> handleFailure(f);
}
```

---

### Java Time Support

```java
// Automatisch mit JavaTimeModule
public record EventDto(
    LocalDate date,           // "2024-01-15"
    Instant instant,          // "2024-01-15T13:30:00Z"
    Duration duration         // "PT2H30M"
) {}
```

**Empfehlung:** Für APIs immer `Instant` verwenden (UTC, keine Zeitzonenprobleme).

---

### Best Practices

1. **JsonPlugin Interface + JacksonJsonPlugin** — Zentraler Zugriffspunkt per DI
2. **Niemals `new ObjectMapper()`** — Immer das injizierte Plugin verwenden
3. **Module registrieren** — Jdk8, JavaTime, ParameterNames, EclipseCollections
4. **Field-basierte Visibility** — Keine Getter/Setter noetig
5. **@JsonProperty** fuer alle Felder — Schutz vor Code-Renaming
6. **@JsonIgnoreProperties(ignoreUnknown = true)** — Fuer externe APIs
7. **Records** als Standard, Klassen nur bei DI
8. **Instant** fuer Timestamps in APIs

---

## Checkliste

- [ ] Maven Dependencies hinzugefuegt
- [ ] JsonPlugin Interface im Framework-Package erstellt
- [ ] JacksonJsonPlugin implementiert (JsonPlugin + Javalin JsonMapper)
- [ ] JacksonJsonPlugin per `injector.add()` registriert
- [ ] Javalin nutzt JacksonJsonPlugin als `jsonMapper()`
- [ ] Module registriert (Jdk8, JavaTime, ParameterNames, EclipseCollections)
- [ ] Field Visibility auf ANY gesetzt
- [ ] Kein `new ObjectMapper()` in Geschaeftslogik
- [ ] @JsonProperty fuer API-Felder
- [ ] @JsonIgnore fuer interne Felder
