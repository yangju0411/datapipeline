# Airflow Dockerfile
FROM puckel/docker-airflow

RUN apt-get update && apt-get install -y procps
COPY ./airflow.cfg /usr/local/airflow/airflow.cfg
RUN airflow initdb