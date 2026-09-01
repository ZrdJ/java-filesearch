# Dependency-Einbindung

## Maven

### Repository hinzufuegen

```xml
<repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>
```

### Dependency hinzufuegen

```xml
<dependency>
    <groupId>com.github.Owner</groupId>
    <artifactId>repo-name</artifactId>
    <version>0.5.0</version>
</dependency>
```

## Gradle (Kotlin DSL)

```kotlin
repositories {
    maven { url = uri("https://jitpack.io") }
}

dependencies {
    implementation("com.github.Owner:repo-name:0.5.0")
}
```

## Gradle (Groovy)

```groovy
repositories {
    maven { url 'https://jitpack.io' }
}

dependencies {
    implementation 'com.github.Owner:repo-name:0.5.0'
}
```

## Versions-Optionen

| Version | Bedeutung |
|---------|-----------|
| `0.5.0` | Spezifischer Release-Tag |
| `main-SNAPSHOT` | Letzter Commit auf main |
| `abc1234` | Spezifischer Commit-Hash |

## README Badge

```markdown
[![](https://jitpack.io/v/Owner/repo-name.svg)](https://jitpack.io/#Owner/repo-name)
```

## Beispiel README-Sektion

```markdown
## Installation

Add the JitPack repository:

\`\`\`xml
<repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>
\`\`\`

Add the dependency:

\`\`\`xml
<dependency>
    <groupId>com.github.Owner</groupId>
    <artifactId>repo-name</artifactId>
    <version>0.5.0</version>
</dependency>
\`\`\`
```
