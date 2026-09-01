---
type: research
title: README vs. code drift
updated: 2026-09-01
---

Found while deriving the as-is spec (see `../../specs/`).

## Version mismatch

`README.md`'s Maven snippet pins `<version>0.4.1</version>`; `pom.xml`
itself declares `<version>0.4.0</version>`. Same pattern as
`java-identifiers` and `java-properties`:
`.github/workflows/release.yml` only rewrites `README.md`'s `<version>`
elements on release, never `pom.xml`'s own `<version>`.
