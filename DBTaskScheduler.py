from apscheduler.schedulers.blocking import BlockingScheduler
from app.Cores.DB_conn import DBConnector
from app.Cores.login_logic import login_xmuxg
from app.CONFIG import *
from app.Cores.health_report_api import health_report

"""Entry: 自动对数据库内的账号进行打卡操作 """

conn = DBConnector(MONGODB_USER, MONGODB_PWD, MONGODB_DBNAME)
sche = BlockingScheduler()


@sche.scheduled_job('cron', day_of_week='*', hour=12, minute=0, second=0)
def time_report_job():
    dicts = conn.get_time_tasks()
    for j in dicts:
        username = j.get('username')
        password = j.get('password')
        s, name = login_xmuxg(username, password)
        if s:
            health_report(s)
        else:
            # try to del time task if password is wrong.
            conn.del_time_task(username)
            print('Login failed')
            pass


if __name__ == '__main__':
    sche.start()
