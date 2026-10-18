// The name javac would derive from the jar file name, "java.filesearch", lies in the java.*
// namespace the JDK reserves for platform modules, so the module names itself after its root package.
module com.github.zrdj.java.filesearch {
    exports com.github.zrdj.java.filesearch;
    exports com.github.zrdj.java.filesearch.filesystem;
    exports com.github.zrdj.java.filesearch.filesystem.attributes;
    exports com.github.zrdj.java.filesearch.iterator;
    exports com.github.zrdj.java.filesearch.iterator.empty;
    exports com.github.zrdj.java.filesearch.iterator.file;
    exports com.github.zrdj.java.filesearch.iterator.path;
}
