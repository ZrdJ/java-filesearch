package com.github.zrdj.java.filesearch.iterator.file;

import com.github.zrdj.java.filesearch.iterator.empty.EmptyIterator;

import java.io.File;
import java.util.Arrays;
import java.util.Iterator;

public class DirectoryIterator implements Iterator<File> {
    private final Iterator<File> iterator;

    public DirectoryIterator(final File directory) {
        if (directory.listFiles() == null)
            this.iterator = new EmptyIterator<>();
        else
            this.iterator = Arrays.asList(directory.listFiles()).iterator();
    }

    @Override
    public boolean hasNext() {
        return iterator.hasNext();
    }

    @Override
    public File next() {
        return iterator.next();
    }
}
