package com.ikm.common.api;

public enum ErrorCode {
    BAD_REQUEST("BAD_REQUEST", 400, "请求参数错误"),
    PAYLOAD_TOO_LARGE("PAYLOAD_TOO_LARGE", 413, "请求体过大"),
    UNAUTHORIZED("UNAUTHORIZED", 401, "未授权"),
    FORBIDDEN("FORBIDDEN", 403, "无访问权限"),
    NOT_FOUND("NOT_FOUND", 404, "资源不存在"),
    RATE_LIMITED("RATE_LIMITED", 429, "请求过于频繁，请稍后再试"),
    BAD_GATEWAY("BAD_GATEWAY", 502, "上游响应异常"),
    SERVICE_UNAVAILABLE("SERVICE_UNAVAILABLE", 503, "服务暂不可用"),
    GATEWAY_TIMEOUT("GATEWAY_TIMEOUT", 504, "上游响应超时"),
    INTERNAL_ERROR("INTERNAL_ERROR", 500, "服务器内部错误");

    private final String code;
    private final int httpStatus;
    private final String defaultMessage;

    ErrorCode(String code, int httpStatus, String defaultMessage) {
        this.code = code;
        this.httpStatus = httpStatus;
        this.defaultMessage = defaultMessage;
    }

    public String getCode() {
        return code;
    }

    public int getHttpStatus() {
        return httpStatus;
    }

    public String getDefaultMessage() {
        return defaultMessage;
    }
}
