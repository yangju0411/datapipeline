set -e
psql -v --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER test with ENCRYPTED password 'test';
    CREATE DATABASE airflow;
    GRANT ALL PRIVILEGES ON DATABASE airflow TO test;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA PUBLIC TO test;
EOSQL