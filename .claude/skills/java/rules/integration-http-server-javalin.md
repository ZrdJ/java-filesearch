---
title: Javalin HTTP Server
impact: CRITICAL
tags: http, rest, javalin, endpoints, cors, exceptions
---

# Javalin HTTP Server

Dieser Skill beschreibt den REST API Server mit Javalin.

### Maven

```xml
<properties>
    <javalin.version>7.0.0</javalin.version>
</properties>

<dependency>
    <groupId>io.javalin</groupId>
    <artifactId>javalin</artifactId>
    <version>${javalin.version}</version>
</dependency>
```

---

### Server Konfiguration

```java
@Component
public class HttpServer {
    @Inject private Logger _log;
    @Inject private UsecaseExecutor _usecases;
    @Inject private JsonMapper _jsonMapper;

    private final Javalin _javalin;
    private final ImmutableList<HttpEndpoints> _endpoints;

    public HttpServer() {
        _javalin = Javalin.create(this::configure);
        _endpoints = Lists.immutable.of(
            new HttpProductEndpoints(),
            new HttpAccountEndpoints()
        );
    }

    private void configure(JavalinConfig config) {
        config.jetty.threadPool = new HttpThreadPool(200);

        config.bundledPlugins.enableCors(cors -> {
            cors.addRule(it -> {
                it.allowCredentials = true;
                it.reflectClientOrigin = true;
            });
        });

        config.jsonMapper(_jsonMapper);
        config.routes.exception(Exception.class, this::handleException);
        config.routes.before(this::beforeRequest);
        config.requestLogger.http(this::logRequest);
    }

    public void start() {
        _endpoints.forEach(ep -> ep.configure(_javalin.router()));
        _javalin.start(8080);
    }
}
```

---

### Exception Handler

```java
private void handleException(Exception e, Context ctx) {
    switch (e) {
        case BadRequest br -> {
            ctx.status(400);
            ctx.json(new ErrorModel(br.validationErrors()));
        }
        case Unauthorized u -> {
            ctx.status(401);
            ctx.json(new ErrorModel(Lists.immutable.of(
                new ValidationError("auth", "Unauthorized"))));
        }
        case Forbidden f -> {
            ctx.status(403);
            ctx.json(new ErrorModel(f.validationErrors()));
        }
        case NotFound nf -> {
            ctx.status(404);
            ctx.json(new ErrorModel(nf.validationErrors()));
        }
        default -> {
            ctx.status(500);
            ctx.json(new ErrorModel(Lists.immutable.of(
                new ValidationError("server", "Internal error"))));
            _log.error("Internal error", e);
        }
    }
}
```

---

### Endpoint Implementierung

```java
@Component
public class HttpProductEndpoints implements HttpEndpoints {
    @Inject private UsecaseExecutor _usecases;

    @Override
    public void configure(RoutesConfig router) {
        // GET Liste
        router.get("/api/products", ctx -> {
            final var response = _usecases.execute(
                new GetProductsUsecase.Request(),
                new WebSession(ctx));
            ctx.json(response);
        });

        // GET einzeln
        router.get("/api/products/{productId}", ctx -> {
            final UUID id = UUID.fromString(ctx.pathParam("productId"));
            final var response = _usecases.execute(
                new GetProductByIdUsecase.Request(id),
                new WebSession(ctx));
            ctx.json(response);
        });

        // POST
        router.post("/api/products", ctx -> {
            final var body = ctx.bodyAsClass(ProductCreateDto.class);
            final var response = _usecases.execute(
                new CreateProductUsecase.Request(body),
                new WebSession(ctx));
            ctx.status(HttpStatus.CREATED);
            ctx.json(response);
        });

        // PATCH
        router.patch("/api/products/{productId}", ctx -> {
            final UUID id = UUID.fromString(ctx.pathParam("productId"));
            final var body = ctx.bodyAsClass(ProductUpdateDto.class);
            final var response = _usecases.execute(
                new UpdateProductUsecase.Request(id, body),
                new WebSession(ctx));
            ctx.json(response);
        });

        // DELETE
        router.delete("/api/products/{productId}", ctx -> {
            final UUID id = UUID.fromString(ctx.pathParam("productId"));
            _usecases.execute(new DeleteProductUsecase.Request(id), new WebSession(ctx));
            ctx.status(HttpStatus.NO_CONTENT);
        });
    }
}
```

---

### File Upload

```java
router.post("/api/documents", ctx -> {
    final var files = ctx.uploadedFiles().stream()
        .map(f -> new ReceivedFile(
            InputStreamSupport.from(f.content()).toByteArray(),
            f.contentType(), f.filename(), f.extension(), f.size()))
        .collect(Collectors2.toImmutableList());

    final var response = _usecases.execute(
        new UploadDocumentUsecase.Request(files),
        new WebSession(ctx));
    ctx.json(response);
});
```

---

### Query Parameter

```java
router.get("/api/products", ctx -> {
    final var page = Optional.ofNullable(ctx.queryParam("page"))
        .map(Integer::parseInt).orElse(1);

    final var sort = Optional.ofNullable(ctx.queryParam("sort"))
        .map(SortOrder::valueOf).orElse(SortOrder.ASC);

    final var active = Boolean.parseBoolean(
        Optional.ofNullable(ctx.queryParam("active")).orElse("true"));
});
```

---

### Thread Pool

```java
public class HttpThreadPool extends QueuedThreadPool {
    private final AtomicInteger _counter = new AtomicInteger(1);

    public HttpThreadPool(int maxThreads) { super(maxThreads); }

    @Override
    public Thread newThread(Runnable runnable) {
        final var thread = super.newThread(runnable);
        thread.setName("http-thread-" + String.format("%03d", _counter.getAndIncrement()));
        return thread;
    }
}
```

---

## Checkliste

- [ ] Maven Dependency hinzugefuegt
- [ ] HttpServer Klasse erstellt
- [ ] CORS konfiguriert
- [ ] Exception Handler implementiert
- [ ] HttpEndpoints Interface implementiert
- [ ] Endpoints registriert
- [ ] Thread Pool konfiguriert
