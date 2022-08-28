import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.hooks.S3_hook import S3Hook

dag = DAG(
    dag_id = "load_to_datalake",
    start_date = airflow.utils.dates.days_ago(3),
    schedule_interval = "@daily"
)

def _generate_file(start, end, inc, prmt, path, filename, **context):
    from library.log_generator import generate_file
    generate_file(start, end, inc, prmt, path, filename)
    context["ti"].xcom_push(key = "log_filename", value = filename)

generate_logs = PythonOperator(
    task_id = "generate_logs",
    python_callable = _generate_file,
    op_kwargs={
        "start" : "{{yesterday_ds}} 00:00:00",
        "end" : "{{yesterday_ds}} 23:59:59",
        "inc" : 1,
        "prmt" : 3000,
        "path" : "/tmp/access_log/",
        "filename": "{{yesterday_ds_nodash}}.log",
        },
    dag = dag,
)

def _load_to_s3(**context):
    hook = S3Hook(aws_conn_id = "datalake_s3")
    filename = context["ti"].xcom_pull(key = "log_filename")
    hook.load_file(filename = "/tmp/access_log/" + filename, key = "access_log/" + filename,
     bucket_name = "yangju0411-datalake", replace = True)

load_to_s3 = PythonOperator(
    task_id = "load_to_s3",
    python_callable = _load_to_s3,
    dag = dag,
)
"""
remove_local = BashOperator(
    task_id = "remove_local",
    bash_command = "rm /tmp/access_log/{{task_instance.xcom_pull(key = 'log_filename')}}",
    dag = dag
)
"""
generate_logs >> load_to_s3 #>> remove_local