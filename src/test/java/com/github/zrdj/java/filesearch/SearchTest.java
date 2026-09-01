package com.github.zrdj.java.filesearch;

import org.junit.Test;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.NoSuchElementException;
import java.util.Spliterator;

import static com.github.zrdj.java.filesearch.Search.search;
import static org.assertj.core.api.Assertions.assertThat;

public class SearchTest {
    private Path givenSearchDirectory;
    private int filesFound;

    // [impl->req~directory-search.implementation-routing~1]
    @Test
    public void testRecursiveSearchByPathForDirectory() throws Exception {
        givenSearchDirectory("src/test/resources/searchstructure");
        whenSearchingRecursivelyByPath();
        thenFilesFoundAre(34);
    }

    // [impl->req~directory-search.implementation-routing~1]
    @Test
    public void testSearchByPathForDirectory() throws Exception {
        givenSearchDirectory("src/test/resources/searchstructure");
        whenSearchingByPath();
        thenFilesFoundAre(4);
    }

    // [impl->req~recursive-traversal-safety.single-file-root~1]
    @Test
    public void testRecursiveSearchByPathForFile() throws Exception {
        givenSearchDirectory("src/test/resources/searchstructure/1/11.txt");
        whenSearchingRecursivelyByPath();
        thenFilesFoundAre(1);
    }

    // [impl->req~directory-search.implementation-routing~1]
    @Test
    public void testRecursiveSearchByFileForDirectory() throws Exception {
        givenSearchDirectory("src/test/resources/searchstructure");
        whenSearchingByFileRecursively();
        thenFilesFoundAre(34);
    }

    // [impl->req~directory-search.implementation-routing~1]
    @Test
    public void testSearchByFileForDirectory() throws Exception {
        givenSearchDirectory("src/test/resources/searchstructure");
        whenSearchingByFile();
        thenFilesFoundAre(4);
    }

    // [impl->req~recursive-traversal-safety.single-file-root~1]
    @Test
    public void testRecursiveSearchByFileForFile() throws Exception {
        givenSearchDirectory("src/test/resources/searchstructure/1/11.txt");
        whenSearchingByFileRecursively();
        thenFilesFoundAre(1);
    }

    // [impl->req~directory-search.directory-required~1]
    @Test(expected = NoSuchElementException.class)
    public void testByFileWithoutDirectorySetThrows() {
        search().byFile();
    }

    // [impl->req~directory-search.directory-required~1]
    @Test(expected = NoSuchElementException.class)
    public void testByPathWithoutDirectorySetThrows() {
        search().byPath();
    }

    // [impl->req~directory-search.directory-input-forms~1]
    @Test
    public void testDirectoryInputFormsTargetTheSameDirectory() {
        final File asFile = new File("src/test/resources/searchstructure");
        final Counter byFile = new Counter();
        final Counter byPath = new Counter();
        final Counter byString = new Counter();

        search().directory(asFile).byFile().stream().forEach(f -> byFile.increment());
        search().directory(asFile.toPath()).byFile().stream().forEach(f -> byPath.increment());
        search().directory(asFile.getPath()).byFile().stream().forEach(f -> byString.increment());

        assertThat(byFile.value()).isEqualTo(4);
        assertThat(byPath.value()).isEqualTo(4);
        assertThat(byString.value()).isEqualTo(4);
    }

    // [impl->req~directory-search.stream-characteristics~1]
    @Test
    public void testStreamReportsDistinctSortedAndOrderedCharacteristics() {
        givenSearchDirectory("src/test/resources/searchstructure");
        final Spliterator<Path> spliterator =
                search().directory(givenSearchDirectory).byPath().stream().spliterator();

        assertThat(spliterator.hasCharacteristics(
                Spliterator.DISTINCT | Spliterator.SORTED | Spliterator.ORDERED)).isTrue();
    }

    private void thenFilesFoundAre(int amount) {
        assertThat(filesFound).isEqualTo(amount);
    }

    private void whenSearchingByFileRecursively() {
        final Counter filesFound = new Counter();
        search().directory(givenSearchDirectory).recursively().byFile().stream().forEach(path -> filesFound.increment());
        this.filesFound = filesFound.value();
    }

    private void whenSearchingByFile() {
        final Counter filesFound = new Counter();
        search().directory(givenSearchDirectory).byFile().stream().forEach(path -> filesFound.increment());
        this.filesFound = filesFound.value();
    }

    private void whenSearchingRecursivelyByPath() {
        final Counter filesFound = new Counter();
        search().directory(givenSearchDirectory).recursively().byPath().stream().forEach(path -> filesFound.increment());
        this.filesFound = filesFound.value();
    }

    private void whenSearchingByPath() {
        final Counter filesFound = new Counter();
        search().directory(givenSearchDirectory).byPath().stream().forEach(path -> filesFound.increment());
        this.filesFound = filesFound.value();
    }

    private void givenSearchDirectory(final String path) {
        givenSearchDirectory = Paths.get(path);
    }
}
