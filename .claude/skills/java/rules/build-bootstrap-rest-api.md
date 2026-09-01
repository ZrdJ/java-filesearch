---
title: Bootstrap REST API
impact: MEDIUM
tags: bootstrap, rest-api, setup, template
---

# Bootstrap REST API

Dieser Skill beschreibt das minimale Setup fuer eine Java REST API.

### Projektstruktur

```
my-backend/
├── pom.xml                         # Parent POM
├── backend-server/
│   └── src/main/java/net/example/
│       ├── Application.java
│       └── http/
│           ├── HttpServer.java
│           └── feature/product/
├── backend-core/
│   └── src/main/java/net/example/core/
│       ├── BusinessLogic.java
│       └── feature/product/
│           ├── usecase/
│           ├── domain/
│           └── api/
├── backend-persistence/
└── backend-bootstrap/
```

---

### Application.java

```java
public class Application {
    private final BusinessLogic _businessLogic;
    private final HttpServer _httpServer;

    public Application(final Injector injector) {
        // Provider
        injector.addProvider(new LoggerFacadeProvider());
        injector.addProviderForSingleInstance(new ApplicationPropertyStoreProvider());

        // Plugins
        injector.add(new JacksonJsonPlugin());

        // Business Logic
        injector.inject(_businessLogic = new BusinessLogic(injector), BusinessLogic.class);
        injector.add(_businessLogic);

        // HTTP Server
        injector.inject(_httpServer = new HttpServer(), HttpServer.class);
    }

    public static void main(final String[] args) {
        new Application(Injector.getInstance()).start();
    }

    private void start() {
        _httpServer.start();
    }
}
```

---

### HttpServer.java

```java
@Component
public class HttpServer {
    @Inject private Logger _log;
    @Inject private UsecaseExecutor _usecases;
    @Inject private JsonMapper _jsonMapper;

    private final Javalin _javalin;

    public HttpServer() {
        _javalin = Javalin.create(config -> {
            config.jsonMapper(_jsonMapper);
            config.bundledPlugins.enableCors(cors -> {
                cors.addRule(it -> {
                    it.allowCredentials = true;
                    it.reflectClientOrigin = true;
                });
            });
            config.routes.exception(Exception.class, this::handleException);
        });
    }

    public void start() {
        new HttpProductEndpoints().configure(_javalin.router());
        _javalin.start(8080);
    }
}
```

---

### BusinessLogic.java

```java
@Component
public class BusinessLogic extends AbstractUsecaseExecutor {
    public BusinessLogic(final Injector injector) {
        addUsecase(GetProductsUsecase.Request.class, new GetProductsUsecase());
        addUsecase(CreateProductUsecase.Request.class, new CreateProductUsecase());
    }
}
```

---

### GetProductsUsecase.java

```java
@Component
public class GetProductsUsecase
    implements PublicUsecase<GetProductsUsecase.Request, GetProductsUsecase.Response> {

    public static class Request extends RequestWithPublicContext {}
    public record Response(ImmutableList<ProductDto> products) {}

    @Inject private ProductRepository _productRepository;

    @Override
    public Response execute(final Request request) {
        return new Response(_productRepository.findAll());
    }
}
```

---

### Checkliste

- [ ] Parent POM mit Modulen
- [ ] Maven Wrapper
- [ ] Application Entry Point
- [ ] HttpServer mit Javalin
- [ ] BusinessLogic mit UseCase-Registrierung
- [ ] Erster UseCase
- [ ] Logging konfigurieren
