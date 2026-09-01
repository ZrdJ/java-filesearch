---
title: Clean Architecture mit JUseCase
impact: CRITICAL
tags: architecture, usecase, clean-architecture, business-logic, dto, auditing, versioned
---

# Clean Architecture

Dieser Skill beschreibt die UseCase-basierte Clean Architecture mit JUseCase Framework.

### Maven

```xml
<dependency>
    <groupId>org.jusecase</groupId>
    <artifactId>jusecase</artifactId>
    <version>1.3.0</version>
</dependency>
```

---

### Architektur-Übersicht

```
HTTP Layer (Javalin)
       ↓ Request
UseCase Layer (Business Logic)
       ↓ Repository Interface
Domain Layer (Interfaces, DTOs)
       ↓ Implementation
Persistence Layer (jOOQ)
```

---

### UseCase-Typen

| Typ | Auth | Request-Basis |
|-----|------|---------------|
| `PublicUsecase` | Keine | `RequestWithPublicContext` |
| `AuthenticatedUsecase` | Eingeloggt (rollenunabhaengig) | `RequestWithAuthenticatedContext` |
| `CustomerUsecase` | Kunde + allowedRoles() | `RequestWithCustomerContext` |
| `AdministrationUsecase` | Agency + allowedRoles() | `RequestWithAdministrationContext` |

---

### UseCase Beispiel

```java
@Component
public class GetProductsUsecase
    implements CustomerUsecase<GetProductsUsecase.Request, GetProductsUsecase.Response> {

    public static class Request extends RequestWithCustomerContext {
        public final Optional<UUID> categoryId;
        public Request(Optional<UUID> categoryId) {
            this.categoryId = categoryId;
        }
    }

    public record Response(ImmutableList<ProductDto> products) {}

    @Inject private ProductRepository _productRepository;

    @Override
    public Set<Role> allowedRoles() {
        return Set.of(Role.TENANT_ADMIN, Role.TENANT_MEMBER);
    }

    @Override
    public Response execute(Request request) {
        final var accountId = request.context().account().id();
        return new Response(_productRepository.findAll(accountId));
    }
}
```

---

### DTO Hierarchie (Versioned / Audited)

DTOs werden nach Operationstyp getrennt:

| Operation | Basisklasse | Felder | Beispiel |
|-----------|-------------|--------|----------|
| **Read** | `Audited` | id, version, createdAt/By, updatedAt/By + business | `AccountDto` |
| **Update** | `Versioned` | id, version + mutable business (Optimistic Locking) | `AccountUpdateDto` |
| **Create** | keine | nur business (kein id, kein version) | `AccountCreateDto` |

**Jackson-Kompatibilitaet:** Alle DTO-Klassen brauchen `@JsonIgnoreProperties(ignoreUnknown = true)` und einen public No-Args-Konstruktor fuer Deserialisierung. Konstruktoren die jOOQ Records annehmen muessen ebenfalls public sein.

```java
// Versioned — Basis fuer Update-DTOs
@JsonIgnoreProperties(ignoreUnknown = true)
public class Versioned {
    public UUID id;
    public long version;

    public Versioned(final org.jooq.Record record) {
        this.id = record.get("id", UUID.class);
        this.version = record.get("row_version", Long.class);
    }
    public Versioned() {}
}

// Audited — Basis fuer Read-DTOs
@JsonIgnoreProperties(ignoreUnknown = true)
public class Audited extends Versioned {
    public final Instant createdAt;
    public final Instant updatedAt;
    public final String createdBy;
    public final String updatedBy;

    public Audited(final org.jooq.Record record) {
        super(record);
        this.createdAt = record.get("created_at", OffsetDateTime.class).toInstant();
        this.updatedAt = record.get("updated_at", OffsetDateTime.class).toInstant();
        this.createdBy = record.get("created_by", String.class);
        this.updatedBy = record.get("updated_by", String.class);
    }
}
```

---

### Read-DTO (extends Audited)

```java
@JsonIgnoreProperties(ignoreUnknown = true)
public class AccountDto extends Audited {
    public final String email;
    public final String displayName;
    public final String role;

    public AccountDto(final org.jooq.Record record) {
        super(record);
        this.email = record.get("email", String.class);
        this.displayName = record.get("display_name", String.class);
        this.role = record.get("role", Object.class).toString();
    }

    public AccountDto() {
        super();
        this.email = null;
        this.displayName = null;
        this.role = null;
    }
}
```

Konstruktion: `_dsl.selectFrom(ACCOUNTS).fetch().stream().map(AccountDto::new)`

---

### Zod Base-Schemas (Frontend)

```typescript
// src/types/schemas.ts
export const versionedSchema = z.object({
    id: z.string(),
    version: z.number(),
});

export const auditedSchema = versionedSchema.extend({
    createdAt: z.string(),
    updatedAt: z.string(),
    createdBy: z.string(),
    updatedBy: z.string(),
});

// Feature-DTOs erben via .extend()
const accountSchema = auditedSchema.extend({
    email: z.string(),
    displayName: z.string(),
    role: z.string(),
});
```

---

### HTTP Integration

```java
router.get("/api/products", ctx -> {
    final var response = _usecases.execute(
        new GetProductsUsecase.Request(Optional.empty()),
        new WebSession(ctx));
    ctx.json(response);
});
```

---

### Fehlertypen

```java
public class BadRequest extends UsecaseError {}     // 400
public class Unauthorized extends UsecaseError {}   // 401
public class Forbidden extends UsecaseError {}      // 403
public class NotFound extends UsecaseError {}       // 404
```

---

### Naming

| Element | Pattern | Beispiel |
|---------|---------|----------|
| UseCase | `[Context][Operation]Usecase` | `WebsiteAccountLoginUsecase` |
| Request | Innere Klasse | `extends RequestWith*Context` |
| Response | Innerer Record | `record Response(...)` |
| Read-DTO | `[Entity]Dto` | `AccountDto extends Audited` |
| Update-DTO | `[Entity]UpdateDto` | `AccountUpdateDto extends Versioned` |
| Create-DTO | `[Entity]CreateDto` | `AccountCreateDto` (keine Basisklasse) |

---

## Checkliste

- [ ] UseCase-Typ gewaehlt (Public/Authenticated/Customer/Administration)
- [ ] Request-Klasse mit korrektem Context
- [ ] Response als Record, DTOs mit korrekter Basisklasse
- [ ] Read-DTOs erben von Audited
- [ ] Update-DTOs erben von Versioned
- [ ] Create-DTOs ohne Basisklasse
- [ ] Frontend: Zod-Schema erbt von auditedSchema/versionedSchema
- [ ] Dependencies injiziert
- [ ] UseCase in BusinessLogic registriert
- [ ] HTTP Endpoint erstellt
- [ ] Fehlerbehandlung implementiert
