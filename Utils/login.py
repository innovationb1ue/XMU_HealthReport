import requests
from bs4 import BeautifulSoup as bs
import execjs

Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def encrypt(pwd, key):
    with open('Utils/EncryptJS.js', 'r') as f:
        js_str = f.read()
    js = execjs.compile(js_str)
    return js.call('encrypt_pass', pwd, key)

def login_xmuxg(username:str, password:str):
    s = requests.Session()
    resp = s.get('https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu',headers=Headers)
    content = resp.content.decode('utf-8')
    soup = bs(content, 'lxml')
    form = {'dllt': 'userNamePasswordLogin', 'execution': 'e1s1', '_eventId': 'submit', 'rmShown': '1','rememberMe':'on',
            'lt': soup.find('input', attrs={'name': 'lt'})['value'], 'username': username, 'password': encrypt(password, soup.find('input',attrs={'id':'pwdDefaultEncryptSalt'})['value'])}
    s.post('https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu', data=form, headers=Headers)
    r1 = s.get('https://xmuxg.xmu.edu.cn/login/check', headers=Headers)
    try:
        name = r1.json()['data']['name']
        print(f'登陆成功！你好: {name}')
        return s
    except Exception as e:
        print('登录失败.')
        print(str(e))
        return False


if __name__ == '__main__':
    login_xmuxg('', '') # test method. input your name&pass here to run the test


