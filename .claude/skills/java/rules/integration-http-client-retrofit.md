---
title: Retrofit HTTP Client
impact: HIGH
tags: retrofit, http-client, okhttp, rest-client, api
---

# Retrofit HTTP Client

Dieser Skill beschreibt Retrofit mit OkHttp fuer Third-Party API Anbindungen.

### Maven

```xml
<properties>
    <retrofit.version>2.9.0</retrofit.version>
</properties>

<dependencies>
    <dependency>
        <groupId>com.squareup.retrofit2</groupId>
        <artifactId>retrofit</artifactId>
        <version>${retrofit.version}</version>
    </dependency>
    <dependency>
        <groupId>com.squareup.retrofit2</groupId>
        <artifactId>converter-jackson</artifactId>
        <version>${retrofit.version}</version>
    </dependency>
</dependencies>
```

---

### Retrofit Builder Setup

```java
final var httpClient = new OkHttpClient.Builder()
    .connectTimeout(5, TimeUnit.SECONDS)
    .readTimeout(10, TimeUnit.SECONDS)
    .writeTimeout(10, TimeUnit.SECONDS)
    .addInterceptor(new AuthInterceptor())
    .build();

final var retrofit = new Retrofit.Builder()
    .baseUrl("https://api.example.com/")
    .client(httpClient)
    .addConverterFactory(JacksonConverterFactory.create(objectMapper))
    .build();

_injector.add(retrofit.create(ExampleApi.class));
```

---

### Service Interface

```java
public interface DeepLApi {
    @POST("v2/translate")
    Call<DeepLTranslationResponse> translate(@Body DeepLTranslationRequest request);
}

public interface CloudflareApi {
    @POST("zones/{zoneId}/purge_cache")
    Call<CloudflarePurgeCacheResponse> purgeCache(
        @Path("zoneId") String zoneId,
        @Header("Authorization") String authorization,
        @Body CloudflarePurgeCacheRequest request
    );
}

public interface GithubApi {
    @GET("repos/{owner}/{repo}/releases/latest")
    Call<GithubRelease> latestRelease(
        @Path("owner") String owner,
        @Path("repo") String repo
    );
}
```

---

### Annotations

| Annotation | Zweck | Beispiel |
|------------|-------|----------|
| `@GET` | GET Request | `@GET("users/{id}")` |
| `@POST` | POST Request | `@POST("users")` |
| `@PUT` | PUT Request | `@PUT("users/{id}")` |
| `@DELETE` | DELETE Request | `@DELETE("users/{id}")` |
| `@Path` | Path Parameter | `@Path("id") String id` |
| `@Query` | Query Parameter | `@Query("page") int page` |
| `@Header` | HTTP Header | `@Header("Auth") String token` |
| `@Body` | Request Body | `@Body UserDto user` |

---

### Service Wrapper

```java
@Component
public class CloudflareApiService {
    private final CloudflareApi _api;
    @Inject private ApplicationPropertyStore _store;
    @Inject private Logger _log;

    public CloudflarePurgeCacheResponse purgeByTags(final List<String> tags) {
        try {
            final var response = _api.purgeCache(
                zoneId(), authorization(),
                CloudflarePurgeCacheRequest.byTags(tags)
            ).execute();

            if (!response.isSuccessful()) {
                throw new RuntimeException("API failed: " + response.code());
            }
            return response.body();
        } catch (IOException e) {
            throw new RuntimeException("Request failed", e);
        }
    }
}
```

---

### Auth Interceptor

```java
@Component
public class AuthInterceptor implements Interceptor {
    @Inject private ApplicationPropertyStore _store;

    @Override
    public Response intercept(final Chain chain) throws IOException {
        final var apiKey = _store.get(Properties.ApiKey)
            .map(ApplicationPropertyValue::asString)
            .orElseThrow();

        final var request = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer " + apiKey)
            .build();

        return chain.proceed(request);
    }
}
```

---

### Best Practices

1. **JacksonConverterFactory** - Shared ObjectMapper
2. **Service Wrapper** - Retrofit-Details abstrahieren
3. **Interceptors** - Für Auth, Logging, MDC
4. **Synchrone Calls** - `.execute()` für einfache Fälle

---

## Checkliste

- [ ] Maven Dependencies hinzugefuegt
- [ ] OkHttpClient konfiguriert (Timeouts)
- [ ] Retrofit Builder mit JacksonConverterFactory
- [ ] Service Interface definiert
- [ ] Service Wrapper implementiert
- [ ] Auth Interceptor (optional)
