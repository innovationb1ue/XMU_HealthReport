import uuid
from concurrent.futures import ThreadPoolExecutor
from flask import request

from flask_restplus import Resource, fields

from . import api_rest
from ..Cores.DB_conn import DBConnector
from ..Cores.Parsers import apply_parser
from ..Cores.health_report_api import health_report
from ..Cores.login_logic import login_xmuxg
from ..CONFIG import *

Executor = ThreadPoolExecutor(max_workers=2)

apply_payload = api_rest.model('Payload', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'N': fields.Integer,
    'timed':fields.Boolean
})

conn = DBConnector(MONGODB_USER, MONGODB_PWD, MONGODB_DBNAME)


@api_rest.route('/report_result/<string:result_id>')
class ReportResult(Resource):
    def get(self, result_id:str):
        if not result_id or len(result_id) != 36:
            return {'message': 'Not valid id'}
        return {'message': "ok", 'result':conn.get_result(result_id)}


@api_rest.route('/apply')
class ReportApply(Resource):
    def get(self):
        return {'message': 'Only support POST method'}

    @api_rest.expect(apply_payload)
    def post(self) -> dict:
        args = apply_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        N = args.get('N')
        timed = args.get('timed')
        if not username or not password or not N:
            return {'message': 'Empty fields'}
        task_uuid = str(uuid.uuid4())
        Executor.submit(self.do_report, task_uuid, username, password, N, timed)
        return {'message': 'ok', 'uuid': task_uuid}

    @staticmethod
    def do_report(task_uuid:str, username, password, N, timed):
        conn.upsert_result(task_uuid, 'Proceeding, Need a moment.')
        s = login_xmuxg(username, password)
        if not s:
            conn.upsert_result(task_uuid, "Failed to login. ")
            return
        conn.upsert_account(username, password)
        if timed:
            conn.upsert_time_task(username, password)
        res = health_report(int(N), s)
        print(f'uuid: {task_uuid} \nres: {res}')
        conn.upsert_result(task_uuid, res)


@api_rest.route('/time_task_apply')
class TimeTask(Resource):
    def post(self):
        args = apply_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        if not username or not password:
            return {'message': "empty fields"}
        conn.upsert_time_task(username, password)


@api_rest.route('/time_task_delete')
class TimeTaskDelete(Resource):
    def post(self):
        args = apply_parser.parse_args()
        username = args.get('username')
        if not username:
            return {'message': 'empty fields'}
        conn.del_time_task(username)


@api_rest.route('/login')
class LoginMethod(Resource):
    def post(self):
        args = apply_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        login_status = login_xmuxg(username, password)
        if not login_status:
            return False
        else:
            return {'cookies':'cookies string'}






