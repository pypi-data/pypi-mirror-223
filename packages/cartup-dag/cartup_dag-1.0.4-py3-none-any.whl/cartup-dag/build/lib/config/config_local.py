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

# Replace Parameters

SEARCH_LIBS = ""
ML_LIBS = ""
DASHBOARD_LIB = "/opt/airflow/dagfiles/dashboard-libs"
EMBEDDING_LIBS_DIR = "/Users/arvind.rapaka/git/cartup-ml-apis/social-videos"
JOB_EXTRA_PARAMS = {
    "embedding_features": "/opt/airflow/dagfiles/EMBEDDING_FEATURES"
}

replace_conf_params = {"SEARCH_LIBS": SEARCH_LIBS,
                       "ML_LIBS": ML_LIBS,
                       "DASHBOARD_LIB": DASHBOARD_LIB,
                       "EMBEDDING_LIB_DIR": EMBEDDING_LIBS_DIR,
                       "EMBEDDING_"
                       "JOB_DIR": JOB_DIR}
JOB_API = "http://localhost:5003/api/v1/jobs"
