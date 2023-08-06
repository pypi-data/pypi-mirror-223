import requests
from cartup_dag.config.config import *
import json
import re
import copy
import traceback
import logging
import uuid

logging.basicConfig(level=logging.DEBUG)


class AirflowService:
    def __init__(self):
        self.dag_cmds = {
            "list_dags": ['GET', 'dags'],
            "update_dag": ['PATCH', 'dags'],
            "delete_dag": ['DELETE', 'dags/{{$dag_id}}'],
            "list_dag_runs": ['GET', 'dags/{{$dag_id}}/dagRuns'],
            "get_dag_run": ['GET', 'dags/{{$dag_id}}/dagRuns/{{$dag_run_id}}'],
            "trigger_dag_run": ['POST', 'dags/{{$dag_id}}/dagRuns'],
        }
        pass

    def get_pattern_replace(self, url, replace_params):
        pattern = re.compile(r'(\{\{\$(.+?)\}\})')
        repstr = copy.copy(url)
        for rep, key in re.findall(pattern, url):
            repstr = repstr.replace(rep, str(replace_params[key]))
        return repstr

    def run_airflow_cmd(self, cmd=None, params=None, replace_params=None, data=None, req_params=None):
        headers = {
            'content-type': 'application/json',
        }
        resp = None
        try:

            if cmd is not None and cmd in self.dag_cmds:
                cmd_params = self.dag_cmds[cmd]
            else:
                cmd_params = [req_params['method'], req_params['path']]

            if replace_params is not None:
                request_url = AIRFLOW_REST_API_SERVER + "/" + self.get_pattern_replace(cmd_params[1], replace_params)
            else:
                request_url = AIRFLOW_REST_API_SERVER + "/" + cmd_params[1]

            if cmd_params[0] == 'GET':
                resp = requests.get(request_url, headers=headers, params=params,
                                    auth=(AIRFLOW_USER, AIRFLOW_PASSWD))
            elif cmd_params[0] == 'POST':
                resp = requests.post(request_url, headers=headers, params=params,
                                     auth=(AIRFLOW_USER, AIRFLOW_PASSWD), data=data)
            elif cmd_params[0] == 'DELETE':
                resp = requests.delete(request_url, headers=headers, params=params,
                                       auth=(AIRFLOW_USER, AIRFLOW_PASSWD))
            elif cmd_params[0] == 'PATCH':
                resp = requests.patch(request_url, headers=headers, params=params, data=data,
                                      auth=(AIRFLOW_USER, AIRFLOW_PASSWD))
        except Exception as e:
            logging.error(traceback.print_exc())
            return "Error: DAG setup failed {}".format(traceback.print_exc()), False

        return resp, True


if __name__ == '__main__':
    af = AirflowService()
    uu_id = str(uuid.uuid4())
    resp, flag = af.run_airflow_cmd(cmd='trigger_dag_run', replace_params={'dag_id': 'example_bash_operator'},
                                    data=json.dumps({"conf": {}, "dag_run_id": uu_id}))
    print(resp.text)

    resp, flag = af.run_airflow_cmd(cmd='list_dag_runs', replace_params={'dag_id': 'example_bash_operator'})
    print(resp.text)

    resp, flag = af.run_airflow_cmd(cmd='list_dags', params={'dag_id_pattern': 'bash', 'only_active': True})
    print(resp.text)

    resp, flag = af.run_airflow_cmd(cmd='update_dag', params={'dag_id_pattern': 'bash', 'only_active': True},
                              data=json.dumps({'is_paused': False}))
    print(resp.text)

    resp, flag = af.run_airflow_cmd(cmd='get_dag_run', replace_params={'dag_id': 'example_bash_operator', 'dag_run_id': uu_id})
    print(resp.text)

    resp, flag = af.run_airflow_cmd(req_params={'method': 'GET', 'path': 'dags/{{$dag_id}}/dagRuns/{{$dag_run_id}}'},
                                    replace_params={'dag_id': 'example_bash_operator', 'dag_run_id': uu_id})
    print(resp.text)

