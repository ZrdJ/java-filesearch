# JitPack Konfiguration

## Maven Wrapper (empfohlen)

JitPack verwendet standardmaessig eine aeltere Maven-Version. Neuere Maven-Plugins (z.B. `maven-compiler-plugin:3.13.0+`) erfordern Maven 3.6.3+.

**Loesung: Maven Wrapper auf aktuelle Version pinnen**

```bash
# Maven Wrapper generieren (falls mvn verfuegbar)
mvn wrapper:wrapper -Dmaven=3.9.9

# Oder manuell: .mvn/wrapper/maven-wrapper.properties erstellen
```

```properties
# .mvn/wrapper/maven-wrapper.properties
distributionUrl=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.9.9/apache-maven-3.9.9-bin.zip
wrapperUrl=https://repo.maven.apache.org/maven2/org/apache/maven/wrapper/maven-wrapper/3.3.2/maven-wrapper-3.3.2.jar
```

JitPack erkennt den Maven Wrapper automatisch und verwendet `./mvnw` statt System-Maven.

## jitpack.yml (Alternative)

Nur noetig wenn kein Maven Wrapper verwendet wird:

```yaml
# jitpack.yml im Repository-Root
jdk:
  - openjdk11

before_install:
  - sdk install maven 3.9.9
```

## pom.xml Anforderungen

### Minimale Konfiguration

```xml
<groupId>com.github.Owner</groupId>
<artifactId>repo-name</artifactId>
<version>0.5.0</version>
<packaging>jar</packaging>

<properties>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
```

### Source und Javadoc JARs (optional)

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-source-plugin</artifactId>
            <version>3.3.0</version>
            <executions>
                <execution>
                    <id>attach-sources</id>
                    <goals><goal>jar</goal></goals>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-javadoc-plugin</artifactId>
            <version>3.6.3</version>
            <executions>
                <execution>
                    <id>attach-javadocs</id>
                    <goals><goal>jar</goal></goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

## JitPack Build-Prozess

1. JitPack klont das Repository beim angegebenen Tag
2. Fuehrt `./mvnw install` aus (oder `mvn install`)
3. Cached das Ergebnis fuer zukuenftige Requests

## Wichtig

- **Keine Credentials** - JitPack braucht keinen Token fuer oeffentliche Repos
- **Maven Wrapper empfohlen** - Konsistente Maven-Version
- **Tests laufen** - JitPack fuehrt standardmaessig Tests aus
