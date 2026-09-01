---
title: UA-Parser User-Agent
impact: LOW
tags: useragent, browser, device, os, parsing
---

# UA-Parser

Dieser Skill beschreibt UA-Parser - parst User-Agent Strings zu Browser, OS und Device.

### Maven

```xml
<properties>
    <uap-java.version>1.6.1</uap-java.version>
</properties>

<dependencies>
    <dependency>
        <groupId>com.github.ua-parser</groupId>
        <artifactId>uap-java</artifactId>
        <version>${uap-java.version}</version>
    </dependency>
</dependencies>
```

---

### Grundlagen

```java
import ua_parser.Parser;
import ua_parser.Client;

Parser parser = new Parser();
Client client = parser.parse(userAgent);

// Browser
client.userAgent.family;  // "Mobile Safari"
client.userAgent.major;   // "16"

// Betriebssystem
client.os.family;         // "iOS"
client.os.major;          // "16"

// Gerät
client.device.family;     // "iPhone"
```

---

### Service-Klasse

```java
@Component
public class UserAgentService {
    private final Parser _parser = new Parser();

    public UserAgentInfo parse(final String userAgent) {
        if (userAgent == null || userAgent.isBlank()) {
            return UserAgentInfo.unknown();
        }

        Client client = _parser.parse(userAgent);

        return new UserAgentInfo(
            browser(client.userAgent),
            os(client.os),
            device(client.device)
        );
    }

    private String browser(final UserAgent ua) {
        if (ua == null || ua.family == null) return "Unknown";
        return ua.major != null
            ? "%s %s".formatted(ua.family, ua.major)
            : ua.family;
    }
}

public record UserAgentInfo(String browser, String os, String device) {
    public static UserAgentInfo unknown() {
        return new UserAgentInfo("Unknown", "Unknown", "Unknown");
    }
}
```

---

### Integration mit Javalin

```java
httpServer.before(ctx -> {
    String userAgent = ctx.header("User-Agent");
    UserAgentInfo info = _userAgentService.parse(userAgent);
    ctx.attribute("userAgentInfo", info);
});
```

---

### Best Practices

1. **Parser als Singleton** - Wiederverwenden
2. **Null-Checks** - family/major können null sein
3. **Caching** - Bei hohem Traffic cachen
4. **Nicht für Security** - User-Agent kann gefälscht werden

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt
- [ ] Parser als Singleton
- [ ] UserAgentInfo Record erstellt
- [ ] Service-Klasse implementiert
- [ ] Null-Safety beachtet
