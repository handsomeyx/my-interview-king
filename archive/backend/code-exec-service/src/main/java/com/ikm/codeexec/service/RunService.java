package com.ikm.codeexec.service;

import com.ikm.codeexec.dto.RunRequest;
import com.ikm.codeexec.dto.RunResponse;
import com.ikm.common.exception.ApiException;
import com.ikm.common.api.ErrorCode;
import org.springframework.stereotype.Service;

@Service
public class RunService {

    private static final int CODE_MAX_BYTES = 16 * 1024;       // D6: 16KB
    private static final int STDIN_MAX_BYTES = 1024 * 1024;    // 1MB

    private final LocalExecutor localExecutor;

    public RunService(LocalExecutor localExecutor) {
        this.localExecutor = localExecutor;
    }

    public RunResponse run(RunRequest req) {
        validate(req);
        if (!"java".equals(req.getLanguage())) {
            throw new ApiException(ErrorCode.BAD_REQUEST, "阶段1 仅支持 Java");
        }
        return localExecutor.execute(req.getCode(), req.getStdin());
    }

    private void validate(RunRequest req) {
        if (req.getCode() == null || req.getCode().isEmpty()) {
            throw new ApiException(ErrorCode.BAD_REQUEST, "代码不能为空");
        }
        if (req.getCode().length() > CODE_MAX_BYTES) {
            throw new ApiException(ErrorCode.PAYLOAD_TOO_LARGE, "代码过长，上限 16KB");
        }
        if (req.getStdin() != null && req.getStdin().length() > STDIN_MAX_BYTES) {
            throw new ApiException(ErrorCode.PAYLOAD_TOO_LARGE, "输入过长，上限 1MB");
        }
    }
}
