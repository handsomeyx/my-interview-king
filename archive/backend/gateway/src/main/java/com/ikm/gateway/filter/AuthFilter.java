package com.ikm.gateway.filter;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

/**
 * 鉴权全局过滤器。
 * 阶段1：app.auth.enabled=false 直接放行。
 * 阶段2：置 true 后接入 JWT 验签、解析 userId 写入 X-User-Id 透传下游。
 */
@Component
public class AuthFilter implements GlobalFilter, Ordered {

    @Value("${app.auth.enabled:false}")
    private boolean authEnabled;

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        if (!authEnabled) {
            return chain.filter(exchange);
        }
        // TODO 阶段2：从 Authorization header 解析 JWT → 验签 → exchange.mutate().request(...).header("X-User-Id", uid)
        return chain.filter(exchange);
    }

    @Override
    public int getOrder() {
        return -100;
    }
}
