---
title: Log4j2 mit SLF4J
impact: HIGH
tags: logging, log4j2, slf4j, json, mdc
---

# Logging mit Log4j2

Dieser Skill beschreibt strukturiertes JSON-Logging mit MDC fuer Request-Korrelation.

### Maven

```xml
<properties>
    <log4j.version>2.25.3</log4j.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <version>${log4j.version}</version>
    </dependency>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-slf4j2-impl</artifactId>
        <version>${log4j.version}</version>
    </dependency>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-layout-template-json</artifactId>
        <version>${log4j.version}</version>
    </dependency>
</dependencies>
```

---

### log4j2.xml (Konsole mit Highlighting)

Standard-Konfiguration mit farbigem Output nach Log-Level:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{HH:mm:ss.SSS} %highlight{%-5level}{FATAL=red blink, ERROR=red, WARN=yellow, INFO=green, DEBUG=cyan, TRACE=blue} %logger{36} - %msg%n"/>
        </Console>
    </Appenders>

    <Loggers>
        <Logger name="net.example" level="info" additivity="false">
            <AppenderRef ref="Console"/>
        </Logger>
        <Logger name="org.jooq" level="warn"/>
        <Logger name="io.javalin" level="warn"/>
        <Root level="info">
            <AppenderRef ref="Console"/>
        </Root>
    </Loggers>
</Configuration>
```

### log4j2.xml (File Logger)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Properties>
        <Property name="logPath">logs</Property>
    </Properties>

    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <PatternLayout pattern="%d{HH:mm:ss.SSS} %highlight{%-5level} %logger{36} - %msg%n"/>
        </Console>

        <RollingFile name="File" fileName="${logPath}/app.log"
                     filePattern="${logPath}/app-%d{yyyy-MM-dd}-%i.log.gz">
            <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level %logger{36} - %msg%n"/>
            <Policies>
                <TimeBasedTriggeringPolicy interval="1" modulate="true"/>
                <SizeBasedTriggeringPolicy size="100MB"/>
            </Policies>
            <DefaultRolloverStrategy max="14"/>
        </RollingFile>
    </Appenders>

    <Loggers>
        <Logger name="net.example" level="info" additivity="false">
            <AppenderRef ref="Console"/>
            <AppenderRef ref="File"/>
        </Logger>
        <Root level="info">
            <AppenderRef ref="Console"/>
        </Root>
    </Loggers>
</Configuration>
```

### log4j2.xml (JSON für Log-Aggregation)

Alternative für Produktion mit Log-Aggregation (ELK, Loki, etc.):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="WARN">
    <Appenders>
        <Console name="Console" target="SYSTEM_OUT">
            <JsonTemplateLayout eventTemplateUri="classpath:JsonLogLayout.json"/>
        </Console>
    </Appenders>

    <Loggers>
        <Logger name="net.example" level="info" additivity="false">
            <AppenderRef ref="Console"/>
        </Logger>
        <Root level="info">
            <AppenderRef ref="Console"/>
        </Root>
    </Loggers>
</Configuration>
```

**JsonLogLayout.json** (in `src/main/resources/`):
```json
{
  "timestamp": {
    "$resolver": "timestamp",
    "pattern": { "format": "yyyy-MM-dd'T'HH:mm:ss.SSSZ" }
  },
  "level": { "$resolver": "level", "field": "name" },
  "logger": { "$resolver": "logger", "field": "name" },
  "message": { "$resolver": "message", "stringified": true },
  "exception": { "$resolver": "exception", "field": "stackTrace", "stringified": true },
  "mdc": { "$resolver": "mdc" }
}
```

---

### Logger Injection

```java
@Component
public class ProductService {
    @Inject private Logger _log;

    public void process(UUID id) {
        _log.info("Processing: {}", id);
        try {
            // ...
        } catch (Exception e) {
            _log.error("Failed: {}", id, e);
        }
    }
}
```

---

### MDC Plugin

```java
@Component
public class MdcPlugin {
    public enum MdcIdentifier {
        RequestId("mdc.request.id"),
        RequestPath("mdc.request.path"),
        ResponseStatus("mdc.response.status"),
        ResponseDuration("mdc.response.time");

        private final String key;
        MdcIdentifier(String key) { this.key = key; }
        public String key() { return key; }
    }

    public void start(Session session, String path, String method) {
        MDC.put(MdcIdentifier.RequestId.key(), UUID.randomUUID().toString());
        MDC.put(MdcIdentifier.RequestPath.key(), path);
    }

    public void stop() { MDC.clear(); }
}
```

---

### Best Practices

1. **SLF4J als Facade**
2. **JSON Layout** für Log-Aggregation
3. **MDC** für Request-Korrelation
4. **Parameterized Logging** - `_log.info("User: {}", id)`
5. **Exception als letzter Parameter**

---

## Checkliste

- [ ] Maven Dependencies hinzugefuegt
- [ ] log4j2.xml erstellt
- [ ] Logger-Injection konfiguriert
- [ ] MDC Plugin implementiert (optional)
- [ ] JSON Layout fuer Produktion (optional)
