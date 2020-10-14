import pymongo
from typing import List, Dict
from ..LOGS import NewLogger
import logging
import traceback
from ..CONFIG import *


class DBConnector:
    def __init__(self, db_user: str = '', db_pwd: str = '', db_name: str = ''):
        client = pymongo.MongoClient(f'mongodb://{db_user}:{db_pwd}@localhost:27017/{db_name}')
        self.p_db = client.Accounts
        self.p_db.authenticate(db_user, db_pwd)
        self.p_Acc = self.p_db.Accounts_collection
        self.p_Res = self.p_db.Results
        self.p_Time = self.p_db.Accounts_timed
        try:
            self.logger = NewLogger(LOGGER_SAVE_PATH)
        except Exception as e:
            print('-----> start logger failed')
            self.logger = logging.getLogger()

    def upsert_account(self, username: str, password:str, name:str) -> bool:
        """
        :param username: as it is
        :param password: as it is
        :param name: the full name of login user
        :return: Boolean for Success or not
        """
        try:
            if not username or not password:
                return False
            self.p_Acc.update_one({"username": username}, {'$set':{'password': password, 'name':name}},
                                  upsert=True)
            return True
        except Exception as e:
            self.logger.log(logging.ERROR, traceback.print_tb(e))
            return False

    def upsert_result(self, taskid: str, result: str, task_status: int):
        """
        status 1: applied
        status 2: processing
        status 3: finished
        status -1: login Failed
        status -2: not valid task ID
        """
        try:
            if not taskid or not result:
                return False
            self.p_Res.update_one({'taskid':taskid}, {'$set': {'result':result, 'status':task_status}}, upsert=True)
        except Exception as e:
            self.logger.log(logging.ERROR, traceback.print_tb(e))
            return False

    def upsert_time_task(self, username: str, password: str):
        try:
            self.p_Time.update_one({'username': username}, {'$set': {'password': password}}, upsert=True)
            return True
        except Exception as e:
            self.logger.log(logging.ERROR, traceback.print_tb(e))

    def del_time_task(self, username:str):
        if self.p_Time.delete_one({'username': username}):
            return True

    def get_result(self, taskid):
        for i in self.p_Res.find({"taskid": taskid}):
            return {'message': i.get("result"), 'status': i.get('status')}

    def get_time_tasks(self) -> List[Dict]:
        return [*self.p_Time.find()]

    def get_pwd(self, username):
        for i in self.p_Acc.find({'username': username}):
            return i.get("password")


def testlines():
    client = pymongo.MongoClient('mongodb://admin:blueking007@localhost:27017/Accounts')
    p = client.Accounts
    p.authenticate('admin', 'blueking007')
    p = p.Accounts_collection
    for i in p.find():
        print(i, type(i), i['_id'], type(i['_id']))





