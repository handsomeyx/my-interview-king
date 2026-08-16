package com.ikm.codeexec.service;

import com.ikm.codeexec.dto.RunResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.concurrent.TimeUnit;

/**
 * 本地执行器：容器/本机内 javac + java 跑用户 Java 代码。
 * 资源限制：wall-time 超时杀进程 + -Xmx 内存上限。
 */
@Service
public class LocalExecutor {

    @Value("${app.local.timeout-seconds:5}")
    private long timeoutSeconds;
    @Value("${app.local.memory-mb:256}")
    private int memoryMb;

    public RunResponse execute(String code, String stdin) {
        Path dir = null;
        try {
            dir = Files.createTempDirectory("ikm-exec-");
            Path javaFile = dir.resolve("Main.java");
            Files.writeString(javaFile, code);

            // 1. 编译
            ProcessBuilder pbC = new ProcessBuilder("javac", javaFile.toString());
            pbC.redirectErrorStream(true);
            Process javac = pbC.start();
            boolean cDone = javac.waitFor(timeoutSeconds, TimeUnit.SECONDS);
            if (!cDone) {
                javac.destroyForcibly();
                return verdict("TLE", "", "编译超时（>" + timeoutSeconds + "s）", -1);
            }
            String compileOut = readAll(javac.getInputStream());
            if (javac.exitValue() != 0) {
                return verdict("CE", "", compileOut, javac.exitValue());
            }

            // 2. 运行
            ProcessBuilder pbR = new ProcessBuilder(
                    "java", "-Xmx" + memoryMb + "m", "-cp", dir.toString(), "Main");
            Process javaProc = pbR.start();
            if (stdin != null && !stdin.isEmpty()) {
                javaProc.getOutputStream().write(stdin.getBytes(StandardCharsets.UTF_8));
            }
            javaProc.getOutputStream().close();
            long start = System.currentTimeMillis();
            boolean done = javaProc.waitFor(timeoutSeconds, TimeUnit.SECONDS);
            long elapsed = System.currentTimeMillis() - start;
            if (!done) {
                javaProc.destroyForcibly();
                return verdict("TLE", "", "运行超时（>" + timeoutSeconds + "s）", -1);
            }
            String stdout = readAll(javaProc.getInputStream());
            String stderr = readAll(javaProc.getErrorStream());
            RunResponse r = new RunResponse();
            r.setStdout(stdout);
            r.setStderr(stderr);
            r.setExitCode(javaProc.exitValue());
            r.setVerdict(javaProc.exitValue() == 0 ? "OK" : "RE");
            r.setTimeMs(elapsed);
            r.setMemoryKb(0);
            return r;
        } catch (Exception e) {
            return verdict("RE", "", "执行异常: " + e.getMessage(), -1);
        } finally {
            if (dir != null) cleanup(dir);
        }
    }

    private RunResponse verdict(String v, String stdout, String stderr, int exit) {
        RunResponse r = new RunResponse();
        r.setStdout(stdout);
        r.setStderr(stderr);
        r.setExitCode(exit);
        r.setVerdict(v);
        return r;
    }

    private String readAll(InputStream is) throws IOException {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        byte[] buf = new byte[4096];
        int n;
        while ((n = is.read(buf)) != -1) bos.write(buf, 0, n);
        return bos.toString(StandardCharsets.UTF_8);
    }

    private void cleanup(Path dir) {
        if (dir == null) return;
        try (var stream = Files.walk(dir)) {
            stream.sorted((a, b) -> b.compareTo(a))
                    .forEach(p -> {
                        try { Files.deleteIfExists(p); } catch (IOException ignored) {}
                    });
        } catch (IOException ignored) {}
    }
}
