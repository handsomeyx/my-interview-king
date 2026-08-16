package com.ikm.codeexec.service;

import com.ikm.codeexec.config.Judge0Props;
import com.ikm.codeexec.dto.Judge0Request;
import com.ikm.codeexec.dto.Judge0Response;
import com.ikm.common.exception.ApiException;
import com.ikm.common.api.ErrorCode;
import org.springframework.stereotype.Service;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Service
public class Judge0Service {

    private final RestTemplate restTemplate;
    private final Judge0Props props;

    public Judge0Service(RestTemplate judge0RestTemplate, Judge0Props props) {
        this.restTemplate = judge0RestTemplate;
        this.props = props;
    }

    public Judge0Response execute(String languageKey, String code, String stdin) {
        Judge0Props.Language lang = props.getLanguages().get(languageKey);
        if (lang == null) {
            throw new ApiException(ErrorCode.BAD_REQUEST, "不支持的语言: " + languageKey);
        }
        Judge0Request req = new Judge0Request(
                lang.getId(),
                code,
                stdin == null ? "" : stdin,
                props.getCpuTimeLimit(),
                props.getWallTimeLimit(),
                props.getMemoryLimit(),
                props.getMaxProcesses()
        );
        String url = props.getBaseUrl() + "/submissions?base64_encoded=false&wait=true";
        try {
            return restTemplate.postForObject(url, req, Judge0Response.class);
        } catch (ResourceAccessException e) {
            throw new ApiException(ErrorCode.GATEWAY_TIMEOUT, "执行服务响应超时");
        } catch (RestClientException e) {
            throw new ApiException(ErrorCode.SERVICE_UNAVAILABLE, "执行服务暂不可用: " + e.getMessage());
        }
    }
}
