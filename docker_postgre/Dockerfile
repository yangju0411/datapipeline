# Postgre Dockerfile
FROM postgres:12.4
COPY ./init-user-db.sh /docker-entrypoint-initdb.d/init.sh

# 12는 postgre의 버젼
RUN pg_createcluster 12 main
RUN pg_ctlcluster 12 main start

COPY ./pg_hba.conf /etc/postgresql/12/main/pg_hba.conf
