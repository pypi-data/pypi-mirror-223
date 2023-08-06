import json
import re
import traceback

import boto3
import requests
from botocore.exceptions import ClientError
from cartup_dag.config.config_notification import s3_config
from airflow import settings
from airflow.models import TaskInstance
from sys import platform
from cartup_dag.config import config as dag_config


def replace_line_with_regex(file_path, regex_pattern, new_value):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            file.close()

        # Use regex to find the line that matches the pattern
        updated_content = re.sub(regex_pattern, new_value, content)

        with open(file_path, 'w') as file:
            file.write(updated_content)
            file.close()

        print("Line replaced successfully.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def create_s3_bucket(bucket_name, client):
    try:
        client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{bucket_name}' already exists.")
        else:
            print(f"Error creating bucket '{bucket_name}': {e}")


def push_file_to_s3(bucket_name, file_path, s3_key):
    try:
        session = boto3.session.Session()
        client = session.client('s3',
                                region_name=s3_config["region"],
                                endpoint_url=s3_config["endpoint_url"],
                                aws_access_key_id=s3_config["ACCESS_ID"],
                                aws_secret_access_key=s3_config["SECRET_KEY"])

        # Check if the bucket exists, if not, create it
        response = client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        if bucket_name not in buckets:
            create_s3_bucket(bucket_name, client)

        # Upload the file to S3
        with open(file_path, 'rb') as file:
            client.upload_fileobj(file, bucket_name, s3_key)

        print("File successfully uploaded to S3.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def update_dag_job_status(**kwargs):
    try:
        """Pull all previously pushed XComs and check if the pushed values match the pulled values."""
        ti = kwargs['ti']
        CONF_DEPLOY_DIR = kwargs['config_dir']
        config = kwargs['config']
        DAG_NAME = kwargs['DAG_NAME']

        with open(CONF_DEPLOY_DIR + "/config/config.py", 'r') as file:
            conf_params = file.read()

        session = settings.Session()
        task_info = []
        for task in session.query(TaskInstance) \
                .filter(TaskInstance.run_id == kwargs['dag_run'].run_id).all():
            task = {
                "task_id": task.task_id,
                "dag_id": task.dag_id,
                "start_date": str(task.start_date),
                "hostname": task.hostname,
                "unixname": task.unixname,
                "job_id": task.job_id,
                "pid": task.pid
            }
            task_info.append(task)

        payload_data = {
            "storeid": config.c_org_s,
            "account_id": config.c_org_id,
            "job_name": DAG_NAME,
            "job_config": json.dumps({"config": conf_params}),
            "tasks": []
        }

        print(json.dumps(task_info))

        for task in task_info:
            if task["task_id"] == "update_dag_job":
                continue
            job_status = ti.xcom_pull(key='job_params', task_ids='run_video_search_job')
            task["status"] = job_status[task["task_id"]]["status"]
            task["message"] = job_status[task["task_id"]]["msg"]
            task["error_message"] = job_status[task["task_id"]]["msg"]
            payload_data["tasks"].append(task)

        print(json.dumps(payload_data))
        print(dag_config.JOB_STATUS_API)

        if platform != "darwin":
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            requests.post(dag_config.JOB_STATUS_API, json=json.dumps(payload_data), headers=headers)
        return
    except:
        traceback.print_exc()


if __name__ == '__main__':
    # Example usage
    bucket_name = 'cartup-demo-test'  # Replace this with the name of your S3 bucket
    file_path = '/tmp/dag/demo/social_videos/config/config.py'  # Replace this with the path to your file
    s3_key = 'dag/demo/social_videos/config/config.py'  # Replace this with the destination key (S3 object key)
    push_file_to_s3(bucket_name, file_path, s3_key)
    # replace_line_with_regex("/tmp/dag/demo/social_videos/config/config.py", "last_update_time *?=.*",
    #                        "last_update_time=\"1 TO 2\"")
