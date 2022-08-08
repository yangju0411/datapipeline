import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator

from log_generator import generate_file

dag = DAG(
    dag_id = "generate_log_file",
    start_date = airflow.utils.dates.days_ago(3),
    schedule_interval = "@daily"
)

generate_logs = PythonOperator(
    task_id = "generate_logs",
    python_collable = generate_file,
    op_kwargs={
        "start" : "{{yesterday_ds}} 00:00:00",
        "end" : "{{yesterday_ds}} 23:59:59",
        "inc" : 10,
        "prmt" : 3000,
        #"path" : "/var/log/access/{{yesterday_ds_nodash}}.log",
        "path" : "/usr/local/airflow/dag/data/{{yesterday_ds_nodash}}.log",
        },
        dag = dag,
)

notify = BashOperator(
    task_id = "notify",
    bash_command = 'echo "There are now $(ls /usr/local/airflow/dag/data/ | wc - l) files."',
    dag = dag,
)

generate_logs >> notify