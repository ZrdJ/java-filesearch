---
title: PostgreSQL mit jOOQ, Flyway, HikariCP
impact: CRITICAL
tags: database, postgresql, jooq, flyway, hikaricp, auditing, migrations
---

# PostgreSQL Integration

Dieser Skill beschreibt die Datenbank-Integration mit jOOQ (Type-Safe Queries), Flyway (Migrations) und HikariCP (Connection Pool).

### Maven Konfiguration

```xml
<properties>
    <jooq.version>3.20.11</jooq.version>
    <flyway.version>12.0.2</flyway.version>
    <hikari.version>7.0.2</hikari.version>
    <postgres.version>42.7.10</postgres.version>
</properties>

<dependencies>
    <!-- jOOQ -->
    <dependency>
        <groupId>org.jooq</groupId>
        <artifactId>jooq</artifactId>
        <version>${jooq.version}</version>
    </dependency>
    <dependency>
        <groupId>org.jooq</groupId>
        <artifactId>jooq-postgres-extensions</artifactId>
        <version>${jooq.version}</version>
    </dependency>
    <dependency>
        <groupId>org.jooq</groupId>
        <artifactId>jooq-jackson-extensions</artifactId>
        <version>${jooq.version}</version>
    </dependency>

    <!-- Flyway -->
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-core</artifactId>
        <version>${flyway.version}</version>
    </dependency>
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-database-postgresql</artifactId>
        <version>${flyway.version}</version>
    </dependency>

    <!-- HikariCP -->
    <dependency>
        <groupId>com.zaxxer</groupId>
        <artifactId>HikariCP</artifactId>
        <version>${hikari.version}</version>
    </dependency>

    <!-- PostgreSQL Driver -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <version>${postgres.version}</version>
    </dependency>
</dependencies>
```

---

### HikariCP + jOOQ Setup

```java
public class ApplicationDatabaseProvider implements Provider<ApplicationDatabase> {
    private final String _jdbc;
    private final String _user;
    private final String _password;

    public ApplicationDatabaseProvider(String jdbc, String user, String password) {
        _jdbc = jdbc;
        _user = user;
        _password = password;
    }

    @Override
    public ApplicationDatabase get() {
        final var config = new HikariConfig();
        config.setJdbcUrl(_jdbc);
        config.setUsername(_user);
        config.setPassword(_password);
        config.addDataSourceProperty("cachePrepStmts", "true");
        config.addDataSourceProperty("prepStmtCacheSize", "250");

        return new ApplicationDatabase(
            DSL.using(
                new HikariDataSource(config),
                SQLDialect.POSTGRES,
                new Settings().withExecuteWithOptimisticLocking(true)
            )
        );
    }
}

public class ApplicationDatabase {
    private final DSLContext _dsl;

    public ApplicationDatabase(DSLContext dsl) { _dsl = dsl; }
    public DSLContext dsl() { return _dsl; }
    public UUID generateId() { return Identifiers.UUIDv7(); }
}
```

---

### Flyway Migrations

**Verzeichnis:** `src/main/resources/database/migration/`

**Naming:** `V{Major}_{Minor}__{description}.sql`
- `V1_0__init.sql`
- `V1_1__add_users_table.sql`

```java
public void migrateDatabase(PersistenceProperties props) {
    Flyway.configure()
        .locations("classpath:database/migration")
        .dataSource(props.jdbc(), props.user(), props.password())
        .load()
        .migrate();
}
```

---

### jOOQ Code Generation

```bash
mvn clean install -Pdatabase-migration -DskipTests
```

**Tabellen-Referenz-Klasse:**
```java
public class ApplicationTables {
    public static final ProductTable tableProduct = ProductTable.PRODUCT;
    public static final CategoryTable tableCategory = CategoryTable.CATEGORY;
}
```

---

### jOOQ Query Beispiele

```java
// SELECT
_database.dsl()
    .selectFrom(ApplicationTables.tableProduct)
    .where(ApplicationTables.tableProduct.ID.eq(productId))
    .fetchOptional()

// INSERT
final var record = _database.dsl().newRecord(Tables.PRODUCT);
record.setId(_database.generateId());
record.setName(name);
record.store();

// UPDATE
_database.dsl()
    .update(Tables.PRODUCT)
    .set(Tables.PRODUCT.NAME, newName)
    .where(Tables.PRODUCT.ID.eq(productId))
    .execute();

// DELETE
_database.dsl()
    .deleteFrom(Tables.PRODUCT)
    .where(Tables.PRODUCT.ID.eq(productId))
    .execute();

// Transaction
_database.dsl().transaction(trx -> {
    // Alle Operationen in einer Transaktion
    trx.dsl().selectFrom(...).fetchOptional();
});
```

---

### Auditing & Historisierung

**Audit-Spalten für jede Tabelle:**
```sql
CREATE TABLE schema.table_name (
    id uuid PRIMARY KEY,
    created_at timestamptz NOT NULL DEFAULT NOW(),
    updated_at timestamptz,
    created_by VARCHAR(100),
    updated_by VARCHAR(100),
    row_version bigint NOT NULL DEFAULT 0,
    row_period tstzrange NOT NULL DEFAULT tstzrange(now(), null),
    -- weitere Spalten
);

SELECT create_base_triggers('schema.table_name');
```

**CustomConnectionProvider für User-Tracking:**
```java
@Component
public class ApplicationCustomConnectionProvider implements ConnectionProvider {
    public static final ThreadLocal<String> CURRENT_USER_ID = new ThreadLocal<>();

    public static void setAccount(UUID accountId) {
        CURRENT_USER_ID.set("account::" + accountId);
    }

    public static void setEmployee(UUID employeeId) {
        CURRENT_USER_ID.set("employee::" + employeeId);
    }

    @Override
    public Connection acquire() {
        final var conn = _delegate.acquire();
        final var userId = CURRENT_USER_ID.get();
        try (Statement stmt = conn.createStatement()) {
            stmt.execute(userId == null
                ? "RESET app.current_user_id"
                : "SET app.current_user_id = '" + userId + "'");
        }
        return conn;
    }
}
```

---

### Best Practices

1. **HikariCP** für Connection Pooling
2. **Flyway** für versionierte Migrations
3. **jOOQ Code Generation** für Type-Safety
4. **Optimistic Locking** via `row_version`
5. **UUIDv7** für sortierbare IDs
6. **KEIN JSONB** — Alle strukturierten Daten werden in eigenen Tabellen/Spalten modelliert, niemals JSONB-Spalten verwenden

### jOOQ Enum Wrapper

Fuer jOOQ-generierte Datenbank-Enums IMMER eigene Wrapper-Enums im Projekt anlegen. Die generierten jOOQ-Enums (`org.jooq.generated.*`) niemals direkt in DTOs oder der Geschaeftslogik verwenden — stattdessen auf String mappen (via `.getLiteral()` / `.name()`) oder eigene Domain-Enums definieren.

---

## Checkliste

- [ ] Maven Dependencies hinzugefuegt
- [ ] HikariCP + jOOQ Setup erstellt
- [ ] Flyway Migrations-Verzeichnis angelegt
- [ ] Erste Migration erstellt
- [ ] jOOQ Codegen ausgefuehrt (User macht selbst)
- [ ] ApplicationTables Klasse erstellt
- [ ] Audit-Spalten in Tabellen
- [ ] `create_base_triggers` aufgerufen
