# from Utils.health_report_api import health_report
import time
import random
from app.Cores.login_logic import login_xmuxg
from app.apis.report import health_report

"""

"""


if __name__ == '__main__':
    # 自定义参数(请填写)
    USERNAME = input('username : ')  # 统一身份认证账号
    PASSWORD = input('password : ')  # 统一身份认证密码
    N = 1  # 你要打卡的天数,1为只打今天，2为打昨天和今天.....以此类推
    while True:
        s, name = login_xmuxg(USERNAME, PASSWORD)
        res = health_report(s)
        print(res)
        rnd = random.randint(-100, 100)
        time.sleep(60*60*24 + rnd)
