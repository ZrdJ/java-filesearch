---
type: spec
title: File Identity and Attributes
updated: 2026-09-01
---

## Purpose

Lets a caller ask whether a `FileEntry` is (still) valid, is a file or a
directory, and compare two entries for identity, without handling
`IOException` at every call site — and lets `Directory.Smart`/
`FileEntry.Smart`'s default construction resolve filesystem attributes in
a way that tolerates broken symlinks and avoids re-reading them.

## Requirements

### Requirement: Existence and kind checks report false instead of throwing when the attribute read fails
`req~file-identity-and-attributes.graceful-attribute-failure~1`

`FileEntry.Smart.valid()`, `isFile()` and `isDirectory()` each try to load
the entry's `BasicFileAttributes` and return `false` when that load
throws `IOException` (for example because the entry no longer exists),
instead of letting the exception propagate.

#### Scenario: Attribute read fails

- **WHEN** `valid()`, `isFile()` or `isDirectory()` is called on a
  `FileEntry.Smart` whose underlying attribute read throws `IOException`
- **THEN** each returns `false`
- **AND** no exception propagates to the caller

### Requirement: Two entries are equal by native file key, falling back to same-file comparison when a key is unavailable
`req~file-identity-and-attributes.identity-fallback~1`

`FileEntry.Smart.equals` compares `uniqueKey()` (the platform's
`BasicFileAttributes.fileKey()`) when both entries have one; when either
entry's key is `null` (the key load failed, or the platform does not
provide one), it falls back to `Files.isSameFile` on the two paths
instead.

#### Scenario: Both entries have a native file key

- **WHEN** two `FileEntry.Smart` instances both resolve a non-null
  `uniqueKey()`
- **THEN** they are equal exactly when those keys are equal

#### Scenario: A file key is unavailable

- **WHEN** either of two `FileEntry.Smart` instances resolves a `null`
  `uniqueKey()`
- **THEN** equality falls back to `Files.isSameFile` on their paths

### Requirement: hashCode falls back to the path's hash, not to the same-file identity equals() uses
`req~file-identity-and-attributes.hashcode-fallback~1`

`FileEntry.Smart.hashCode()` returns `uniqueKey().hashCode()` when a key
is present, and `path.hashCode()` when it is not — the path itself, not
anything derived from `Files.isSameFile`.

#### Scenario: hashCode without a file key

- **WHEN** `hashCode()` is called on a `FileEntry.Smart` whose
  `uniqueKey()` is `null`
- **THEN** it returns that entry's `path.hashCode()`

### Requirement: Attribute loading follows symlinks by default, falls back to not following them on failure, and caches the result
`req~file-identity-and-attributes.attribute-loading-chain~1`

The default `Smart` construction wraps attribute access as
`Cached(NoFollowLinksFallback(FollowLinks(path)))`: `FollowLinks.load()`
reads attributes following symlinks; if that throws `IOException`,
`NoFollowLinksFallback.load()` retries via `NoFollowLinks.load()` (which
does not follow symlinks) instead of propagating; `Cached.load()` keeps
the first successful result and returns it on every later call without
reading the filesystem again. `NoFollowLinksFallback.followLinks()`
always answers `false`, regardless of whether the link-following attempt
actually succeeded.

#### Scenario: Link-following succeeds

- **WHEN** `load()` is called and reading attributes while following
  symlinks succeeds
- **THEN** that result is returned

#### Scenario: Link-following fails, the no-follow attempt is used instead

- **WHEN** `load()` is called and reading attributes while following
  symlinks throws `IOException`
- **THEN** attributes are instead read without following symlinks, and
  that result is returned

#### Scenario: A second load reuses the cached result

- **WHEN** `load()` is called twice on the same `Cached` instance
- **THEN** the second call returns the exact same `BasicFileAttributes`
  instance as the first, without reading the filesystem again
