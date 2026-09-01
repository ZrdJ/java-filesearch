package net.baunach.bis.backend.core.feature.website.{domain}.api;

import java.util.Optional;
import java.util.UUID;

// ============================================================
// Standard Record DTO
// ============================================================
public record {FeatureName}Dto(
    UUID id,
    String name,
    Optional<String> description
) {
    // Konstruktor fuer jOOQ-Records
    public {FeatureName}Dto(final JooqGeneratedBisRecord{Entity} record) {
        this(
            record.getId(),
            record.getName(),
            Optional.ofNullable(record.getDescription())
        );
    }
}

// ============================================================
// Sealed Interface (fuer polymorphe Ergebnisse)
// ============================================================
// public sealed interface {FeatureName}Result
//     permits {FeatureName}Success, {FeatureName}Failure {
// }
//
// public record {FeatureName}Success(UUID id) implements {FeatureName}Result {}
// public record {FeatureName}Failure(String errorCode) implements {FeatureName}Result {}
