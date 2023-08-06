import requests
import json
payload_data = {
            "storeid": "demo8",
            "account_id": "123",
            "job_name": "DAG_NAME",
            "job_config": "parmas",
            "status": "status",
            "message": "msg",
            "error_message": "msg"
        }

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
requests.post("http://127.0.0.1:5003/api/v1/jobs", json=json.dumps(payload_data), headers=headers)