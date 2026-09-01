---
title: Naming Conventions
impact: HIGH
tags: naming, classes, interfaces, methods, variables, packages
---

# Naming Conventions

Dieser Skill definiert die Namenskonventionen fuer Java-Klassen, Interfaces, Methoden und Variablen.

---

### Interfaces

- **PascalCase**, kein `I`-Prefix
- Abstrakte Implementierungen: `Abstract*`-Prefix erlaubt

```java
public interface ProductRepository {
    Optional<Product> findById(final UUID id);
}
```

### Klassen & Records

- **PascalCase**, Suffix nach Rolle: `*Dto`, `*Repository`, `*Service`
- Kein `Impl`-Suffix für Implementierungen
- Innere Klassen: immer `static`, oben in der Datei platzieren
- `sealed` Klassen für geschlossene Hierarchien

```java
public class ProductService {
    private final ProductRepository _productRepository;
}
```

### Methoden

- **camelCase** mit Verb-Prefix
- Prefixe: `find*`, `create*`, `update*`, `delete*`, `is*`, `has*`
- Keine `get`/`set`-Prefixe

```java
public Optional<Product> findProductById(final UUID id) {
    return _productRepository.findById(id);
}
```

### Variablen

- **camelCase** für lokale Variablen
- **_underscorePrefix** für private Felder
- `final` bevorzugen

```java
public class Example {
    private final ProductRepository _productRepository;

    public void process() {
        final var products = _productRepository.findAll();
    }
}
```

### Konstanten

- **UPPER_SNAKE_CASE**

```java
private static final int MAX_RETRY_COUNT = 3;
public static final String DEFAULT_LOCALE = "de";
```

### Enums

- Enum-Klasse: **PascalCase**
- Enum-Werte: **PascalCase** (nicht UPPER_SNAKE_CASE)
- PostgreSQL-Enums: **snake_case lowercase** (`customer`, `service_provider`)

```java
public enum OrderStatus {
    Pending,
    Processing,
    Shipped,
    Delivered,
    Cancelled
}

public enum PaymentMethod {
    CreditCard,
    PayPal,
    BankTransfer,
    Invoice
}
```

**Verwendung im Switch:**
```java
return switch (status) {
    case Pending -> "Ausstehend";
    case Processing -> "In Bearbeitung";
    case Shipped, Delivered -> "Unterwegs";
    case Cancelled -> "Storniert";
};
```

### Domain-Enums (Wrapping jOOQ-Enums)

Fuer jedes PostgreSQL-Enum wird ein **Domain-Enum** erstellt, das das jOOQ-generierte Enum wrappt und um zusaetzliche Informationen ergaenzt (z.B. Translation-Keys). Das Domain-Enum ist das Enum das in DTOs und an der API verwendet wird — nie das jOOQ-Enum direkt.

```java
import org.jooq.generated.bis.baunach_crm.enums.OrganisationType;

public enum CrmOrganisationType {
    Customer(OrganisationType.customer, "crm.organisation.type.customer"),
    Supplier(OrganisationType.supplier, "crm.organisation.type.supplier"),
    ServiceProvider(OrganisationType.service_provider, "crm.organisation.type.service_provider");

    private final OrganisationType jooqType;
    private final String translationKey;

    CrmOrganisationType(OrganisationType jooqType, String translationKey) {
        this.jooqType = jooqType;
        this.translationKey = translationKey;
    }

    public OrganisationType jooq() { return jooqType; }
    public String translationKey() { return translationKey; }

    public static CrmOrganisationType fromDatabase(OrganisationType db) {
        for (var value : values()) {
            if (value.jooqType == db) return value;
        }
        throw new IllegalArgumentException("Unknown: " + db);
    }
}
```

**Konventionen:**
- Domain-Enum referenziert jOOQ-Enum direkt im Konstruktor
- `jooq()` Methode fuer Konvertierung Domain → DB
- `fromDatabase()` statische Methode fuer DB → Domain
- Translation-Key folgt dem Muster `{bereich}.{entitaet}.{feld}.{wert}`

### Packages

- **lowercase**, keine Unterstriche

```
net.example.project.product.usecase
```

---

## Checkliste

- [ ] Klassen/Records: PascalCase mit Suffix (*Dto, *Repository, etc.)
- [ ] Interfaces: PascalCase ohne I-Prefix
- [ ] Methoden: camelCase mit Verb-Prefix
- [ ] Private Felder: _underscorePrefix
- [ ] Konstanten: UPPER_SNAKE_CASE
- [ ] Enums: PascalCase (Klasse und Werte)
- [ ] Packages: lowercase
