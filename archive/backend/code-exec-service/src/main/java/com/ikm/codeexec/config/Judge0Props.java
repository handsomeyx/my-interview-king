package com.ikm.codeexec.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.Map;

@ConfigurationProperties(prefix = "app.judge0")
public class Judge0Props {
    private String baseUrl;
    private long waitTimeoutSeconds;
    private int cpuTimeLimit;
    private int wallTimeLimit;
    private int memoryLimit;
    private int maxProcesses;
    private Map<String, Language> languages;

    public String getBaseUrl() { return baseUrl; }
    public void setBaseUrl(String baseUrl) { this.baseUrl = baseUrl; }
    public long getWaitTimeoutSeconds() { return waitTimeoutSeconds; }
    public void setWaitTimeoutSeconds(long waitTimeoutSeconds) { this.waitTimeoutSeconds = waitTimeoutSeconds; }
    public int getCpuTimeLimit() { return cpuTimeLimit; }
    public void setCpuTimeLimit(int cpuTimeLimit) { this.cpuTimeLimit = cpuTimeLimit; }
    public int getWallTimeLimit() { return wallTimeLimit; }
    public void setWallTimeLimit(int wallTimeLimit) { this.wallTimeLimit = wallTimeLimit; }
    public int getMemoryLimit() { return memoryLimit; }
    public void setMemoryLimit(int memoryLimit) { this.memoryLimit = memoryLimit; }
    public int getMaxProcesses() { return maxProcesses; }
    public void setMaxProcesses(int maxProcesses) { this.maxProcesses = maxProcesses; }
    public Map<String, Language> getLanguages() { return languages; }
    public void setLanguages(Map<String, Language> languages) { this.languages = languages; }

    public static class Language {
        private int id;
        private String version;
        private String file;

        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
        public String getVersion() { return version; }
        public void setVersion(String version) { this.version = version; }
        public String getFile() { return file; }
        public void setFile(String file) { this.file = file; }
    }
}
