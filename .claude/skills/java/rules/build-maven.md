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

### Assembly (Anwendungs-JAR plus `lib/`)

Eine Anwendung wird **nie** als Fat JAR gebaut — weder mit `maven-shade-plugin` noch mit dem
`jar-with-dependencies`-Deskriptor des Assembly-Plugins. Beide entpacken die Abhaengigkeiten in ein
einziges Archiv, und dabei ueberschreiben sich Dateien, die mehrere Jars an derselben Stelle
mitbringen: `META-INF/services`, `reference.conf`, Signaturdateien. Der Shade kann das mit
Transformern reparieren, `jar-with-dependencies` kann es gar nicht — und eine Reparatur, die still
scheitert, faellt erst beim Start auf, nicht im gruenen Build.

Stattdessen bleibt das Anwendungs-JAR fuer sich, die Abhaengigkeiten liegen als eigene Jars daneben,
und der Klassenpfad steht im Manifest.

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-dependency-plugin</artifactId>
    <version>${maven.dependency.plugin.version}</version>
    <executions>
        <execution>
            <id>copy-dependencies</id>
            <phase>package</phase>
            <goals><goal>copy-dependencies</goal></goals>
            <configuration>
                <outputDirectory>${project.build.directory}/lib</outputDirectory>
                <includeScope>runtime</includeScope>
            </configuration>
        </execution>
    </executions>
</plugin>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-jar-plugin</artifactId>
    <version>${maven.jar.plugin.version}</version>
    <configuration>
        <archive>
            <manifest>
                <mainClass>net.example.Application</mainClass>
                <addClasspath>true</addClasspath>
                <classpathPrefix>lib/</classpathPrefix>
            </manifest>
        </archive>
    </configuration>
</plugin>
```

`java -jar target/app.jar` funktioniert damit unveraendert: `Class-Path` im Manifest wird relativ zum
Jar aufgeloest. Zusaetzlich bleibt lesbar, welche Version welcher Abhaengigkeit ausgeliefert wird —
genau das verliert ein Fat JAR, und mit ihm die Grundlage fuer CVE-Scans und das Nachziehen einer
einzelnen Abhaengigkeit.

Ein verteilbares Archiv (`tar.gz`, `zip`) baut `maven-assembly-plugin` mit einem eigenen Deskriptor
darauf auf — erst dann, wenn ein Deployment eines braucht.

Bei einem `module-info.java` kommt hinzu, dass ein Fat JAR den Moduldeskriptor verwirft: `shade`
fuehrt ihn nicht zusammen, und die Anwendung laeuft danach aus dem unbenannten Modul. Die Assembly
erhaelt ihn.

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
- [ ] Abhaengigkeiten als eigene Jars plus Manifest-Klassenpfad (nie ein Fat JAR)
