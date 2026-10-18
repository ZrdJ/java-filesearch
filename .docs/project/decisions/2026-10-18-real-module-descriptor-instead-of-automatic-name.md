---
type: decision
title: A real module descriptor, not an automatic module name
updated: 2026-10-18
status: accepted
origin: []
---

## Context

`tibbots/bots` wants to use the zrdj libraries from its named JPMS modules, so all of them get a
real module descriptor in one sweep; `java-properties` went first
(`zrdj/java-properties`, pull request #18), and this repo follows the same model. A named module can
only `requires` another named module. A plain jar without a descriptor still works there as an
automatic module, but its name is derived from the jar file name instead of being chosen.

Until now this library shipped no `module-info.class` and no `Automatic-Module-Name` manifest entry.
Absent both, the JPMS file name algorithm turns `java-filesearch-0.4.1.jar` into the automatic module
name `java.filesearch` — a name in the `java.*` namespace the JDK reserves for platform modules. Such
a name compiles and runs today as long as the consumer starts from the classpath, where the runtime
module system never resolves it; it is a latent failure, not a current one.

## Decision

**Ship a real `module-info.java`, module name `com.github.zrdj.java.filesearch`, matching the root
package.** No `Automatic-Module-Name` fallback: that entry would need the same non-`java.*` value
anyway, and a real descriptor additionally states the module's dependencies and its public surface
explicitly.

The module has no `requires` clause beyond the implicit `java.base`: the only dependencies in
`pom.xml` are JUnit 4 and AssertJ, both in test scope, and no main source file imports anything
outside `java.*` and the library's own packages.

All seven packages are exported:

- `com.github.zrdj.java.filesearch` — `Search`, `FileSearch`
- `com.github.zrdj.java.filesearch.filesystem` — `Attributes`, `Directory`, `FileEntry`
- `com.github.zrdj.java.filesearch.filesystem.attributes` — `Cached`, `FollowLinks`, `NoFollowLinks`,
  `NoFollowLinksFallback`
- `com.github.zrdj.java.filesearch.iterator` — `CloseableIterator`, `RepeatableIterator`
- `com.github.zrdj.java.filesearch.iterator.empty` — `EmptyIterator`
- `com.github.zrdj.java.filesearch.iterator.file` — the `File`-flavored directory iterators
- `com.github.zrdj.java.filesearch.iterator.path` — the `Path`-flavored directory iterators

## Rationale

- **The derived name sits in a reserved namespace.** The first module-path start, `jlink` image or
  JDK that tightens the check would turn a consumer's green build red, and no test in either repo
  would catch it beforehand, because the descriptor is the only place the name appears.
- **A descriptor is also documentation.** `requires java.filesearch;` in a consumer reads as a
  platform module; `requires com.github.zrdj.java.filesearch;` reads as what it is.
- **Every package is exported, none held back.** Today every package is reachable on the classpath,
  and its classes are public. The subpackages are visible from the entry point — `FileSearch`'s
  implementations are built on the `iterator.file` and `iterator.path` types and the
  `filesystem` types — and some consumer may already use them directly. Hiding a package would break
  such a consumer as soon as it moves to the module path, for no gain this decision needs.

## Consequences

- `pom.xml`'s `<version>` moves from `0.4.0` to `0.5.0`, catching up with the already-tagged `0.4.1`
  and going one further because this changes how JPMS consumers name the library, not a patch. The
  README's dependency snippet follows to `0.5.0`.
- `maven.compiler.source`/`target` stay at `11`. JPMS exists since Java 9, and `maven-compiler-plugin`
  3.16.0 detects `module-info.java` and compiles it without `<release>`; the tests, which share the
  root package, compile and run unchanged. No build configuration change beyond the version bump.
- Classpath consumers are unaffected: a modular jar read from the classpath behaves as before.
- Consumers on `0.4.1` keep working. This release removes a latent problem; nothing about adopting
  it is urgent.
