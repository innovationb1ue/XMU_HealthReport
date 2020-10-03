from apscheduler.schedulers.blocking import BlockingScheduler
from app.Cores.DB_conn import DBConnector
from app.Cores.health_report_api import health_report
from app.Cores.login_logic import login_xmuxg


conn = DBConnector()
sche = BlockingScheduler()

@sche.scheduled_job('cron', day_of_week='*', hour=12, minute=0, second=0)
def time_report_job():
    for j in conn.get_time_tasks():
        s = login_xmuxg(j.get('username'), j.get('password'))
        health_report(1, s)


if __name__ == '__main__':
    sche.start()
