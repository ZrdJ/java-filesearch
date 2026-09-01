---
title: Null-Handling & Type Safety
impact: HIGH
tags: optional, null, var, final, types
---

# Null-Handling & Type Safety

Dieser Skill beschreibt den Umgang mit Null-Werten und Type Safety in Java.

---

### Optional statt null

Niemals `null` zurückgeben, immer `Optional<T>`:

```java
// Richtig
public Optional<Product> findById(UUID id) {
    return Optional.ofNullable(result);
}

// Falsch - kann null sein!
public Product findById(UUID id) {
    return result;
}
```

### Optional-Verwendung

```java
// Wert extrahieren
final var product = findById(id).orElseThrow(() -> new NotFound("Product"));

// Mit Default
final var name = findName().orElse("Unknown");

// Mapping
final var price = findProduct(id)
    .map(Product::price)
    .orElse(BigDecimal.ZERO);

// Conditional
findProduct(id).ifPresent(this::process);
```

### var für lokale Variablen

`final var` wenn Typ aus rechter Seite klar ersichtlich:

```java
// Gut - Typ klar
final var products = _repository.findAll();
final var name = "example";
final var id = UUID.randomUUID();

// Besser explizit - Typ unklar
ImmutableList<Product> result = process(input);
```

### final bevorzugen

- `final` für alle Parameter
- `final var` für unveränderliche lokale Variablen
- `final` für Felder wenn möglich

```java
public Response execute(final Request request) {
    final var products = _repository.findAll();
    final var filtered = products.select(p -> p.isActive());
    return new Response(filtered);
}
```

### Nullable Parameter

Wenn ein Parameter optional ist, `Optional<T>` als Parametertyp verwenden:

```java
public void updateProduct(
        final UUID id,
        final String name,
        final Optional<String> description
) {
    // description kann leer sein
}
```

### Parameter-Validierung

`Objects.requireNonNull()` für Pflicht-Parameter in Konstruktoren und öffentlichen Methoden:

```java
public class ProductService {
    private final ProductRepository _productRepository;

    public ProductService(final ProductRepository productRepository) {
        _productRepository = Objects.requireNonNull(productRepository, "productRepository");
    }

    public void process(final UUID productId, final String name) {
        Objects.requireNonNull(productId, "productId");
        Objects.requireNonNull(name, "name");
        // ...
    }
}
```

**Wann verwenden:**
- Konstruktor-Parameter (immer)
- Öffentliche API-Methoden
- Nicht bei privaten Methoden (dort ist Caller verantwortlich)

---

## Checkliste

- [ ] `Optional<T>` statt null zurueckgeben
- [ ] `final var` fuer lokale Variablen
- [ ] `final` fuer Parameter
- [ ] `Optional<T>` fuer optionale Parameter
- [ ] `Objects.requireNonNull()` in Konstruktoren
