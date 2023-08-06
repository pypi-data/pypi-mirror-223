# Airflow Configs
AIRFLOW_SERVER = "178.62.214.94"
AIRFLOW_USER = "airflow"
AIRFLOW_PASSWD = "airflow"
AIRFLOW_DAG_DIR = "/home/ubuntu/airflow-docker/dags"
AIRFLOW_REST_API_SERVER = "http://178.62.214.94:8080/api/v1"
AIRFLOW_DAG_DEPLOY_DIR = "/opt/airflow/dagfiles/accounts"

# Deploy Directory Configs
SSH_CERTIFICATE = "/Users/arvind.rapaka/.ssh/id_rsa"
SSH_SERVER = "178.62.214.94"
SSH_USER = "arvind.rapaka"
DEPLOY_DIR = "/home/ubuntu/airflow-docker/dagfiles/accounts"

# Jobs directory. This directory is where template dag files are found.
JOB_DIR = "/jobs/"
TEMP_DIR = "/tmp/dag"

# Replace Parameters
SEARCH_LIBS = ""
ML_LIBS = ""
DASHBOARD_LIB = "/opt/airflow/dagfiles/dashboard-libs"

JOB_EXTRA_PARAMS = {
    "embedding_features": "/opt/airflow/dagfiles/EMBEDDING_FEATURES"
}

replace_conf_params = {"SEARCH_LIBS": SEARCH_LIBS,
                       "ML_LIBS": ML_LIBS,
                       "DASHBOARD_LIB": DASHBOARD_LIB,
                       "JOB_DIR": JOB_DIR}
JOB_API = "http://localhost:5003/api/v1/jobs"
