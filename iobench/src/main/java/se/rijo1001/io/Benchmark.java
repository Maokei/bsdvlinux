package se.rijo1001.io;

import org.openjdk.jmh.annotations.*;

import java.io.File;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

/**
 * A class for benchmarking different Java IO techniques
 * on a simple file copying task.
 *
 * Run with jar file directly or with docker
 * <pre>
 *     mvn clean package
 *     java -jar target/benchmarks.jar
 * </pre>
 */

@Warmup(iterations=2, time=5, timeUnit=TimeUnit.SECONDS)
@Measurement(iterations=10, time=10, timeUnit=TimeUnit.SECONDS)
@Fork(1)
@Threads(1)
// calculate average time of one call
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Benchmark)

public class Benchmark {
    private File srcFile = new File("testfiles/input-1000KB.jpg");
    private File targetFile = new File("testfiles/output-1000KB.jpg");
    private long fileSize = srcFile.length();

    // this shows, how we can perform four measure groups: 1 KByte, 4 KByte, 16 KByte, 64 KByte
    @Param({"1024", "4096", "16384", "65536"})
    public int bufferSize;

    @org.openjdk.jmh.annotations.Benchmark
    public void copyFileUsingStreams() throws IOException {

        long bytesCopied = Util.copyFileUsingStreams(srcFile, targetFile, bufferSize);
        assert bytesCopied == fileSize;
    }

    @org.openjdk.jmh.annotations.Benchmark
    public void copyFileUsingBufferedStreams() throws IOException {

        long bytesCopied = Util.copyFileUsingBufferedStreams(srcFile, targetFile, bufferSize);
        assert bytesCopied == fileSize;
    }

    @org.openjdk.jmh.annotations.Benchmark
    public void copyFileUsingInChannelOutBufferedStream() throws IOException {

        long bytesCopied = Util.copyFileUsingInChannelOutBufferedStream(srcFile, targetFile, bufferSize);
        assert bytesCopied == fileSize;
    }

    @org.openjdk.jmh.annotations.Benchmark
    public void copyFileUsingChannelWithDirectByteBuffer() throws IOException {

        long bytesCopied = Util.copyFileUsingChannelWithDirectByteBuffer(srcFile, targetFile, bufferSize);
        assert bytesCopied == fileSize;
    }

    @org.openjdk.jmh.annotations.Benchmark
    public void copyFileUsingChannelTransferFrom() throws IOException {

        long bytesCopied = Util.copyFileUsingChannelTransferFrom(srcFile, targetFile);
        assert bytesCopied == fileSize;
    }

    @org.openjdk.jmh.annotations.Benchmark
    public void copyFileUsingChannelTransferTo() throws IOException {

        long bytesCopied = Util.copyFileUsingChannelTransferTo(srcFile, targetFile);
        assert bytesCopied == fileSize;
    }
}
