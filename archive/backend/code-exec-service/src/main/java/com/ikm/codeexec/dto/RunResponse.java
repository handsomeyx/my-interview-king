package com.ikm.codeexec.dto;

public class RunResponse {
    private String stdout;
    private String stderr;
    private int exitCode;
    private String verdict;     // OK | TLE | MLE | RE | CE
    private long timeMs;
    private long memoryKb;

    public String getStdout() { return stdout; }
    public void setStdout(String stdout) { this.stdout = stdout; }
    public String getStderr() { return stderr; }
    public void setStderr(String stderr) { this.stderr = stderr; }
    public int getExitCode() { return exitCode; }
    public void setExitCode(int exitCode) { this.exitCode = exitCode; }
    public String getVerdict() { return verdict; }
    public void setVerdict(String verdict) { this.verdict = verdict; }
    public long getTimeMs() { return timeMs; }
    public void setTimeMs(long timeMs) { this.timeMs = timeMs; }
    public long getMemoryKb() { return memoryKb; }
    public void setMemoryKb(long memoryKb) { this.memoryKb = memoryKb; }
}
