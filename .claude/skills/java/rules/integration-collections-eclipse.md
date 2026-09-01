---
title: Eclipse Collections
impact: HIGH
tags: collections, immutable, eclipse-collections, lists, maps, sets
---

# Eclipse Collections

Dieser Skill beschreibt Eclipse Collections - immutable, thread-safe Collections mit fluent API.

### Maven

```xml
<properties>
    <eclipse-collections.version>13.0.0</eclipse-collections.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.eclipse.collections</groupId>
        <artifactId>eclipse-collections-api</artifactId>
        <version>${eclipse-collections.version}</version>
    </dependency>
    <dependency>
        <groupId>org.eclipse.collections</groupId>
        <artifactId>eclipse-collections</artifactId>
        <version>${eclipse-collections.version}</version>
    </dependency>
    <dependency>
        <groupId>com.fasterxml.jackson.datatype</groupId>
        <artifactId>jackson-datatype-eclipse-collections</artifactId>
        <version>${jackson.version}</version>
    </dependency>
</dependencies>
```

---

### Immutable vs Mutable

| Typ | Immutable | Mutable |
|-----|-----------|---------|
| List | `ImmutableList<T>` | `MutableList<T>` |
| Set | `ImmutableSet<T>` | `MutableSet<T>` |
| Map | `ImmutableMap<K,V>` | `MutableMap<K,V>` |

**Regel:** `Immutable*` für Rückgabewerte/Fields, `Mutable*` nur lokal.

---

### Factory Methods

```java
import org.eclipse.collections.api.factory.Lists;
import org.eclipse.collections.api.factory.Sets;
import org.eclipse.collections.api.factory.Maps;

// Leere Collections
ImmutableList<String> emptyList = Lists.immutable.empty();
ImmutableSet<String> emptySet = Sets.immutable.empty();

// Mit Elementen
ImmutableList<String> list = Lists.immutable.of("a", "b", "c");
ImmutableMap<String, Integer> map = Maps.immutable.of("a", 1, "b", 2);

// Aus bestehender Collection
ImmutableList<String> fromList = Lists.immutable.ofAll(existingList);
```

---

### Stream zu ImmutableList

```java
import org.eclipse.collections.impl.collector.Collectors2;

ImmutableList<ProductDto> products = repository.findAll()
    .stream()
    .map(ProductDto::new)
    .collect(Collectors2.toImmutableList());

ImmutableMap<UUID, ProductDto> byId = products.stream()
    .collect(Collectors2.toImmutableMap(ProductDto::id, p -> p));
```

---

### Collection Methoden

```java
ImmutableList<String> list = Lists.immutable.of("a", "b", "c");

// Filtern
ImmutableList<String> filtered = list.select(s -> s.startsWith("a"));
ImmutableList<String> rejected = list.reject(s -> s.isEmpty());

// Transformieren
ImmutableList<Integer> lengths = list.collect(String::length);

// Finden
String first = list.getFirst();
String found = list.detect(s -> s.equals("b"));

// Prüfen
boolean anyMatch = list.anySatisfy(s -> s.length() > 1);
```

---

### Mutable für Transformationen

```java
MutableList<ProductDto> mutableList = Lists.mutable.empty();
for (ProductEntity entity : entities) {
    if (entity.isActive()) {
        mutableList.add(new ProductDto(entity));
    }
}
ImmutableList<ProductDto> result = mutableList.toImmutable();
```

---

### Best Practices

1. **ImmutableList als Standard** - Für alle Rückgabewerte
2. **MutableList nur lokal** - Für Aufbau, dann `toImmutable()`
3. **Collectors2 verwenden** - Für Stream-Integration
4. **Keine null-Collections** - Leere Collections statt null

---

## Checkliste

- [ ] Maven Dependencies hinzugefuegt
- [ ] Jackson-Modul fuer Eclipse Collections registriert
- [ ] ImmutableList fuer Rueckgabewerte
- [ ] Collectors2.toImmutableList() fuer Streams
- [ ] Lists.immutable.empty() statt null
