---
title: DTO Conventions
impact: HIGH
tags: dto, record, sealed, serialization
---

# DTO Conventions

Dieser Skill beschreibt DTOs (Data Transfer Objects) - serialisierbare Datenklassen fuer Schnittstellen.

### Grundregeln

- Suffix `*Dto` fuer alle DTOs
- **Records als Standard** fuer einfache DTOs
- **Klassen mit Vererbung** fuer DTOs mit Audit/Version-Feldern (siehe Versioned/Audited Pattern)
- Serialisierung auf Feldebene konfigurieren (nicht Getter/Setter)
- Keine Geschaeftslogik in DTOs
- **Zeitstempel immer als `Instant`** — nie `OffsetDateTime` in DTOs. jOOQ liefert `OffsetDateTime`, daher beim Lesen `.toInstant()` und beim Schreiben `.atOffset(ZoneOffset.UTC)` konvertieren

### Record DTOs (Standard)

```java
public record ProductPriceDto(
        BigDecimal basePrice,
        BigDecimal finalPrice,
        Optional<ProductPriceRebateDto> rebate
) {}
```

### Klassen DTOs mit Vererbung (Versioned/Audited Pattern)

Fuer Entitaeten mit Audit-Feldern und Optimistic Locking werden Klassen statt Records verwendet, um Vererbung fuer die gemeinsamen Felder nutzen zu koennen.

#### Vererbungshierarchie

```
              Versioned
              ├── id: UUID
              └── version: long
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
    Audited                *UpdateDto
    ├── createdAt           (id + version fuer
    ├── updatedAt            Optimistic Locking,
    ├── createdBy            alle fachlichen Felder
    └── updatedBy            vollstaendig)
        │
        ▼
    *Dto (Response)
```

#### Versioned (Basis fuer Update-DTOs)

```java
public class Versioned {
    public UUID id;
    public long version;

    // Fuer Response-DTOs (aus jOOQ Record)
    protected Versioned(org.jooq.Record record) {
        this.id = record.get("id", UUID.class);
        this.version = record.get("row_version", Long.class);
    }

    // Fuer Request-DTOs (Jackson Deserialisierung)
    protected Versioned() {}
}
```

#### Audited (Basis fuer Response-DTOs)

```java
public class Audited extends Versioned {
    public final Instant createdAt;
    public final Instant updatedAt;
    public final String createdBy;
    public final String updatedBy;

    protected Audited(org.jooq.Record record) {
        super(record);
        this.createdAt = record.get("created_at", OffsetDateTime.class).toInstant();
        this.updatedAt = record.get("updated_at", OffsetDateTime.class).toInstant();
        this.createdBy = record.get("created_by", String.class);
        this.updatedBy = record.get("updated_by", String.class);
    }
}
```

#### DTO-Typen

| Typ | Erbt von | Zweck |
|-----|----------|-------|
| `*Dto` | `Audited` | Response (Lesen), befuellt sich aus jOOQ-Record |
| `*CreateDto` | nichts | Request (Neu anlegen), alle fachlichen Felder |
| `*UpdateDto` | `Versioned` | Request (Aktualisieren), id + version + alle fachlichen Felder |

#### Beispiel: Response-DTO

```java
public class CrmPersonDto extends Audited {
    public final String firstName;
    public final String lastName;
    public final String notes;

    public CrmPersonDto(JooqGeneratedBisRecordPerson record) {
        super(record);  // id, version, audit-felder automatisch
        this.firstName = record.getFirstName();
        this.lastName = record.getLastName();
        this.notes = record.getNotes();
    }
}
```

Repository wird einzeilig durch Method-Reference:

```java
public Optional<CrmPersonDto> findById(UUID id) {
    return _database.dsl()
        .selectFrom(tablePerson)
        .where(tablePerson.ID.eq(id))
        .fetchOptional()
        .map(CrmPersonDto::new);
}
```

#### Beispiel: Create-DTO

```java
public class CrmPersonCreateDto {
    public String firstName;
    public String lastName;
    public String notes;
}
```

#### Beispiel: Update-DTO

```java
public class CrmPersonUpdateDto extends Versioned {
    public String firstName;
    public String lastName;
    public String notes;
}
```

Create und Update haben die gleichen fachlichen Felder. Update hat zusaetzlich `id` + `version` (von Versioned). Das Frontend schickt beim Update immer den vollstaendigen Datensatz — jOOQ erkennt selbst welche Felder sich geaendert haben.

#### Composite-Aggregate fuer Multi-Entity-Responses

Wenn ein Response zwei oder mehr Audited-Entities buendelt (z.B. eine `party`-Zeile zusammen mit der `person`-Zeile, an der sie haengt), **nicht** flach machen mit gepraefixten Versionsfeldern (`partyVersion`, `personVersion`). Stattdessen ein `record *AggregateDto(Entity1Dto, Entity2Dto)` als Wrapper — jede Component traegt ihren eigenen Audit-Envelope, Optimistic-Lock-Checks koennen pro Tabelle erfolgen.

```java
public record CrmPartyAggregateDto(CrmPartyDto party, CrmPersonDto person) {
}
```

JSON:

```json
{
  "header": {
    "party":  { "id": "...", "version": 1, "createdAt": "...", "organisationId": "...", "notes": "..." },
    "person": { "id": "...", "version": 1, "createdAt": "...", "firstName": "...", "lastName": "..." }
  }
}
```

Naming: `*AggregateDto`, Suffix `Dto` ist auch hier Pflicht (gilt fuer alle JSON-Klassen, auch records). Der `header`-Schluessel kommt aus dem UseCase-`Response`-Record-Wrapper.

Composite ist nur fuer **echte** Mehrfach-Entity-Sichten. Eine reine Projektion einer einzigen Entity (z.B. ein `*HeaderDto`, das einfach nur `id` zu `organisationId` aliased) ist **kein** Composite — dort entfaellt der eigene Typ, und der UseCase-Response traegt direkt das Entity-DTO.

#### Ref- und Listen-DTOs (records bleiben)

Reduzierte Projektionen fuer Listen-/Such-Resultate (`*RefDto`, `*ListItemDto`, `*SummaryDto`) **bleiben Records**, kein Audited. Sie fuehren nur die paar Felder, die der Listen-Eintrag braucht (typischerweise `id` + Anzeigeattribut + Status-Flag), und sind nicht das Update-Subjekt.

```java
public record CrmPersonRefDto(
        UUID id,
        Optional<String> title,
        String firstName,
        String lastName,
        Optional<Gender> gender
) {
    public CrmPersonRefDto(final JooqGeneratedBisRecordPerson record) { ... }
}
```

Auch reine **Container/Aggregator-Records** (`CrmPartyContactDataDto(partyId, ImmutableList<CrmPhoneDto> phones, ...)`) bleiben records — sie buendeln nur, sind selbst kein Audit-Subjekt.

#### Update-DTOs mit Path-Param-id (Sonderfall)

Wenn der Endpoint die `id` bereits aus dem URL-Path bezieht und der Body sie **nicht** redundant fuehrt (typisch fuer Sub-Entity-Updates wie Phone/Email/Address am Party), erbt das Update-DTO **nicht** `Versioned`. Stattdessen plain class mit `public long version;` plus fachliche Felder:

```java
public final class CrmPhoneUpdateDto {
    public long version;
    public String number;
    public UUID typeId;
    public boolean isPrimary;
}
```

Begruendung: `Versioned` bringt ein `id`-Feld, das hier nie befuellt wird (oder der Endpoint muesste es nach Deserialisierung manuell aus dem Path setzen — unnoetiger Reibungspunkt). Pragmatik vor formaler Konsistenz.

### Klassen DTOs (Ausnahme: DI-Injection)

Nur verwenden wenn Dependency Injection benötigt wird:

```java
@Component
public class ProductDownloadDto {
    public final UUID id;
    public final String filename;
    public final String url;

    @Inject
    @JsonIgnore
    private StorageService _storageService;

    public ProductDownloadDto(final ProductDownloadDbContext record) {
        this.id = record.download().getId();
        this.filename = record.downloadFile().getFilenameOriginal();
        this.url = _storageService.createPublicUrl(record.downloadFile());
    }
}
```

**Beachte bei Klassen-DTOs:**
- `public final` Felder (keine Getter)
- DI-Felder mit `@JsonIgnore` markieren
- Privates Feld mit `_underscorePrefix`

### Sealed Klassen (Polymorphe DTOs)

Fuer polymorphe Datenstrukturen mit exhaustive Switch-Support:

```java
public sealed interface PaymentResult
    permits PaymentSuccess, PaymentFailure, PaymentPending {
}

public record PaymentSuccess(UUID transactionId, Instant timestamp)
    implements PaymentResult {}

public record PaymentFailure(String errorCode, String message)
    implements PaymentResult {}

public record PaymentPending(UUID pendingId)
    implements PaymentResult {}
```

**Verwendung im Switch:**

```java
return switch (result) {
    case PaymentSuccess s -> handleSuccess(s);
    case PaymentFailure f -> handleFailure(f);
    case PaymentPending p -> handlePending(p);
};
```

### Naming fuer Sealed Klassen

Nicht zwingend `*Dto`, sondern nach Anwendungsfall:
- `*Result` - Ergebnisse von Operationen
- `*Event` - Domain Events
- `*Command` - Command-Objekte
- `*Message` - Queue Messages

---

## Checkliste

- [ ] Suffix `*Dto` verwendet
- [ ] Record als Standard fuer einfache DTOs (Refs, Listen-Items, Container, Sub-Records)
- [ ] Versioned/Audited Pattern fuer Entitaeten mit Audit-Feldern
- [ ] Response-DTOs: `extends Audited`, Konstruktor mit jOOQ-Record
- [ ] Create-DTOs: keine Vererbung, alle fachlichen Felder, plus no-arg + all-args Konstruktor
- [ ] Update-DTOs: `extends Versioned`, alle fachlichen Felder vollstaendig
- [ ] Update-DTOs mit Path-Param-id: plain class mit `public long version;` (kein Versioned)
- [ ] Multi-Entity-Response: `record *AggregateDto(Entity1Dto, Entity2Dto)`, **nicht** flachgepraefixte Versionsfelder
- [ ] Optional-Felder in Plain-Class-DTOs auf `Optional.empty()` defaulten (sonst NPE wenn Jackson-Key fehlt)
- [ ] Serialisierung auf Feldebene
- [ ] Keine Geschaeftslogik
- [ ] Bei DI-Klassen-DTOs: `@JsonIgnore` fuer DI-Felder
- [ ] Bei Polymorphie: Sealed Interface
- [ ] Enums in DTOs: Domain-Enums verwenden, nicht jOOQ-Enums
