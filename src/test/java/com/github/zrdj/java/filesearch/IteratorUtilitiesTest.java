package com.github.zrdj.java.filesearch;

import com.github.zrdj.java.filesearch.iterator.CloseableIterator;
import com.github.zrdj.java.filesearch.iterator.RepeatableIterator;
import com.github.zrdj.java.filesearch.iterator.empty.EmptyIterator;
import org.junit.Test;

import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.concurrent.atomic.AtomicBoolean;

import static org.assertj.core.api.Assertions.assertThat;

public class IteratorUtilitiesTest {

    // [impl->req~iterator-utilities.repeatable-current~1]
    @Test
    public void testNoCurrentValueBeforeTheFirstNext() {
        final RepeatableIterator<String> repeatable =
                new RepeatableIterator.Smart<>(Arrays.asList("a", "b").iterator());

        assertThat(repeatable.hasCurrent()).isFalse();
    }

    // [impl->req~iterator-utilities.repeatable-current~1]
    @Test
    public void testCurrentMirrorsTheLastNext() {
        final RepeatableIterator<String> repeatable =
                new RepeatableIterator.Smart<>(Arrays.asList("a", "b").iterator());

        final String returned = repeatable.next();

        assertThat(repeatable.current()).isEqualTo(returned);
        assertThat(repeatable.hasCurrent()).isTrue();
    }

    // [impl->req~iterator-utilities.closeable-delegation~1]
    @Test
    public void testCloseDelegatesToTheWrappedCloseableIterator() throws IOException {
        final AtomicBoolean closed = new AtomicBoolean(false);
        final Iterator<String> delegate = Collections.singletonList("x").iterator();
        final CloseableIterator<String> wrapped = new CloseableIterator<String>() {
            @Override
            public void close() {
                closed.set(true);
            }

            @Override
            public boolean hasNext() {
                return delegate.hasNext();
            }

            @Override
            public String next() {
                return delegate.next();
            }
        };

        new RepeatableIterator.Closeable<>(wrapped).close();

        assertThat(closed.get()).isTrue();
    }

    // [impl->req~iterator-utilities.empty-iterator~1]
    @Test
    public void testHasNextIsAlwaysFalse() {
        assertThat(new EmptyIterator<String>().hasNext()).isFalse();
    }

    // [impl->req~iterator-utilities.empty-iterator~1]
    @Test
    public void testNextReturnsNullInsteadOfThrowing() {
        assertThat(new EmptyIterator<String>().next()).isNull();
    }
}
