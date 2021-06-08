import requests
from bs4 import BeautifulSoup as bs

Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                         ' like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


def login_xmuxg(username: str, password: str) -> (requests.Session, str):
    s = requests.Session()
    resp = s.get('https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu',
                 headers=Headers)
    content = resp.content.decode('utf-8')
    soup = bs(content, 'lxml')
    form = {'dllt': 'userNamePasswordLogin', 'execution': 'e1s1', '_eventId': 'submit', 'rmShown': '1','rememberMe':'on'
        ,'lt': soup.find('input', attrs={'name': 'lt'})['value'], 'username': username, 'password': password}
    s.post('https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu', data=form,
           headers=Headers)
    r1 = s.get('https://xmuxg.xmu.edu.cn/login/check', headers=Headers)
    try:
        name = r1.json()['data']['name']
        print(f'登陆成功！你好: {name}')
        return s, name
    except Exception as e:
        print('登录失败.', str(e))
        return None, None

