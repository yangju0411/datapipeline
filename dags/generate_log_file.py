import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

dag = DAG(
    dag_id = "generate_log_file",
    start_date = airflow.utils.dates.days_ago(3),
    schedule_interval = "@daily"
)

def _generate_file(start, end, inc, prmt, path, filename):
    from library.log_generator import generate_file
    generate_file(start, end, inc, prmt, path, filename)

generate_logs = PythonOperator(
    task_id = "generate_logs",
    python_callable = _generate_file,
    op_kwargs={
        "start" : "{{ds}} 00:00:00",
        "end" : "{{ds}} 23:59:59",
        "inc" : 1,
        "prmt" : 3000,
        "path" : "/tmp/access_log/",
        "filename": "{{ds_nodash}}.log",
        },
    dag = dag,
)

notify = BashOperator(
    task_id = "notify",
    bash_command = 'echo "$(ls /tmp/access_log/)"',
    dag = dag,
)

generate_logs >> notify