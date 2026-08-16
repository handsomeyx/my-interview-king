package com.ikm.codeexec;

import com.ikm.codeexec.config.Judge0Props;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@SpringBootApplication
@EnableConfigurationProperties(Judge0Props.class)
public class CodeExecApplication {
    public static void main(String[] args) {
        SpringApplication.run(CodeExecApplication.class, args);
    }
}
