package com.github.zrdj.java.filesearch.filesystem.attributes;

import com.github.zrdj.java.filesearch.filesystem.Attributes;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.LinkOption;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;

public final class NoFollowLinks implements Attributes {
    private final Path path;

    public NoFollowLinks(Path path) {
        this.path = path;
    }

    @Override
    public Path path() {
        return path;
    }

    @Override
    public boolean followLinks() {
        return false;
    }

    @Override
    public BasicFileAttributes load() throws IOException {
        return Files.readAttributes(path, BasicFileAttributes.class, LinkOption.NOFOLLOW_LINKS);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        NoFollowLinks that = (NoFollowLinks) o;

        return path != null ? path.equals(that.path) : that.path == null;

    }

    @Override
    public int hashCode() {
        return path != null ? path.hashCode() : 0;
    }
}
