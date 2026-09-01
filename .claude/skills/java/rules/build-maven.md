---
title: Maven Single-Module
impact: HIGH
tags: maven, build, pom, wrapper
---

# Maven Single-Module

Dieser Skill beschreibt das minimale Setup fuer ein Java-Projekt mit Maven.

### Projektstruktur

```
my-project/
├── .mvn/wrapper/
│   └── maven-wrapper.properties
├── src/
│   ├── main/java/
│   └── test/java/
├── mvnw
├── mvnw.cmd
└── pom.xml
```

---

### Maven Wrapper

```properties
# .mvn/wrapper/maven-wrapper.properties
wrapperVersion=3.3.4
distributionType=only-script
distributionUrl=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.9.12/apache-maven-3.9.12-bin.zip
```

```bash
mvn wrapper:wrapper -Dmaven=3.9.12
```

---

### pom.xml Grundstruktur

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>net.example</groupId>
    <artifactId>my-project</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <properties>
        <jdk.version>21</jdk.version>
        <maven.compiler.source>${jdk.version}</maven.compiler.source>
        <maven.compiler.target>${jdk.version}</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>

        <maven.compiler.plugin.version>3.15.0</maven.compiler.plugin.version>
        <maven.surefire.plugin.version>3.5.5</maven.surefire.plugin.version>
        <junit.version>5.11.0</junit.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>${maven.compiler.plugin.version}</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>${maven.surefire.plugin.version}</version>
            </plugin>
        </plugins>
    </build>
</project>
```

---

### Assembly Plugin (Fat JAR)

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-assembly-plugin</artifactId>
    <version>3.8.0</version>
    <configuration>
        <descriptorRefs>
            <descriptorRef>jar-with-dependencies</descriptorRef>
        </descriptorRefs>
        <archive>
            <manifest>
                <mainClass>net.example.Application</mainClass>
            </manifest>
        </archive>
    </configuration>
    <executions>
        <execution>
            <phase>package</phase>
            <goals><goal>single</goal></goals>
        </execution>
    </executions>
</plugin>
```

---

### Befehle

```bash
./mvnw clean compile        # Kompilieren
./mvnw test                 # Tests
./mvnw package              # JAR erstellen
./mvnw package -DskipTests  # Ohne Tests
./mvnw install              # Lokales Repository

# Dependency Updates (ohne Pre-Release)
./mvnw versions:display-dependency-updates \
  "-Dmaven.version.ignore=.*-M.*,.*-alpha.*,.*-rc.*,.*-beta.*"
```

---

## Checkliste

- [ ] Projektstruktur angelegt
- [ ] Maven Wrapper installiert
- [ ] pom.xml konfiguriert
- [ ] JDK Version gesetzt
- [ ] JUnit hinzugefuegt
- [ ] Assembly Plugin (optional)
