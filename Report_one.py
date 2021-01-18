from Utils.health_report_api import health_report

# 自定义参数(请填写)
USERNAME = input('username : ')  # 统一身份认证账号
PASSWORD = input('password : ')  # 统一身份认证密码
N = 2  # 你要打卡的天数,1为只打今天，2为打昨天和今天.....以此类推

if __name__ == '__main__':
    a = health_report(USERNAME, PASSWORD, N)
    print(a)
