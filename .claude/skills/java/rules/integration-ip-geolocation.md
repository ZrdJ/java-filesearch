---
title: MaxMind GeoLite2
impact: LOW
tags: geolocation, ip, maxmind, geoip, location
---

# MaxMind GeoLite2

Dieser Skill beschreibt MaxMind GeoLite2 - IP-Geolokalisierung.

### Maven

```xml
<properties>
    <geoip2.version>5.0.2</geoip2.version>
</properties>

<dependencies>
    <dependency>
        <groupId>com.maxmind.geoip2</groupId>
        <artifactId>geoip2</artifactId>
        <version>${geoip2.version}</version>
    </dependency>
</dependencies>
```

---

### GeoLite2 Datenbanken

| Datenbank | Datei | Zweck |
|-----------|-------|-------|
| City | GeoLite2-City.mmdb | Stadt-Level |
| Country | GeoLite2-Country.mmdb | Land-Level |
| ASN | GeoLite2-ASN.mmdb | Autonomous System |

**Download:** https://dev.maxmind.com/geoip/geolite2-free-geolocation-data

---

### Geolite2 Service

```java
@Component
public class Geolite2 {
    @Inject private Logger _log;
    private final Map<Databases, DatabaseReader> _databases = new HashMap<>();

    public enum Databases {
        City("GeoLite2-City.mmdb"),
        Country("GeoLite2-Country.mmdb");

        private final String name;
        Databases(final String name) { this.name = name; }

        public Path path() {
            return Paths.get(Environment.isLocal()
                ? ".local/maxmind" : "/maxmind").resolve(name);
        }
    }

    public record GeoLocation(String de, String en) {}
}
```

---

### IP zu Standort

```java
public Optional<GeoLocation> locationFromIP(final String ip) {
    try {
        final var reader = _databases.get(Databases.City);
        if (reader == null) return Optional.empty();

        final var cityResponse = reader.city(InetAddress.getByName(ip));
        if (cityResponse == null) return Optional.empty();

        return Optional.of(new GeoLocation(
            getLocation(cityResponse, "de"),
            getLocation(cityResponse, "en")
        ));
    } catch (Exception e) {
        _log.error("Failed to get location for IP: {}", ip, e);
        return Optional.empty();
    }
}

private String getLocation(final CityResponse response, final String lang) {
    final var city = response.city().names().get(lang);
    final var country = response.country().names().get(lang);
    return Stream.of(city, country)
        .filter(Objects::nonNull)
        .collect(Collectors.joining(", "));
}
```

---

### Verzeichnisstruktur

```
# Lokal
.local/maxmind/
├── GeoLite2-City.mmdb
└── GeoLite2-Country.mmdb

# Produktion (Docker Volume)
/maxmind/
├── GeoLite2-City.mmdb
└── GeoLite2-Country.mmdb
```

---

### Best Practices

1. **DatabaseReader cachen** - Einmal laden
2. **Shutdown Hook** - Datenbanken schließen
3. **Optional** - Fehlertoleranz
4. **Nicht committen** - .mmdb in .gitignore

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt
- [ ] GeoLite2 Datenbanken heruntergeladen
- [ ] .mmdb in .gitignore
- [ ] DatabaseReader als Singleton
- [ ] Service-Klasse implementiert
- [ ] Shutdown Hook registriert
