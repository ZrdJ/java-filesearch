---
title: Code Formatting
impact: MEDIUM
tags: formatting, indentation, braces, whitespace, iteration, loops
---

# Code Formatting

Dieser Skill beschreibt die Code-Formatierungskonventionen fuer Java.

---

### Einrückung

- **4 Spaces**, keine Tabs
- Continuation Indent: **8 Spaces**

### Records

Parameter auf eigenen Zeilen bei mehr als 2 Parametern:

```java
// Kurz - eine Zeile
public record Point(int x, int y) { }

// Lang - mehrzeilig (> 2 Parameter)
public record ProductDto(
        UUID id,
        long version,
        String name,
        Optional<String> description
) { }
```

### Klammern

- Opening Brace auf gleicher Zeile
- Closing Brace auf eigener Zeile

```java
public class Example {
    public void method() {
        if (condition) {
            // ...
        } else {
            // ...
        }
    }
}
```

### Leerzeilen

- 1 Leerzeile nach Package-Deklaration
- 1 Leerzeile zwischen Import-Gruppen
- 1 Leerzeile zwischen Methoden
- Keine Leerzeile nach öffnender Klammer

### Zeilenlänge

- **Max 120 Zeichen** pro Zeile
- Bei Überschreitung: Umbruch mit Continuation Indent (8 Spaces)

### Method Chaining

Punkt am Zeilenanfang bei mehrzeiligen Chains:

```java
// Kurz - eine Zeile
final var result = list.select(p -> p.isActive()).collect();

// Lang - mehrzeilig
final var products = _database.dsl()
        .selectFrom(Tables.PRODUCT)
        .where(Tables.PRODUCT.CATEGORY_ID.eq(categoryId))
        .and(Tables.PRODUCT.IS_ACTIVE.isTrue())
        .orderBy(Tables.PRODUCT.NAME.asc())
        .fetch()
        .stream()
        .map(ProductDto::new)
        .collect(Collectors2.toImmutableList());
```

### Iteration

IMMER `for` / `for-each` Schleifen verwenden. NIEMALS `.forEach()` Helper-Methoden (weder `Iterable.forEach()` noch `Stream.forEach()`).

```java
// RICHTIG - for-each
for (final var product : products) {
    process(product);
}

// RICHTIG - klassisches for-i
for (int i = 0; i < products.size(); i++) {
    process(products.get(i));
}

// FALSCH - .forEach() Helper
products.forEach(p -> process(p));
products.forEach(this::process);
products.stream().forEach(p -> process(p));
```

### Lambdas

```java
// Einzeilig bei kurzen Expressions
list.select(p -> p.isActive());

// Method Reference wenn möglich
list.collect(ProductDto::new);
```

### EditorConfig

Für vollständige IDE-Konfiguration siehe [editorconfig.template](../editorconfig.template).

---

## Checkliste

- [ ] 4 Spaces Einrueckung
- [ ] Max 120 Zeichen pro Zeile
- [ ] Records mehrzeilig bei > 2 Parametern
- [ ] Method Chaining mit Punkt am Zeilenanfang
- [ ] Iteration mit for/for-each, kein .forEach()
- [ ] EditorConfig konfiguriert
