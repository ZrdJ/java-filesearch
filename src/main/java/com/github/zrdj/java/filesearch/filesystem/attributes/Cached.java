package com.github.zrdj.java.filesearch.filesystem.attributes;

import com.github.zrdj.java.filesearch.filesystem.Attributes;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;

public final class Cached implements Attributes {
    private final Attributes fallback;
    private BasicFileAttributes cachedAttributes;

    public Cached(final Attributes attributes) {
        this.fallback = attributes;
    }

    @Override
    public Path path() {
        return fallback.path();
    }

    @Override
    public boolean followLinks() {
        return fallback.followLinks();
    }

    @Override
    public BasicFileAttributes load() throws IOException {
        if (cachedAttributes == null) {
            cachedAttributes = fallback.load();
        }
        return cachedAttributes;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Cached cached = (Cached) o;

        return fallback != null ? fallback.equals(cached.fallback) : cached.fallback == null;

    }

    @Override
    public int hashCode() {
        return fallback != null ? fallback.hashCode() : 0;
    }
}
