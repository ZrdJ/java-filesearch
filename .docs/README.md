---
type: index
title: java-filesearch — Knowledge Layer
lang: en
updated: 2026-08-31
---

# java-filesearch — Knowledge Layer

This library reimplements the JDK's file walking as a fluent, `Stream`-based API,
combining `File.listFiles()` and `Files.walkFileTree()` behind a single `Search`
entry point for recursive and non-recursive searches by `File` or `Path`.

Repo-specific knowledge. What concerns more than this repo lives in the knowledge layer
of the WS root (`~/workspaces/personal/docs/`).

## Folders

- `project/decisions/` — why things are the way they are (ADRs)
- `project/worklog/` — work logs, one file per day
- `project/research/` — self-collected material
- `project/sources/` — material delivered by others
- `wayfinding/` — undertakings whose path is not yet settled
- `changes/` — ongoing undertakings whose path is settled
- `archive/` — completed changes
- `specs/` — current state per capability

## Entry points

- `pom.xml` — coordinates (`com.github.zrdj:java-filesearch`), Java 11, JUnit4/AssertJ test deps
- `src/main/java/com/github/zrdj/java/filesearch/Search.java` — the public entry point (`Search.search()`)
- `src/main/java/com/github/zrdj/java/filesearch/FileSearch.java` — the `Stream<T>`-producing interface built on top of the iterators
- `src/test/java/com/github/zrdj/java/filesearch/SearchTest.java` — usage examples as tests
- `README.md` (repo root) — recursive/non-recursive, File-API/Path-API usage examples

This repo does not (yet) have its own `CLAUDE.md` — working rules apply from
`zrdj/CLAUDE.md` and the provider levels above it.
