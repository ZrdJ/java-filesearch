---
title: AWS DynamoDB
impact: LOW
tags: dynamodb, aws, nosql, database
---

# AWS DynamoDB Enhanced Client

Dieser Skill beschreibt den DynamoDB Enhanced Client fuer NoSQL-Datenmodellierung.

### Maven

```xml
<properties>
    <aws-sdk.version>2.29.42</aws-sdk.version>
</properties>

<dependencies>
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>dynamodb</artifactId>
        <version>${aws-sdk.version}</version>
    </dependency>
    <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>dynamodb-enhanced</artifactId>
        <version>${aws-sdk.version}</version>
    </dependency>
</dependencies>
```

---

### Client Setup

```java
@Component
public class DynamoDbClientProvider implements Provider<DynamoDbEnhancedClient> {
    @Inject private ApplicationPropertyStore _store;

    @Override
    public DynamoDbEnhancedClient get() {
        final var dynamoDbClient = DynamoDbClient.builder()
            .region(Region.of("eu-central-1"))
            .credentialsProvider(DefaultCredentialsProvider.create())
            .build();

        return DynamoDbEnhancedClient.builder()
            .dynamoDbClient(dynamoDbClient)
            .build();
    }
}
```

---

### Table Schema Definition

```java
@DynamoDbBean
public class ProductEntity {
    private String pk;
    private String sk;
    private String productId;
    private String name;

    @DynamoDbPartitionKey
    @DynamoDbAttribute("PK")
    public String getPk() { return pk; }

    @DynamoDbSortKey
    @DynamoDbAttribute("SK")
    public String getSk() { return sk; }
}
```

---

### CRUD Operationen

```java
// Create
product.setPk("PRODUCT#" + product.getProductId());
product.setSk("METADATA");
_table.putItem(product);

// Read
final var key = Key.builder()
    .partitionValue("PRODUCT#" + productId)
    .sortValue("METADATA")
    .build();
return Optional.ofNullable(_table.getItem(key));

// Update
_table.updateItem(product);

// Delete
_table.deleteItem(key);
```

---

### Query

```java
final var queryCondition = QueryConditional
    .keyEqualTo(Key.builder()
        .partitionValue("CATEGORY#" + categoryId)
        .build());

return _table.query(queryCondition)
    .items()
    .stream()
    .toList();
```

---

### Single-Table Design

```
PK                | SK              | Daten
------------------|-----------------|------------------
PRODUCT#123       | METADATA        | Name, Preis
PRODUCT#123       | CATEGORY#456    | Kategorie-Zuordnung
CATEGORY#456      | METADATA        | Kategorie-Name
```

---

### Best Practices

1. **Single-Table Design** - Alle Entitäten in einer Tabelle
2. **Composite Keys** - PK/SK für flexible Abfragen
3. **Enhanced Client** - Type-Safety mit @DynamoDbBean

---

## Checkliste

- [ ] Maven Dependencies hinzugefuegt
- [ ] DynamoDB Client konfiguriert
- [ ] Entity mit @DynamoDbBean
- [ ] PK/SK definiert
- [ ] Single-Table Design geplant
- [ ] CRUD-Operationen implementiert
