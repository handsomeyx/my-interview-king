# 多阶段构建：本机无需装 Maven，容器内编译
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
COPY settings.xml /root/.m2/settings.xml
COPY pom.xml .
COPY common/pom.xml common/pom.xml
COPY gateway/pom.xml gateway/pom.xml
COPY code-exec-service/pom.xml code-exec-service/pom.xml
COPY common/src common/src
COPY gateway/src gateway/src
RUN mvn -B -s /root/.m2/settings.xml clean package -pl gateway -am -DskipTests

FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=builder /build/gateway/target/gateway.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
