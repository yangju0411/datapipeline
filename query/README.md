# Redshift 

![erd](/attached/erd.png)
ETL 과정의 코드와 DW 설계는 [ETL_DW](https://github.com/yangju0411/etl_dw) 프로젝트에 기반합니다.

PostgreSQL에서 AWS Redshift로 데이터 웨어하우스를 변경하면서 여러 변경사항이 생겼습니다.

## 변경사항
- 인코딩 추가
    - 열 지향 데이터베이스인 redshift는 각 컬럼의 압축을 지원합니다. 이에 따라 각 컬럼에 맞는 인코딩 방식을 선택했습니다. 예를 들면 os 테이블의 name은 클라이언트가 접속할 때 사용한 기기의 os를 나타내는데 가짓수가 적어 byte dictionary 방식을 사용하면 효율적입니다.
    - 마찬가지로 time 테이블의 time_key는 본래 varchar 타입이었는데 redshift에서는 delta 인코딩으로 효율적인 시간 인코딩이 가능하여 timestamp로 데이터 타입을 변경하였습니다.
- distkey 추가
    - 단일 노드였던 PostgreSQL과 달리 MPP 데이터베이스인 Redshift는 여러 개의 노드가 클러스터를 이룹니다. 단일 노드에 많은 양의 데이터가 저장되면 분산 처리의 의의가 사라지고 성능이 저하되므로 distkey를 설정하여 데이터가 분산 저장할 수 있게 해줍니다.
    - distkey 선택 방식은 AWS 공식 문서의 가이드를 따라 설정하였습니다.
        - 카디널리티가 높은 컬럼을 선택한다. 그래야 골고루 분산됨
        - 팩트 테이블은 distkey가 1개로 제한되는데 함께 배치할 디멘션 테이블을 하나 선택해준다. 두 외래키 모두 distkey로 지정한다. 카디널리티가 가장 높은 time을 지정했습니다. 
- sortkey 추가
    - RDB의 인덱스와 달리 Redshift는 sortkey를 지정하여 읽어야 할 데이터를 줄여 성능을 높힐 수 있습니다.
    - sortkey 선택 방식은 AWS 공식 문서의 가이드를 따라 설정하였습니다.
        - 자주 테이블을 조인할 경우 외래키를 sortkey로 지정한다. 그러면 쿼리 최적화 프로그램이 느린 해시 조인 대신 정렬 병합 조인을 선택할 수 있어 성능이 향상된다. 