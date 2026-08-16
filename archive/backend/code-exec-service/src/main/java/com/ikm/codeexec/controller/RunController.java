package com.ikm.codeexec.controller;

import com.ikm.codeexec.dto.RunRequest;
import com.ikm.codeexec.dto.RunResponse;
import com.ikm.codeexec.service.RunService;
import com.ikm.common.api.Result;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/run")
public class RunController {

    private final RunService runService;

    public RunController(RunService runService) {
        this.runService = runService;
    }

    @PostMapping
    public Result<RunResponse> run(@RequestBody RunRequest req) {
        return Result.ok(runService.run(req));
    }
}
