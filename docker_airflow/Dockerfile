# Airflow Dockerfile
FROM puckel/docker-airflow

USER root
RUN apt-get update && apt-get install -y procps
USER airflow
COPY ./airflow.cfg /usr/local/airflow/airflow.cfg

VOLUME ["/usr/local/airflow/dags"]
