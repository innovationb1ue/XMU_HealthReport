import uuid
from concurrent.futures import ThreadPoolExecutor

from flask_restplus import Resource

from . import api_rest
from ..CONFIG import *
from ..Cores.DB_conn import DBConnector
from ..Cores.Parsers import apply_parser
from ..Cores.health_report_api import health_report
from ..Cores.login_logic import login_xmuxg

Executor = ThreadPoolExecutor(max_workers=2)


conn = DBConnector(MONGODB_USER, MONGODB_PWD, MONGODB_DBNAME)


@api_rest.route('/report_result/<string:result_id>')
class ReportResult(Resource):
    def get(self, result_id:str):
        if not result_id or len(result_id) != 36:
            return {'message': 'Not valid id', 'status': -2}
        results = conn.get_result(result_id)
        return {'message': "ok", 'result': results['message'], 'status': results['status']}


@api_rest.route('/apply')
class ReportApply(Resource):
    def get(self):
        return {'message': 'Only support POST method'}

    def post(self) -> dict:
        args = apply_parser.parse_args()
        username = args.get('username')
        password = args.get('password')
        timed = args.get('timed')  # 1开启 2关闭 3维持
        if not username or not password:
            return {'message': 'Empty fields'}
        task_uuid = str(uuid.uuid4())
        Executor.submit(self.do_report, task_uuid, username, password, timed)
        return {'message': 'ok', 'uuid': task_uuid}

    @staticmethod
    def do_report(task_uuid: str, username, password, timed):
        conn.upsert_result(task_uuid, 'Proceeding, Need a moment.', task_status=2)
        s, name = login_xmuxg(username, password)
        if not s:
            conn.upsert_result(task_uuid, "Failed to login. ", task_status=-1)
            return
        conn.upsert_account(username, password, name)
        print(timed)
        if timed == '1':
            conn.upsert_time_task(username, password)
        elif timed == '2':
            conn.del_time_task(username)
        elif timed == '3':
            pass
        else:
            raise ValueError(f"param time is set to {timed}")
        res = health_report(s)
        print(f'uuid: {task_uuid} \nres: {res}')
        conn.upsert_result(task_uuid, res, task_status=3)


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






