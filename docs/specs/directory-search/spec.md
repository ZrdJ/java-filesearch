---
type: spec
title: Directory Search
updated: 2026-09-01
---

## Purpose

Lets a caller search a directory for `File` or `Path` entries, recursively
or not, through one fluent entry point — `Search.search().directory(...)`
— and get a lazily-produced `Stream<T>` back, instead of choosing between
`File.listFiles()` and `Files.walkFileTree()` and wiring the traversal by
hand.

## Requirements

### Requirement: A directory must be set before a search can be produced
`req~directory-search.directory-required~1`

`Search.byFile()` and `Search.byPath()` both call `.get()` on an internal
`Optional<File>` that starts empty and is only populated by one of the
`directory(...)` overloads. Calling either method before `directory(...)`
has been called throws `NoSuchElementException`.

#### Scenario: No directory set

- **WHEN** `byFile()` or `byPath()` is called on a `Search` that has not
  had `directory(...)` called
- **THEN** a `NoSuchElementException` is thrown

### Requirement: The search directory can be given as a File, a Path or a String
`req~directory-search.directory-input-forms~1`

`directory(File)` stores the file as-is; `directory(Path)` stores
`path.toFile()`; `directory(String)` stores `new File(path)`. All three
overloads set the same target for a subsequent `byFile()`/`byPath()` call.

#### Scenario: Same target regardless of input type

- **WHEN** `directory(file)`, `directory(file.toPath())` and
  `directory(file.getPath())` are each used to configure a separate
  `Search` for the same location
- **THEN** all three searches operate against the same directory

### Requirement: recursively()/notRecursively() combined with byFile()/byPath() selects one of four FileSearch implementations
`req~directory-search.implementation-routing~1`

`Search` is not recursive by default. Each combination of recursion flag
and result type routes to a distinct `FileSearch` implementation:
not-recursive + `byFile()` to `FileSearch.ByFile`, recursive + `byFile()`
to `FileSearch.ByFileRecursive`, not-recursive + `byPath()` to
`FileSearch.ByPath`, recursive + `byPath()` to
`FileSearch.ByPathRecursive`.

#### Scenario: Not recursive, by File

- **WHEN** `byFile()` is called without `recursively()` having been called
- **THEN** the search is a `FileSearch.ByFile`

#### Scenario: Recursive, by File

- **WHEN** `recursively()` is called before `byFile()`
- **THEN** the search is a `FileSearch.ByFileRecursive`

#### Scenario: Not recursive, by Path

- **WHEN** `byPath()` is called without `recursively()` having been
  called
- **THEN** the search is a `FileSearch.ByPath`

#### Scenario: Recursive, by Path

- **WHEN** `recursively()` is called before `byPath()`
- **THEN** the search is a `FileSearch.ByPathRecursive`

### Requirement: The produced stream claims to be distinct, sorted and ordered regardless of the underlying traversal order
`req~directory-search.stream-characteristics~1`

`FileSearch.stream()` wraps its iterator in a `Spliterator` built with
`Spliterator.DISTINCT | Spliterator.SORTED | Spliterator.ORDERED`. Neither
`File.listFiles()` nor `Files.newDirectoryStream()` guarantees a sorted or
duplicate-free listing, so these flags are asserted, not verified — a
caller chaining `.sorted()` or `.distinct()` on the returned `Stream<T>`
may see those operations elided by the JDK because it trusts the
characteristics already claimed, not because the entries are actually
sorted or unique.

#### Scenario: Stream reports DISTINCT, SORTED and ORDERED

- **WHEN** `stream()` is called on any `FileSearch<T>`
- **THEN** the returned `Stream`'s underlying `Spliterator` reports
  `DISTINCT`, `SORTED` and `ORDERED` characteristics
