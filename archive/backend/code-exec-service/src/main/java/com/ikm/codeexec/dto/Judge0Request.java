package com.ikm.codeexec.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * 发给 Judge0 的 submission 请求体。字段名按 Judge0 文档（下划线）。
 */
public record Judge0Request(
        @JsonProperty("language_id") int languageId,
        @JsonProperty("source_code") String sourceCode,
        @JsonProperty("stdin") String stdin,
        @JsonProperty("cpu_time_limit") int cpuTimeLimit,
        @JsonProperty("wall_time_limit") int wallTimeLimit,
        @JsonProperty("memory_limit") int memoryLimit,
        @JsonProperty("max_processes_and_or_threads") int maxProcessesAndOrThreads
) {}
