package net.baunach.bis.backend.core.feature.website.{domain}.usecase;

import net.baunach.bis.backend.core.feature.website.{domain}.api.{FeatureName}Dto;
import net.baunach.bis.backend.core.feature.website.{domain}.domain.{Domain}Repository;
import net.baunach.bis.backend.core.framework.jusecase.CustomerUsecase;
import net.baunach.bis.backend.core.framework.jusecase.request.RequestWithCustomerContext;
import org.eclipse.collections.api.list.ImmutableList;
import org.jusecase.inject.Component;

import javax.inject.Inject;
import java.util.UUID;

@Component
public class WebsiteAccount{FeatureName}Usecase
    implements CustomerUsecase<WebsiteAccount{FeatureName}Usecase.Request, WebsiteAccount{FeatureName}Usecase.Response> {

    // Response als Record
    public record Response(ImmutableList<{FeatureName}Dto> items) {}

    // Request mit Customer-Kontext
    public static class Request extends RequestWithCustomerContext {
        // Optional: Request-Parameter
        // public final UUID categoryId;
        // public Request(UUID categoryId) { this.categoryId = categoryId; }
    }

    @Inject
    private {Domain}Repository _{domain}Repository;

    @Override
    public Response execute(final Request request) {
        final var accountId = request.context().account().id();
        final var items = _{domain}Repository.findAll(accountId);
        return new Response(items);
    }
}
