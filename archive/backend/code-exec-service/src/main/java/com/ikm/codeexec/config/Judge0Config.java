package com.ikm.codeexec.config;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

@Configuration
public class Judge0Config {

    @Bean
    public RestTemplate judge0RestTemplate(RestTemplateBuilder builder, Judge0Props props) {
        return builder
                .setConnectTimeout(Duration.ofSeconds(5))
                .setReadTimeout(Duration.ofSeconds(props.getWaitTimeoutSeconds() + 10))
                .build();
    }
}
