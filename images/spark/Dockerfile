# syntax=docker/dockerfile:1

# ==========================================
# ЭТАП 1. Получаем Java-зависимости
# ==========================================

FROM maven:3.9-eclipse-temurin-17 AS dependencies

WORKDIR /build

COPY spark/dependencies/pom.xml ./pom.xml

RUN --mount=type=cache,target=/root/.m2 \
    mvn -B dependency:copy-dependencies \
    -DoutputDirectory=/build/jars \
    -DincludeScope=runtime \
    -U \
    -Dmaven.wagon.http.pool=false \
    -Dmaven.wagon.http.timeout=60000

# ==========================================
# ЭТАП 2. Собираем Spark с поддержкой S3A
# ==========================================

FROM apache/spark@sha256:fc64959c04bd87b0ac686be9aaa9008b69cdb1afc695400528279c8b01f43d89

USER root

# Копируем только необходимые зависимости.
# Не заменяем библиотеки Spark и Hadoop,
# которые уже есть в базовом образе.

COPY --from=dependencies /build/jars/hadoop-aws-3.5.0.jar /opt/spark/jars/
COPY --from=dependencies /build/jars/bundle-2.35.4.jar /opt/spark/jars/
COPY --from=dependencies /build/jars/analyticsaccelerator-s3-1.3.1.jar /opt/spark/jars/
COPY --from=dependencies /build/jars/wildfly-openssl-2.2.5.Final.jar /opt/spark/jars/

USER spark
