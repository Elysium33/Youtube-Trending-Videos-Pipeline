from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['yourmail@mail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries' : 1,
    'retry_delay': timedelta(minutes=5)
    }
    
    with DAG(
        'Youtube_Trending_Dag'
        start_date = datetime(2022, 25, 2),
        default_args = default_args,
        description = 'Youtube Trending Videos Pipeline',
        schedule_interval = '@daily',
        catchup = False
        ) as dag:
            t1 = BashOperator(
                task_id = 'ETLjob',
                bash_command = 'python3 [path/to/script/here]'
                )
     