# Airflow Configs
AIRFLOW_SERVER = "127.0.0.1"
AIRFLOW_USER = "airflow"
AIRFLOW_PASSWD = "airflow"
AIRFLOW_DAG_DIR = "/Users/arvind.rapaka/venvs/airflow-2.6.2/airflow/dags"
AIRFLOW_REST_API_SERVER = "http://127.0.0.14:8080/api/v1"
AIRFLOW_DAG_DEPLOY_DIR = "/Users/arvind.rapaka/venvs/airflow-2.6.2/airflow/dagfiles/accounts"

# Deploy Directory Configs
SSH_CERTIFICATE = "/Users/arvind.rapaka/.ssh/id_rsa"
SSH_SERVER = "127.0.0.1"
SSH_USER = "arvind.rapaka"
DEPLOY_DIR = "/Users/arvind.rapaka/venvs/airflow-2.6.2/airflow/dagfiles/accounts"

# Jobs directory. This directory is where template dag files are found.
JOB_DIR = "/jobs/"
TEMP_DIR = "/tmp/dag"

# config = JOBS[data["jobname"]] + "/dag_template/" + data["jobname"] + "_template"
JOB_DAG_CONFIG_PATH = {
    "social_videos": "/Users/arvind.rapaka/git/cartup-ml-apis/social_videos/dag_template/social_videos_template",
    "widget_stats_report": ""
}

# A new way to configure jobs
replace_conf_params = {"SEARCH_LIBS": "/opt/airflow/dagfiles/dashboard-libs",
                       "ML_LIBS": "/opt/airflow/dagfiles/dashboard-libs",
                       "DASHBOARD_LIB": "/opt/airflow/dagfiles/dashboard-libs",
                       "EMBEDDING_LIB_DIR": "/opt/airflow/dagfiles/dashboard-libs",
                       "SOCIAL_LIB_DIR": "/Users/arvind.rapaka/git/cartup-ml-apis/social_videos",
                       "JOB_DIR": "/opt/airflow/dagfiles/dashboard-libs"}
JOB_API = "http://localhost:5003/api/v1/jobs"
