---
title: JUseCase Inject DI
impact: CRITICAL
tags: dependency-injection, di, inject, jusecase, aspectj
---

# JUseCase Inject

Dieser Skill beschreibt JUseCase Inject - AspectJ-basierte Dependency Injection.

### Maven

```xml
<properties>
    <jusecase-inject.version>1.0.0</jusecase-inject.version>
    <aspectj.version>1.9.25</aspectj.version>
</properties>

<dependencies>
    <dependency>
        <groupId>org.jusecase</groupId>
        <artifactId>inject</artifactId>
        <version>${jusecase-inject.version}</version>
    </dependency>
    <dependency>
        <groupId>org.aspectj</groupId>
        <artifactId>aspectjrt</artifactId>
        <version>${aspectj.version}</version>
    </dependency>
</dependencies>
```

---

### AspectJ Maven Plugin

```xml
<plugin>
    <groupId>dev.aspectj</groupId>
    <artifactId>aspectj-maven-plugin</artifactId>
    <version>1.14.1</version>
    <configuration>
        <complianceLevel>${jdk.version}</complianceLevel>
        <showWeaveInfo>true</showWeaveInfo>
        <aspectLibraries>
            <aspectLibrary>
                <groupId>org.jusecase</groupId>
                <artifactId>inject</artifactId>
            </aspectLibrary>
        </aspectLibraries>
    </configuration>
    <executions>
        <execution>
            <phase>process-classes</phase>
            <goals><goal>compile</goal></goals>
        </execution>
    </executions>
</plugin>
```

---

### @Component und @Inject

```java
@Component
public class ProductRepositoryJooq implements ProductRepository {
    @Inject
    private ApplicationDatabase _database;
    @Inject
    private Logger _log;
}
```

**Jede Klasse mit `@Inject`-Feldern MUSS `@Component` annotiert sein.** Ohne `@Component` werden die `@Inject`-Felder nicht vom AspectJ-Weaver erkannt und bleiben `null`.

---

### Injector-Zugriff: Strikte Regeln

**VERBOTEN:** Der `Injector` darf NUR in Bootstrap-Klassen verwendet werden:

| Erlaubt | Beispiel |
|---------|----------|
| `Application.java` | Root-Registrierung von Providern, Plugins, BusinessLogic, HttpServer |
| `BusinessLogic.java` | Registrierung von Services und UseCases |
| Dedizierte `*Module`-Klassen | Falls Registrierung in Module ausgelagert wird |

**VERBOTEN in allen anderen Klassen:**
- Kein `Injector.getInstance()` in Services, UseCases, Endpoints, Repositories
- Kein `injector.inject()` ausserhalb des Registrierungszyklus
- Kein `injector.resolve()` in Geschaeftslogik
- Kein `injector.add()` zur Laufzeit

**Warum:** Der Injector ist kein Service Locator. Alle Abhaengigkeiten werden beim Start registriert und danach per `@Inject` aufgeloest. Wenn eine Klasse den Injector braucht, ist das ein Architektur-Problem — die Abhaengigkeit fehlt im DI-Graph.

**Einzige Ausnahme:** `HttpServer.start()` darf `Injector.getInstance()` verwenden um Endpoints zu injizieren, weil Endpoints erst beim Server-Start erstellt werden (nach dem Registrierungszyklus).

---

### Injector Setup (Application)

```java
public class Application {
    public Application(final Injector injector) {
        // Config
        var config = ApplicationConfig.load();
        injector.add(config);

        // Providers
        injector.addProvider(new LoggerFacadeProvider());
        injector.addProviderForSingleInstance(new ApplicationDatabaseProvider());
        injector.add(new JacksonJsonPlugin());

        // Business Logic (registriert Services + UseCases intern)
        injector.add(new BusinessLogic(injector));

        // HTTP Server (nach BusinessLogic — braucht UsecaseExecutor)
        injector.inject(_httpServer = new HttpServer(), HttpServer.class);
    }

    public static void main(final String[] args) {
        new Application(Injector.getInstance()).start();
    }
}
```

### BusinessLogic (Service-Registrierung)

```java
public BusinessLogic(final Injector injector) {
    // Einfache Services — @Inject-Felder werden automatisch befuellt
    injector.add(new PasswordHasher());
    injector.add(new SessionService());

    // Services mit Initialisierung — inject() + initialize() noetig
    var geoService = new GeoLocationService();
    injector.inject(geoService, GeoLocationService.class);
    geoService.initialize();
    injector.add(geoService);

    // UseCases registrieren
    addUsecase(LoginUsecase.Request.class, new LoginUsecase());
}
```

**Wann `injector.inject()` noetig ist:** Nur wenn eine Klasse nach `new` sofort auf `@Inject`-Felder zugreifen muss (z.B. in `initialize()`). Bei einfachen Services reicht `injector.add()` — die `@Inject`-Felder werden beim ersten Zugriff durch den AspectJ-Weaver befuellt.

---

### Provider Patterns

```java
// Per-Class Provider (z.B. Logger)
@Component
public class LoggerFacadeProvider implements PerClassProvider<Logger> {
    @Override
    public Logger get(final Class<?> aClass) {
        return LoggerFactory.getLogger(aClass);
    }
}

// Singleton Provider (z.B. Database)
@Component
public class ApplicationDatabaseProvider implements Provider<ApplicationDatabase> {
    @Inject
    private ApplicationConfig _config;

    @Override
    public ApplicationDatabase get() {
        // HikariCP + Flyway + jOOQ Setup
        return new ApplicationDatabase(dsl);
    }
}
```

---

### Injector API

| Methode | Zweck | Wo verwenden |
|---------|-------|--------------|
| `Injector.getInstance()` | Singleton Injector | Nur in `main()` |
| `addProvider(Provider<T>)` | Neue Instanz pro Aufruf | Bootstrap |
| `addProviderForSingleInstance(Provider<T>)` | Singleton | Bootstrap |
| `add(Object)` | Direkte Instanz registrieren | Bootstrap |
| `inject(Object, Class<?>)` | @Inject-Felder sofort fuellen | Bootstrap (nur wenn noetig) |

---

### Anti-Patterns

```java
// VERBOTEN — Injector in Service
@Component
public class SomeService {
    public void doSomething() {
        var db = Injector.getInstance().resolve(ApplicationDatabase.class); // NEIN!
    }
}

// RICHTIG — @Inject verwenden
@Component
public class SomeService {
    @Inject
    private ApplicationDatabase _database;
}

// VERBOTEN — injector.inject() in UseCase
public Response execute(Request request) {
    var helper = new SomeHelper();
    injector.inject(helper, SomeHelper.class); // NEIN!
}

// RICHTIG — Helper als @Inject-Feld
@Inject
private SomeHelper _helper;
```

---

### Best Practices

1. **@Component auf allen injizierbaren Klassen** — Pflicht fuer @Inject
2. **Private Fields mit @Inject** — `_fieldName` Konvention
3. **Provider fuer externe Dependencies** — Database, PropertyStore
4. **SingleInstance fuer teure Ressourcen** — Database, HTTP Clients
5. **Injector NUR in Bootstrap-Klassen** — Application, BusinessLogic
6. **Kein Service Locator Pattern** — Nie `Injector.getInstance()` in Geschaeftslogik

---

## Checkliste

- [ ] Maven Dependencies hinzugefuegt
- [ ] AspectJ Maven Plugin konfiguriert
- [ ] @Component auf allen Klassen mit @Inject-Feldern
- [ ] @Inject fuer private Felder (`_fieldName`)
- [ ] Provider fuer externe Dependencies
- [ ] Injector Setup nur in Application + BusinessLogic
- [ ] Kein Injector-Zugriff in Services/UseCases/Endpoints
