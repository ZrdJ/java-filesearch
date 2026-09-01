---
type: spec
title: Recursive Traversal Safety
updated: 2026-09-01
---

## Purpose

Describes how `RecursiveDirectoryIterator` (backing `byFile().recursively()`)
and `RecursiveSilentDirectoryIterator` (backing `byPath().recursively()`)
walk a directory tree depth-first, and — this is where the two diverge —
what protection each offers against symlink cycles and open file handles,
so a caller can pick the flavor that matches how the target tree is
expected to behave.

## Requirements

### Requirement: A non-empty directory is descended into immediately; an empty one is never opened
`req~recursive-traversal-safety.lazy-depth-first-expansion~1`

Both recursive iterators expand a directory into the traversal only once
it becomes the "current" entry (the value most recently returned by
`next()`), and only after confirming — by opening it and checking for a
first entry — that it is non-empty. An empty directory is left unopened
for iteration purposes; the caller still receives the empty directory
itself as one entry.

#### Scenario: A non-empty directory is queued for descent

- **WHEN** the current entry during recursive traversal is a directory
  that contains at least one entry
- **THEN** that directory's entries are visited next, before traversal
  returns to the remaining entries of its parent

#### Scenario: An empty directory is not opened for descent

- **WHEN** the current entry during recursive traversal is a directory
  that contains no entries
- **THEN** traversal does not attempt to descend into it, and continues
  with the remaining entries of its parent

### Requirement: The search root may be a single file instead of a directory
`req~recursive-traversal-safety.single-file-root~1`

When the root passed to a recursive iterator is not a directory, both
flavors wrap it in a single-element iterator (`FileIterator` /
`FilePathIterator`) instead of a `DirectoryIterator`.

#### Scenario: Root is a single file

- **WHEN** a recursive search is rooted at a path that is a regular file,
  not a directory
- **THEN** the iterator yields exactly that one entry and nothing else

### Requirement: Only the Path-flavored iterator detects and skips a directory that repeats an ancestor's identity
`req~recursive-traversal-safety.symlink-cycle-protection~1`

`RecursiveSilentDirectoryIterator` checks, before opening a directory,
whether its identity (per `FileEntry.equals` — see
`file-identity-and-attributes`) already matches the current entry of any
iterator still on its ancestor stack; if so, it skips opening that
directory rather than descending into it again, which is what protects a
`byPath().recursively()` search against an infinite loop through a
symlink cycle. `RecursiveDirectoryIterator` (`byFile().recursively()`)
performs no equivalent check.

#### Scenario: A directory matching an ancestor's identity is skipped

- **WHEN** a directory encountered during a `byPath().recursively()`
  traversal has the same identity as a directory already open higher up
  the current traversal path
- **THEN** that directory is not opened again

### Requirement: Only the Path-flavored iterator releases each directory's open resource as traversal moves past it
`req~recursive-traversal-safety.directory-stream-cleanup~2`

`RecursiveSilentDirectoryIterator` reads each directory through a
`DirectoryStream`, an OS-level resource. As traversal advances past a
directory — whether by exhausting it or by finding it empty — that
directory's `DirectoryStream` is closed, and any `IOException` raised by
`close()` is swallowed rather than propagated. This holds for the search
root the same as for any directory found beneath it, including a root
that has no subdirectory to descend into (empty, or containing only
files) — the root's own `DirectoryStream` is still closed once traversal
is exhausted. `RecursiveDirectoryIterator` reads directories via
`File.listFiles()`, which holds no such resource open, so it has nothing
to close.

#### Scenario: A directory's stream is closed once traversal moves past it

- **WHEN** a `byPath().recursively()` traversal finishes or skips a
  directory
- **THEN** that directory's `DirectoryStream` is closed
- **AND** an `IOException` from that close does not propagate to the
  caller

#### Scenario: The root's stream is closed even when it has no subdirectory to descend into

- **WHEN** the root passed to a `byPath().recursively()` traversal is
  empty, or contains only files and no subdirectories
- **THEN** the root's own `DirectoryStream` is closed once traversal is
  exhausted, the same as any other directory's
