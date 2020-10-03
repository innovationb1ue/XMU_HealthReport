import pymongo
from typing import List, Dict
from ..LOGS import NewLogger
import traceback


class DBConnector():
    def __init__(self, db_user='', db_pwd=''):
        client = pymongo.MongoClient('mongodb://admin:blueking007@localhost:27017/Accounts')
        self.p_db = client.Accounts
        self.p_db.authenticate(db_user, db_pwd)
        self.p_act = self.p_db.Accounts_collection
        self.p_res = self.p_db.Results
        self.p_time = self.p_db.Accounts_timed
        self.logger = NewLogger('/Users/jeffb1ue/XMU_AutoHealthReporter/app/LOGS/log_file.txt')


    def upsert_account(self, document: Dict) -> bool:
        '''
        Upsert username and password once login in
        :param document: List of Dict of documents
        :return: Boolean
        '''
        try:
            if not document.get('username') or not document.get('password'):
                return False
            self.p_act.update_one({"username": document.get('username')}, {'$set':{'password': document.get('password')}},
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


def testlines():
    client = pymongo.MongoClient('mongodb://admin:blueking007@localhost:27017/Accounts')
    p = client.Accounts
    p.authenticate('admin', 'blueking007')
    p = p.Account_collection
    for i in p.find():
        print(i, type(i), i['_id'], type(i['_id']))





