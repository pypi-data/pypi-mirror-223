import logging
from flask import Flask
import json

log = logging.getLogger('__file__')
app = Flask(__name__)


class ResponseMessage:
    """A plain object. Response Maessage handles all the reviews.
       :arg msg: Response message
    """

    def __init__(self, msg):
        self.msg = msg

    def response_in_json(self, error=False):
        """Create Response in json. The Rest API Get and remove an attribute by name. Like :meth:`dict.pop`.

            :param error: Default is false - it is set the status as FAIL. If set true - it is set the status to OK.
            :return: returns the app.response object
        """

        response = {}
        if error:
            response['status'] = 'FAIL'
            response['msg'] = self.msg
        else:
            response['status'] = 'OK'
            response['msg'] = self.msg

        return app.response_class(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )
