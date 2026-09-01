package com.github.zrdj.java.filesearch;

import org.junit.Assume;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

import static com.github.zrdj.java.filesearch.Search.search;
import static org.assertj.core.api.Assertions.assertThat;

public class RecursiveTraversalSafetyTest {
    @Rule
    public final TemporaryFolder tempFolder = new TemporaryFolder();

    // [impl->req~recursive-traversal-safety.lazy-depth-first-expansion~1]
    @Test
    public void testDirectoryIsFullyDescendedBeforeReturningToRemainingSiblings() {
        final File root = new File("src/test/resources/searchstructure");
        final List<Path> entries = new ArrayList<>();
        search().directory(root).recursively().byPath().stream().forEach(entries::add);

        // Depth-first means every directory's whole subtree is a *contiguous*
        // run right after it, regardless of what order siblings happen to be
        // listed in (that order is filesystem-defined, not asserted here).
        for (int i = 0; i < entries.size(); i++) {
            final Path current = entries.get(i);
            if (!Files.isDirectory(current))
                continue;
            int afterSubtree = i + 1;
            while (afterSubtree < entries.size() && entries.get(afterSubtree).startsWith(current))
                afterSubtree++;
            for (int k = afterSubtree; k < entries.size(); k++)
                assertThat(entries.get(k).startsWith(current))
                        .as("%s must not reappear once traversal has left it", current)
                        .isFalse();
        }
    }

    // [impl->req~recursive-traversal-safety.lazy-depth-first-expansion~1]
    @Test
    public void testEmptyDirectoryYieldsItselfButNoChildrenAndTraversalContinues() throws IOException {
        final File root = tempFolder.newFolder("root");
        new File(root, "empty").mkdir();
        final File withFile = new File(root, "withFile");
        withFile.mkdir();
        new File(withFile, "f.txt").createNewFile();

        final List<Path> entries = new ArrayList<>();
        search().directory(root).recursively().byPath().stream().forEach(entries::add);

        assertThat(entries).hasSize(3); // empty/, withFile/, withFile/f.txt
        assertThat(entries).anyMatch(p -> p.endsWith("empty"));
    }

    // [impl->req~recursive-traversal-safety.symlink-cycle-protection~1]
    @Test(timeout = 5000)
    public void testPathFlavorSkipsADirectoryThatRepeatsAnAncestorsIdentity() throws IOException {
        final File root = tempFolder.newFolder("cycleRoot");
        final File a = new File(root, "a");
        final File b = new File(a, "b");
        assertThat(b.mkdirs()).isTrue();
        try {
            Files.createSymbolicLink(new File(b, "loop").toPath(), a.toPath());
        } catch (UnsupportedOperationException | IOException e) {
            Assume.assumeNoException("symlinks are not supported in this environment", e);
        }

        final List<Path> entries = new ArrayList<>();
        search().directory(root).recursively().byPath().stream().forEach(entries::add);

        // a, b, loop - loop's identity matches a's (its ancestor), so it is
        // skipped rather than opened again. An unprotected traversal would
        // never reach this assertion at all (@Test(timeout) is the backstop
        // in case this reasoning is wrong, so the suite fails fast instead
        // of hanging CI).
        assertThat(entries).hasSize(3);
    }

    // [impl->req~recursive-traversal-safety.directory-stream-cleanup~2]
    @Test
    public void testDirectoryStreamsAreClosedAsTraversalAdvancesPastEachSibling() throws IOException {
        // Only observable from outside the facade via the process's open file
        // descriptors - /proc/self/fd is Linux-specific (true of both this
        // devcontainer and the ubuntu-latest CI runner; skips cleanly
        // elsewhere rather than failing on an unrelated platform).
        Assume.assumeTrue("requires /proc/self/fd (Linux)",
                new File("/proc/self/fd").isDirectory());

        final File root = tempFolder.newFolder("cleanupRoot");
        for (int i = 0; i < 40; i++) {
            final File sibling = new File(root, "sib" + i);
            sibling.mkdir();
            new File(sibling, "f.txt").createNewFile();
        }

        final int before = openFileDescriptorCount();
        search().directory(root).recursively().byPath().stream().forEach(p -> {
        });
        final int after = openFileDescriptorCount();

        assertThat(after)
                .as("open file descriptors before vs. after traversing 40 sibling directories")
                .isEqualTo(before);
    }

    // [impl->req~recursive-traversal-safety.directory-stream-cleanup~2]
    @Test
    public void testRootDirectoryStreamIsClosedEvenWhenRootHasNoSubdirectoryToDescendInto() throws IOException {
        // Same rationale as testDirectoryStreamsAreClosedAsTraversalAdvancesPastEachSibling
        // for why /proc/self/fd and why Linux-only.
        Assume.assumeTrue("requires /proc/self/fd (Linux)",
                new File("/proc/self/fd").isDirectory());

        final File emptyRoot = tempFolder.newFolder("emptyRoot");
        final File filesOnlyRoot = tempFolder.newFolder("filesOnlyRoot");
        new File(filesOnlyRoot, "a.txt").createNewFile();
        new File(filesOnlyRoot, "b.txt").createNewFile();

        // The root's own DirectoryStream is only ever closed via the ancestor
        // stack, and the root never lands on that stack unless one of its own
        // subdirectories gets opened. A root with no subdirectory - empty, or
        // containing only files - never triggers that push, so its stream
        // would otherwise never close. Repeating 3x per root turns a single
        // possibly-lost descriptor into an unmistakable cumulative delta.
        for (File root : new File[]{emptyRoot, filesOnlyRoot}) {
            final int before = openFileDescriptorCount();
            for (int i = 0; i < 3; i++)
                search().directory(root).recursively().byPath().stream().forEach(p -> {
                });
            final int after = openFileDescriptorCount();

            assertThat(after)
                    .as("open file descriptors before vs. after searching root '%s' (no subdirectory), repeated 3x", root.getName())
                    .isEqualTo(before);
        }
    }

    private static int openFileDescriptorCount() throws IOException {
        try (Stream<Path> fds = Files.list(new File("/proc/self/fd").toPath())) {
            return (int) fds.count();
        }
    }
}
