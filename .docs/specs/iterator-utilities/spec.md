---
type: spec
title: Iterator Utilities
updated: 2026-09-01
---

## Purpose

Small `Iterator` building blocks the traversal iterators (see
`recursive-traversal-safety`) are assembled from: `RepeatableIterator`
re-exposes the value most recently returned by `next()`, `EmptyIterator`
is a always-empty iterator usable as a fallback, and `CloseableIterator`
is the marker combining `Iterator` with `Closeable` that the Path-flavored
iterators implement.

## Requirements

### Requirement: A RepeatableIterator re-exposes the value most recently returned by next()
`req~iterator-utilities.repeatable-current~1`

`RepeatableIterator.Smart.current()` returns the value the last `next()`
call returned; `hasCurrent()` is `false` until `next()` has been called at
least once, and `true` afterward.

#### Scenario: No current value before the first next()

- **WHEN** `hasCurrent()` is called on a fresh `RepeatableIterator.Smart`
  before `next()` has been called
- **THEN** it returns `false`

#### Scenario: current() mirrors the last next()

- **WHEN** `next()` is called and returns a value, then `current()` is
  called
- **THEN** `current()` returns that same value, and `hasCurrent()` returns
  `true`

### Requirement: RepeatableIterator.Closeable delegates close() to its CloseableIterator, and iteration to its RepeatableIterator
`req~iterator-utilities.closeable-delegation~1`

`RepeatableIterator.Closeable(closeableIterator)` defaults its
`RepeatableIterator` delegate to `new Smart<>(closeableIterator)`, and
routes `close()` to the `CloseableIterator` it was built from.

#### Scenario: close() delegates to the wrapped CloseableIterator

- **WHEN** `close()` is called on a `RepeatableIterator.Closeable`
- **THEN** the wrapped `CloseableIterator`'s `close()` is invoked

### Requirement: EmptyIterator never has a next element, and returns null rather than throwing when next() is called anyway
`req~iterator-utilities.empty-iterator~1`

`EmptyIterator.hasNext()` always returns `false`. Calling `next()`
regardless returns `null` instead of throwing
`NoSuchElementException` — a deviation from the standard `Iterator`
contract that callers relying on this class must account for.

#### Scenario: hasNext is always false

- **WHEN** `hasNext()` is called on an `EmptyIterator`
- **THEN** it returns `false`

#### Scenario: next() returns null instead of throwing

- **WHEN** `next()` is called on an `EmptyIterator`
- **THEN** it returns `null`
- **AND** no exception is thrown
