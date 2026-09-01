package com.github.zrdj.java.filesearch;

import com.github.zrdj.java.filesearch.filesystem.Attributes;
import com.github.zrdj.java.filesearch.filesystem.FileEntry;
import com.github.zrdj.java.filesearch.filesystem.attributes.Cached;
import com.github.zrdj.java.filesearch.filesystem.attributes.FollowLinks;
import com.github.zrdj.java.filesearch.filesystem.attributes.NoFollowLinks;
import com.github.zrdj.java.filesearch.filesystem.attributes.NoFollowLinksFallback;
import org.junit.Assume;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

public class FileIdentityAndAttributesTest {
    @Rule
    public final TemporaryFolder tempFolder = new TemporaryFolder();

    // [impl->req~file-identity-and-attributes.graceful-attribute-failure~1]
    @Test
    public void testExistenceAndKindChecksReturnFalseInsteadOfThrowing() {
        final Path missing = tempFolder.getRoot().toPath().resolve("does-not-exist");
        final FileEntry entry = new FileEntry.Smart(missing);

        assertThat(entry.valid()).isFalse();
        assertThat(entry.isFile()).isFalse();
        assertThat(entry.isDirectory()).isFalse();
    }

    // [impl->req~file-identity-and-attributes.identity-fallback~1]
    @Test
    public void testEqualityByNativeFileKeyWhenBothAreAvailable() throws IOException {
        final Path file = tempFolder.newFile("a.txt").toPath();
        final FileEntry first = new FileEntry.Smart(file);
        final FileEntry second = new FileEntry.Smart(file);

        assertThat(first.uniqueKey()).isNotNull();
        assertThat(second.uniqueKey()).isNotNull();
        assertThat(first).isEqualTo(second);
    }

    // [impl->req~file-identity-and-attributes.identity-fallback~1]
    @Test
    public void testEqualityFallsBackToSameFileWhenAKeyIsUnavailable() throws IOException {
        final Path file = tempFolder.newFile("b.txt").toPath();
        final Path missing = tempFolder.getRoot().toPath().resolve("also-missing");
        final FileEntry withKey = new FileEntry.Smart(file);
        // Same path, but wired to an Attributes that always fails to load -
        // the only way to make uniqueKey() null without deleting the file
        // that path() itself must keep pointing at.
        final FileEntry withoutKey = new FileEntry.Smart(file, new NoFollowLinks(missing));

        assertThat(withoutKey.uniqueKey()).isNull();
        assertThat(withoutKey).isEqualTo(withKey);
    }

    // [impl->req~file-identity-and-attributes.hashcode-fallback~1]
    @Test
    public void testHashCodeFallsBackToPathHashWhenKeyIsUnavailable() throws IOException {
        final Path file = tempFolder.newFile("c.txt").toPath();
        final Path missing = tempFolder.getRoot().toPath().resolve("also-missing-2");
        final FileEntry withoutKey = new FileEntry.Smart(file, new NoFollowLinks(missing));

        assertThat(withoutKey.uniqueKey()).isNull();
        assertThat(withoutKey.hashCode()).isEqualTo(file.hashCode());
    }

    // [impl->req~file-identity-and-attributes.attribute-loading-chain~1]
    @Test
    public void testLinkFollowingSucceedsAndIsReturnedDirectly() throws IOException {
        final Path file = tempFolder.newFile("d.txt").toPath();
        final Attributes attributes = new FollowLinks(file);

        assertThat(attributes.load()).isNotNull();
        assertThat(attributes.followLinks()).isTrue();
    }

    // [impl->req~file-identity-and-attributes.attribute-loading-chain~1]
    @Test
    public void testLinkFollowingFailureFallsBackToNotFollowingLinks() throws IOException {
        final Path brokenLink = tempFolder.getRoot().toPath().resolve("broken-link");
        try {
            Files.createSymbolicLink(brokenLink, tempFolder.getRoot().toPath().resolve("no-such-target"));
        } catch (UnsupportedOperationException | IOException e) {
            Assume.assumeNoException("symlinks are not supported in this environment", e);
        }

        // Confirm the premise: following the (broken) link really does throw.
        assertThatThrownBy(() -> new FollowLinks(brokenLink).load()).isInstanceOf(IOException.class);

        final Attributes fallback = new NoFollowLinksFallback(new FollowLinks(brokenLink));
        assertThat(fallback.load()).isNotNull();
        assertThat(fallback.followLinks()).isFalse();
    }

    // [impl->req~file-identity-and-attributes.attribute-loading-chain~1]
    @Test
    public void testCachedReusesTheFirstSuccessfulLoad() throws IOException {
        final Path file = tempFolder.newFile("e.txt").toPath();
        final Cached cached = new Cached(new FollowLinks(file));

        final BasicFileAttributes first = cached.load();
        final BasicFileAttributes second = cached.load();

        assertThat(second).isSameAs(first);
    }
}
