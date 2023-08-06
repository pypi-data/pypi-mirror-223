from flask import Flask, request, Response
from flask_cors import CORS
from config.config import *
import logging
import traceback
import json
import os
from ssh.ssh_client import SSHClient
import shutil
from pathlib import Path
from airflow.airflow_service import AirflowService
import re
import copy
import uuid


app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

ssh_client = SSHClient()
airflow_client = AirflowService()

codes = {
    "CARTUP_200": "DAG setup successful",
    "CARTUP_401": "DAG setup failed",
    "CARTUP_402": "DAG File missing",
    "CARTUP_403": "DAG SSH failed",
    "CARTUP_404": "DAG setup Failed; Unknown error",
}

HTTP_METHODS = ['GET', 'POST']
HTTP_AIRFLOW_METHODS = ['GET', 'POST', 'DELETE', 'PATCH']


def send_error_response(msg):
    response = Response(msg, 400)
    return response


def send_response(msg):
    msg['status'] = "SUCCESS"
    response = Response(json.dumps(msg), 200)
    return response


def check_if_param_exist(params, args):
    for param in params:
        if param not in args:
            return False
    return True


def get_pattern_replace(data, replace_c_params):
    pattern = re.compile(r'(\{\{\$(.+?)\}\})')
    rep_str = copy.copy(data)
    for rep, key in re.findall(pattern, data):
        if key.upper() in replace_c_params:
            rep_str = rep_str.replace(rep, str(replace_c_params[key.upper()]))
    return rep_str


def write_close_file(file_path, params):
    fin = open(file_path, "rt")
    data = fin.read()
    data = get_pattern_replace(data, params)
    fin.close()
    fin = open(file_path, "wt")
    fin.write(data)
    fin.close()


def replace_params(replace_c_params, location):
    for path, currentDirectory, files in os.walk(location):
        for file in files:
            if re.match(".*swp", file):
                continue
            file_path = os.path.join(path, file)
            write_close_file(file_path, replace_c_params)


def find_a_file(path_dir, prefix):
    dag_files = []
    for path in Path(path_dir).rglob(prefix + '*'):
        dag_files.append(os.path.abspath(path))
    return dag_files


@app.route('/setjob', methods=['POST'])
def set_job():
    try:
        params = ["org_s", "jobname"]
        data = request.get_json()
        # Checking for mandatory parameters
        if not check_if_param_exist(params, data):
            return send_error_response(codes['CARTUP_406'])
        jobdir_path = JOB_DIR + "/" + data['jobname']

        if not os.path.isdir(jobdir_path):
            if data["jobname"] in JOB_DAG_CONFIG_PATH:
                jobdir_path = JOB_DAG_CONFIG_PATH[data["jobname"]]
                if not os.path.isdir(jobdir_path):
                    raise Exception("Job Name doesn't exist ...")
            else:
                raise Exception("Job Name doesn't exist ...")

        # Create a local temp directory
        tmp_dir = TEMP_DIR + "/" + data['org_s'] + "/" + data['jobname']
        shutil.copytree(jobdir_path, tmp_dir, dirs_exist_ok=True)

        # Make sure Dag files exists
        dag_files = find_a_file(tmp_dir, "dag_")
        if len(dag_files) == 0:
            raise Exception("Dag file missing {}".format(data['org_s']))

        # building replace parameters
        replace_conf_args_copy = copy.deepcopy(replace_conf_params)
        remote_dir = DEPLOY_DIR + "/" + data['org_s']
        replace_conf_args_copy['AIRFLOW_DEPLOY_DIR'] = AIRFLOW_DAG_DEPLOY_DIR + "/" + data['org_s']

        for k, v in data.items():
            replace_conf_args_copy[k] = v

        #Conf Dir
        replace_conf_args_copy = dict((k.upper(), v) for k, v in replace_conf_args_copy.items())
        replace_conf_args_copy['CONF_DEPLOY_DIR'] = AIRFLOW_DAG_DEPLOY_DIR + "/" + data['org_s'] + "/" + data[
            "jobname"] + "/config"
        replace_params(replace_conf_args_copy, tmp_dir)


        # Now SSH the conf and DAG files
        ssh_client.make_remote_dir(remote_dir)
        ssh_client.export_file_directory(remote_dir, tmp_dir)

        # Push the DAG files to remote AIRFLOW DAG Folder
        for dag_file in dag_files:
            head, tail = os.path.split(dag_file)
            dag_id = data['org_s'] + "_" + tail.rsplit(".", 1)[0]
            replace_dag_id = {'DAG_NAME':  dag_id}
            write_close_file(dag_file, replace_dag_id)
            n_dag_file = head + "/" + data['org_s'] + "_" + tail
            os.rename(dag_file, n_dag_file)
            ssh_client.export_file_directory(AIRFLOW_DAG_DIR, n_dag_file, recursive=False)
            uu_id = str(uuid.uuid4())
            resp, flag = ("success", True)
            resp, flag = airflow_client.run_airflow_cmd(cmd='trigger_dag_run', replace_params={'dag_id': dag_id},
                                            data=json.dumps({"conf": {}, "dag_run_id": uu_id}))
            if not flag:
                logging.error("Not able to trigger the job {} {}".format(n_dag_file, uu_id))
            else:
                logging.info(resp.text)

    except Exception as e:
        logging.error(traceback.print_exc())
        send_error_response("{} : {}".format(codes['CARTUP_404'],
                                             traceback.print_exc()))
    return send_response({'message': codes['CARTUP_200']})


@app.route('/airflow_cmd', methods=HTTP_AIRFLOW_METHODS)
def trigger_dag():
    args = request.args
    cmd, params, data, req_params = None
    if 'cmd' in args:
        cmd = args['cmd']
    if 'params' in args:
        params = json.loads(args['params'])
    if data in args:
        data = args['data']
    if req_params in args:
        req_params = json.loads(args['req_params'])

    resp, flag = airflow_client.run_airflow_cmd(cmd=cmd, params=params,
                                                data=data, req_params=req_params)
    if not flag:
        send_error_response(resp)
    return send_response(resp)


def start_server():
    app.run(debug=True, threaded=True, port=5003)
    return app


if __name__ == '__main__':
    start_server()
