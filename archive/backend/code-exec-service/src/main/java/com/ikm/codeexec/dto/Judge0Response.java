package com.ikm.codeexec.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * Judge0 返回的 submission 结果。仅取我们关心的字段。
 */
public record Judge0Response(
        String stdout,
        String stderr,
        @JsonProperty("exit_code") Integer exitCode,
        String time,            // 秒，字符串如 "0.12"
        String memory,          // KB，字符串如 "24576"
        Status status,
        @JsonProperty("compile_output") String compileOutput,
        String message
) {
    public record Status(Integer id, String description) {}
}
