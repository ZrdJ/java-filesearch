package com.github.zrdj.java.filesearch.filesystem;

import com.github.zrdj.java.filesearch.filesystem.attributes.Cached;
import com.github.zrdj.java.filesearch.filesystem.attributes.FollowLinks;
import com.github.zrdj.java.filesearch.filesystem.attributes.NoFollowLinksFallback;
import com.github.zrdj.java.filesearch.iterator.CloseableIterator;
import com.github.zrdj.java.filesearch.iterator.path.DirectoryIterator;

import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;

public interface Directory extends FileEntry {
    CloseableIterator<Path> iterator();

    DirectoryStream<Path> open() throws IOException;

    final class Smart implements Directory {
        private final FileEntry fileEntry;

        public Smart(final FileEntry fileEntry) {
            this.fileEntry = fileEntry;
        }

        public Smart(final Path path) {
            this(
                    new FileEntry.Smart(path,
                            new Cached(
                                    new NoFollowLinksFallback(
                                            new FollowLinks(path)))));
        }

        @Override
        public Path path() {
            return fileEntry.path();
        }

        @Override
        public Attributes attributes() {
            return fileEntry.attributes();
        }

        @Override
        public Object uniqueKey() {
            return fileEntry.uniqueKey();
        }

        @Override
        public boolean valid() {
            return fileEntry.valid();
        }

        @Override
        public boolean isFile() {
            return fileEntry.isFile();
        }

        @Override
        public boolean isDirectory() {
            return fileEntry.isDirectory();
        }


        @Override
        public DirectoryStream<Path> open() throws IOException {
            return Files.newDirectoryStream(fileEntry.path());
        }

        @Override
        public CloseableIterator<Path> iterator() {
            return new DirectoryIterator(this);
        }

        @Override
        public boolean equals(Object o) {
            return fileEntry.equals(o);
        }

        @Override
        public int hashCode() {
            return fileEntry.hashCode();
        }
    }
}
