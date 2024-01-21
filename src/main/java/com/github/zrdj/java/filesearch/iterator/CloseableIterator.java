package com.github.zrdj.java.filesearch.iterator;

import java.io.Closeable;
import java.util.Iterator;

public interface CloseableIterator<T> extends Iterator<T>, Closeable {
}
