# My Data Pipeline Project
데이터 파이프라인을 직접 구축해보는 프로젝트입니다.

날마다 갱신되는 웹 서버 액세스 로그를 가져오는 상황을 가정하고 데이터 파이프라인을 작성합니다.

회사에서 웹 서버를 운영 중이고 액세스 로그를 매일 다른 파일에 저장하게끔 관리한다고 가정합니다. 

## 데이터 소스
데이터 소스는 NASA에서 공개한 1995년 웹 액세스 로그를 사용합니다.
해당 데이터는 1995년 7월 한 달 간의 웹 액세스 로그를 저장해둔 것인데 이를 파이썬으로 한 번 처리하여 일자 별로 파일을 저장해둡니다.

원본 파일 링크: ftp://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html

[파일 처리 코드 링크](/log_data/separate_files_per_day.ipynb)

## Airflow
매번 쌓이는 로그를 실시간으로 처리하는 것이 아닌 데이터를 일괄 처리(batch processing)하는 작업이기 때문에 배치 작업에 적합한 워크플로우인 Airflow를 선택하였습니다. 

그리하여 Airflow를 통해 데이터 파이프라인의 워크플로우를 관리합니다. Airflow의 메타데이터 DB로는 PostgreSQL을 사용합니다. 기본적으로 SQLite를 사용할 수 있으나 SQLite는 Airflow의 SequentialExecutor 밖에 사용하지 못하기 때문에 태스크를 병렬로 실행하지 못하고 순차적으로 실행하여 속도가 느립니다. 그렇기 때문에 병렬 처리가 가능하며 단일 호스트 환경에서 권장되는 LocalExecutor를 사용하기 위해 Postgre를 채용하게 되었습니다.

**관련 디렉토리**
- [dags](/docker_airflow/dags/)
- [docker-airflow](/docker_airflow/)
- [docker-postgre](/docker_postgre/)

# References
참고하는 모든 유용한 링크들을 모아놓습니다.

## Data Pipeline
[Simple Data Pipeline Project](https://github.com/yansfil/grab-data-world)

## Airflow on Docker
[Apache 공식 문서 Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)

[AirFlow Manual on Docker](https://dorumugs.tistory.com/entry/AirFlow-Manual-on-Docker-stage-install)

[Airflow 시작하기](https://lsjsj92.tistory.com/631)

[Data Pipeline with Apache Airflow](https://github.com/K9Ns/data-pipelines-with-apache-airflow)