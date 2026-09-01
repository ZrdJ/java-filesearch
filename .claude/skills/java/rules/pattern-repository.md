---
title: Repository Pattern
impact: HIGH
tags: repository, data-access, domain, database
---

# Repository Pattern

Dieser Skill beschreibt das Repository Pattern - Interface im Domain Layer, Implementierung im Database Layer.

### Verzeichnisstruktur

```
feature/{domain}/
  ├── domain/
  │   └── ProductRepository.java        (Interface)
  ├── database/
  │   └── ProductRepositoryJooq.java    (Implementierung)
  └── api/
      └── ProductDto.java               (DTOs)
```

---

### Interface (Domain Layer)

```java
package net.example.feature.product.domain;

public interface ProductRepository {
    ImmutableList<ProductDto> findAll();
    ImmutableList<ProductDto> findByCategory(UUID categoryId);
    Optional<ProductDto> findById(UUID productId);
    UUID create(ProductCreateDto product);
    void update(ProductUpdateDto product);
    void delete(UUID productId);
}
```

---

### Implementierung (Database Layer)

Naming: `{Name}Repository{Technology}` (z.B. `ProductRepositoryJooq`)

```java
@Component
public class ProductRepositoryJooq implements ProductRepository {
    @Inject private ApplicationDatabase _database;

    @Override
    public ImmutableList<ProductDto> findAll() {
        return _database.dsl()
            .selectFrom(ApplicationTables.tableProduct)
            .fetch()
            .stream()
            .map(ProductDto::new)
            .collect(Collectors2.toImmutableList());
    }

    @Override
    public Optional<ProductDto> findById(UUID productId) {
        return _database.dsl()
            .selectFrom(ApplicationTables.tableProduct)
            .where(ApplicationTables.tableProduct.ID.eq(productId))
            .fetchOptional()
            .map(ProductDto::new);
    }

    @Override
    public UUID create(ProductCreateDto product) {
        final var record = _database.dsl().newRecord(Tables.PRODUCT);
        record.setId(_database.generateId());
        record.setName(product.name());
        record.store();
        return record.getId();
    }
}
```

---

### Methoden-Naming

| Präfix | Rückgabe | Beispiel |
|--------|----------|----------|
| `findAll*` | `ImmutableList<Dto>` | `findAllActive()` |
| `findBy*` | `ImmutableList<Dto>` | `findByCategory(id)` |
| `findById` | `Optional<Dto>` | `findById(id)` |
| `create*` | `UUID` | `create(dto)` |
| `update*` | `void` | `update(dto)` |
| `delete*` | `void` | `delete(id)` |
| `exists*` | `boolean` | `existsById(id)` |

---

### Best Practices

1. **Interface im Domain Layer** - Keine DB-Details
2. **DTOs aus api/ Package** - Niemals DB-Records nach außen
3. **ImmutableList** - Thread-Sicherheit
4. **Optional** - Keine null-Rückgaben

---

## Checkliste

- [ ] Interface in domain/ Package
- [ ] Implementierung in database/ Package
- [ ] Naming: {Name}Repository{Technology}
- [ ] DTOs aus api/ Package zurueckgeben
- [ ] ImmutableList fuer Listen
- [ ] Optional fuer einzelne Entitaeten
- [ ] Repository in Injector registriert
