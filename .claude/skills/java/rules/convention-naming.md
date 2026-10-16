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
- **_underscorePrefix** nur für `private`/`protected` Felder, die ausschliesslich aus der eigenen Klassenhierarchie gelesen werden — als `_feld`, nie als `objekt._feld`
- Ein Feld, das direkt über ein Objekt gelesen wird (`objekt.feld`), ist `public` und trägt keinen Underscore
- Auch der Zugriff über eine andere Instanz derselben Klasse (z.B. `other.id` in `equals`) zählt als Zugriff über ein Objekt
- `final` bevorzugen

```java
public class Order {
    public final OrderId id;             // wird von aussen gelesen: order.id
    protected final Money _total;        // nur Order und Unterklassen: _total
    private final List<Line> _lines;     // nur Order selbst: _lines

    public boolean equals(final Object o) {
        return o instanceof final Order other && id.equals(other.id);   // other._id waere falsch
    }
}

// anderswo
final var orderId = order.id;            // richtig
final var total = order._total;          // falsch: Underscore-Feld ueber ein Objekt
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

    private final OrganisationType _jooqType;
    private final String _translationKey;

    CrmOrganisationType(final OrganisationType jooqType, final String translationKey) {
        _jooqType = jooqType;
        _translationKey = translationKey;
    }

    public OrganisationType jooq() { return _jooqType; }
    public String translationKey() { return _translationKey; }

    public static CrmOrganisationType fromDatabase(final OrganisationType db) {
        for (final var value : values()) {
            if (value.jooq() == db) return value;
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
- [ ] Underscore nur bei private/protected Feldern, die ausschliesslich aus der eigenen Klassenhierarchie gelesen werden; Zugriff ueber ein Objekt nur auf public-Felder ohne Underscore
- [ ] Konstanten: UPPER_SNAKE_CASE
- [ ] Enums: PascalCase (Klasse und Werte)
- [ ] Packages: lowercase
