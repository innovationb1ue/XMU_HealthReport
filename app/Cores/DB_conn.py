import pymongo
from typing import List, Dict
from ..LOGS import NewLogger
import traceback


class DBConnector():
    def __init__(self, db_user:str='', db_pwd:str='', db_name:str=''):
        client = pymongo.MongoClient(f'mongodb://admin:blueking007@localhost:27017/{db_name}')
        self.p_db = client.Accounts
        self.p_db.authenticate(db_user, db_pwd)
        self.p_act = self.p_db.Accounts_collection
        self.p_res = self.p_db.Results
        self.p_time = self.p_db.Accounts_timed
        self.logger = NewLogger('/Users/jeffb1ue/XMU_AutoHealthReporter/app/LOGS/log_file.txt')

    def upsert_account(self, username:str, password:str) -> bool:
        """
        :param username: as it is
        :param password: as it is
        :return:
        """
        try:
            if not username or not password:
                return False
            self.p_act.update_one({"username": username}, {'$set':{'password': password}},
                                  upsert=True)
            return True
        except Exception as e:
            self.logger.log(traceback.print_tb(e))
            return False

    def upsert_result(self, taskid:str, result:str):
        try:
            if not taskid or not result:
                return False
            self.p_res.update_one({'taskid':taskid}, {'$set': {'result':result}}, upsert=True)
        except Exception as e:
            self.logger.log(traceback.print_tb(e))
            return False

    def upsert_time_task(self, username:str, password:str):
        if self.p_time.update_one({'username':username}, {'$set': {'password': password}}, upsert=True):
            return True

    def del_time_task(self, username:str):
        if self.p_time.delete_one({'username':username}):
            return True

    def get_result(self, taskid):
        for i in self.p_res.find({"taskid":taskid}):
            return i.get("result")
        return None

    def get_time_tasks(self) -> List[Dict]:
        return [*self.p_time.find()]

    def get_pwd(self, username):
        for i in self.p_act.find({'username': username}):
            return i.get("password")


def testlines():
    client = pymongo.MongoClient('mongodb://admin:blueking007@localhost:27017/Accounts')
    p = client.Accounts
    p.authenticate('admin', 'blueking007')
    p = p.Account_collection
    for i in p.find():
        print(i, type(i), i['_id'], type(i['_id']))




