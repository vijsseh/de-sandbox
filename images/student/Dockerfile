# syntax=docker/dockerfile:1

# ==========================================
# ЭТАП 1. Получение зависимостей Hadoop S3A
# ==========================================

FROM maven:3.9-eclipse-temurin-17 AS dependencies

WORKDIR /build

COPY spark/dependencies/pom.xml ./pom.xml

RUN --mount=type=cache,target=/root/.m2 \
    mvn -B dependency:copy-dependencies \
    -DoutputDirectory=/build/jars \
    -DincludeScope=runtime


# ==========================================
# ЭТАП 2. Студенческое окружение
# ==========================================

FROM quay.io/jupyter/pyspark-notebook:2026-07-28

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Добавляем S3A в Spark, установленный внутри Jupyter
COPY --from=dependencies /build/jars/hadoop-aws-3.5.0.jar /usr/local/spark/jars/
COPY --from=dependencies /build/jars/bundle-2.35.4.jar /usr/local/spark/jars/
COPY --from=dependencies /build/jars/analyticsaccelerator-s3-1.3.1.jar /usr/local/spark/jars/
COPY --from=dependencies /build/jars/wildfly-openssl-2.2.5.Final.jar /usr/local/spark/jars/
# Общие настройки Spark для студенческих контейнеров
COPY spark/config/spark-defaults.conf /usr/local/spark/conf/spark-defaults.conf

USER ${NB_UID}

RUN pip install --no-cache-dir \
    "jupyterhub==5.5.4" \
    boto3 \
    s3fs