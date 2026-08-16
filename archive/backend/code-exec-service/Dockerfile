# 多阶段构建：本机无需装 Maven，容器内编译
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /build
COPY settings.xml /root/.m2/settings.xml
COPY pom.xml .
COPY common/pom.xml common/pom.xml
COPY code-exec-service/pom.xml code-exec-service/pom.xml
COPY gateway/pom.xml gateway/pom.xml
COPY common/src common/src
COPY code-exec-service/src code-exec-service/src
RUN mvn -B -s /root/.m2/settings.xml clean package -pl code-exec-service -am -DskipTests

FROM eclipse-temurin:17-jdk
WORKDIR /app
COPY --from=builder /build/code-exec-service/target/code-exec-service.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
