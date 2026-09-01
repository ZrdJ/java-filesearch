// ============================================================
// 1. Interface (Domain Layer)
// Pfad: feature/{domain}/domain/{Domain}Repository.java
// ============================================================
package net.baunach.bis.backend.core.feature.website.{domain}.domain;

import net.baunach.bis.backend.core.feature.website.{domain}.api.{FeatureName}Dto;
import org.eclipse.collections.api.list.ImmutableList;

import java.util.Optional;
import java.util.UUID;

public interface {Domain}Repository {
    ImmutableList<{FeatureName}Dto> findAll(UUID accountId);
    Optional<{FeatureName}Dto> findById(UUID id);
    UUID create({FeatureName}Dto dto, UUID accountId);
    void update({FeatureName}Dto dto);
    void delete(UUID id);
}

// ============================================================
// 2. Implementierung (Database Layer)
// Pfad: feature/{domain}/database/{Domain}RepositoryJooq.java
// ============================================================
package net.baunach.bis.backend.core.feature.website.{domain}.database;

import net.baunach.bis.backend.core.feature.website.{domain}.api.{FeatureName}Dto;
import net.baunach.bis.backend.core.feature.website.{domain}.domain.{Domain}Repository;
import net.baunach.bis.backend.persistence.ApplicationDatabase;
import net.baunach.bis.backend.persistence.tables.ApplicationBisTables;
import org.eclipse.collections.api.list.ImmutableList;
import org.eclipse.collections.impl.collector.Collectors2;
import org.jusecase.inject.Component;

import javax.inject.Inject;
import java.util.Optional;
import java.util.UUID;

@Component
public class {Domain}RepositoryJooq implements {Domain}Repository {

    @Inject
    private ApplicationDatabase _database;

    @Override
    public ImmutableList<{FeatureName}Dto> findAll(final UUID accountId) {
        return _database.dsl()
            .selectFrom(ApplicationBisTables.table{Entity})
            .where(ApplicationBisTables.table{Entity}.ACCOUNT_ID.eq(accountId))
            .fetch()
            .stream()
            .map({FeatureName}Dto::new)
            .collect(Collectors2.toImmutableList());
    }

    @Override
    public Optional<{FeatureName}Dto> findById(final UUID id) {
        return _database.dsl()
            .selectFrom(ApplicationBisTables.table{Entity})
            .where(ApplicationBisTables.table{Entity}.ID.eq(id))
            .fetchOptional()
            .map({FeatureName}Dto::new);
    }

    @Override
    public UUID create(final {FeatureName}Dto dto, final UUID accountId) {
        final var record = _database.dsl().newRecord(ApplicationBisTables.table{Entity});
        record.setId(_database.generateId());
        // record.setAccountId(accountId);
        // record.setName(dto.name());
        record.store();
        return record.getId();
    }

    @Override
    public void update(final {FeatureName}Dto dto) {
        _database.dsl()
            .update(ApplicationBisTables.table{Entity})
            // .set(ApplicationBisTables.table{Entity}.NAME, dto.name())
            .where(ApplicationBisTables.table{Entity}.ID.eq(dto.id()))
            .execute();
    }

    @Override
    public void delete(final UUID id) {
        _database.dsl()
            .deleteFrom(ApplicationBisTables.table{Entity})
            .where(ApplicationBisTables.table{Entity}.ID.eq(id))
            .execute();
    }
}

// ============================================================
// 3. Registrierung in BusinessLogic.java
// ============================================================
// _injector.add(new {Domain}RepositoryJooq());
