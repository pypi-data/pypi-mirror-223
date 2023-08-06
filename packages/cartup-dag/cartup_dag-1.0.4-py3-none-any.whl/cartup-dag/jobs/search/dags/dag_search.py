from datetime import datetime, timedelta
import os
import logging
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator


# Require Params
DAG_NAME = "{{$DAG_NAME}}"
LIB_DIR = "{{$DASHBOARD_LIB}}"
SCHEDULE_INTERVAL = "{{$SCHEDULE_INTERVAL}}"
DEPLOY_DIR = "{{$DEPLOY_DIR}}"


BASH_DASHBOARD_COMMAND = "python3 " + LIB_DIR + os.sep +"dashboard_dag.py " + DEPLOY_DIR + os.sep +"config-dashboard.prop-dashboard.prop"

one_day_ago = datetime.combine(datetime.today() - timedelta(1),
                                  datetime.min.time())


args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': one_day_ago,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#Define the DAG
dag = DAG(
    dag_id=DAG_NAME, default_args=args,
    schedule_interval=SCHEDULE_INTERVAL,
    dagrun_timeout=timedelta(minutes=60))

logging.info("Command Running : " +  BASH_DASHBOARD_COMMAND)

dashboard_task = BashOperator(
    task_id='dashboard_task',
    bash_command=BASH_DASHBOARD_COMMAND,
    dag=dag)

if __name__ == "__main__":
    dag.cli()