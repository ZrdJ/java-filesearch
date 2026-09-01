---
type: spec
title: Distribution
updated: 2026-09-01
---

## Purpose

Makes the library obtainable as a versioned Maven dependency without a
Maven Central publish: JitPack builds the artifact directly from this
GitHub repository's tags, and a GitHub release both triggers that build and
keeps the version documented in the README current. Every push is built
and tested against the range of JDKs the library targets.

## Requirements

### Requirement: The library is built and tested against every supported JDK on each push
`req~distribution.jdk-compatibility-build~1`

`.github/workflows/build.yml` must run `mvn -B -ntp verify` for every push
to any branch, once each for JDK 11, 17 and 21. `pom.xml` declares
`junit` and `assertj-core` as test-scoped dependencies and `src/test`
holds 2 JUnit test files, so `verify` both compiles/packages the artifact
and runs that test suite. A further push to the same branch must cancel
the still-running build for the previous push on that branch.

#### Scenario: Push to a branch

- **WHEN** a commit is pushed to any branch
- **THEN** `mvn -B -ntp verify` runs once under JDK 11, once under JDK 17
  and once under JDK 21, compiling and running the test suite each time

#### Scenario: Second push while the first build is still running

- **WHEN** a commit is pushed to a branch while the build for a previous
  commit on that same branch is still running
- **THEN** the previous build is cancelled

### Requirement: A published GitHub release triggers the JitPack build and updates the documented version
`req~distribution.release-publishes-artifact~1`

`.github/workflows/release.yml` must, on a published GitHub release,
request a JitPack build for the release's tag and rewrite every
`<version>` element in `README.md` to that tag, committing the change to
`main`. The Maven coordinates `com.github.zrdj:java-filesearch` resolve on
JitPack against this repository, `ZrdJ/java-filesearch`.

#### Scenario: Release published

- **WHEN** a GitHub release with tag `X` is published
- **THEN** a build for tag `X` is requested from JitPack at
  `jitpack.io/com/github/ZrdJ/java-filesearch/X/build.log`
- **AND** `README.md`'s `<version>` elements are set to `X` and committed to
  `main`
