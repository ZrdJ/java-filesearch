---
title: Maven Multi-Module
impact: HIGH
tags: maven, multimodule, parent-pom, modules
---

# Maven Multi-Module

Dieser Skill beschreibt Multi-Module Maven Projekte mit Parent POM.

### Projektstruktur

```
my-project/
├── pom.xml                    # Parent POM (packaging: pom)
├── project-server/            # HTTP Server + Assembly
├── project-core/              # Business Logic
├── project-persistence/       # Datenbank Layer
└── project-bootstrap/         # Konfiguration
```

---

### Parent pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <groupId>net.example</groupId>
    <artifactId>my-project</artifactId>
    <version>1.0-ROLLING</version>
    <packaging>pom</packaging>

    <modules>
        <module>project-server</module>
        <module>project-core</module>
        <module>project-persistence</module>
        <module>project-bootstrap</module>
    </modules>

    <properties>
        <jdk.version>21</jdk.version>
        <maven.compiler.source>${jdk.version}</maven.compiler.source>
        <maven.compiler.target>${jdk.version}</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

        <!-- Dependencies zentral verwalten -->
        <javalin.version>7.0.0</javalin.version>
        <jackson.version>2.21.1</jackson.version>
        <jooq.version>3.20.11</jooq.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <!-- Interne Module -->
            <dependency>
                <groupId>net.example</groupId>
                <artifactId>project-core</artifactId>
                <version>${project.version}</version>
            </dependency>
            <!-- Externe Dependencies -->
            <dependency>
                <groupId>io.javalin</groupId>
                <artifactId>javalin</artifactId>
                <version>${javalin.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
```

---

### Module pom.xml

```xml
<project>
    <parent>
        <groupId>net.example</groupId>
        <artifactId>my-project</artifactId>
        <version>1.0-ROLLING</version>
    </parent>

    <artifactId>project-server</artifactId>

    <dependencies>
        <dependency>
            <groupId>net.example</groupId>
            <artifactId>project-core</artifactId>
        </dependency>
        <dependency>
            <groupId>io.javalin</groupId>
            <artifactId>javalin</artifactId>
        </dependency>
    </dependencies>
</project>
```

---

### Modul-Abhängigkeiten

```
project-server
├── project-core
└── project-bootstrap

project-core
├── project-persistence
└── project-bootstrap

project-persistence
└── project-bootstrap
```

---

### Befehle

```bash
# Gesamtes Projekt bauen
./mvnw clean install

# Ohne Tests
./mvnw clean install -DskipTests

# Nur bestimmtes Modul (mit Abhängigkeiten)
./mvnw clean install -pl project-server -am
```

---

## Checkliste

- [ ] Parent POM mit packaging=pom
- [ ] Module definiert
- [ ] dependencyManagement konfiguriert
- [ ] Interne Module-Versionen mit ${project.version}
- [ ] Module-POMs mit parent-Referenz
- [ ] Modul-Abhaengigkeiten korrekt
