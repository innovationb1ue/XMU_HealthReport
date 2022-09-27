import json

import requests
from bs4 import BeautifulSoup as bs
import execjs
import json

Headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Aoyou/WnVDaDxcMSs7U2pMdGcxR8ojOsrBN_eEl1V5m1EUYUNuimscundQvTOr2g==',
    'origin': "https://ids.xmu.edu.cn",
    "referer": "https://ids.xmu.edu.cn/authserver/login?service=https://account.soe.xmu.edu.cn/Account/XMULogin",
}

Headers2 = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Aoyou/WnVDaDxcMSs7U2pMdGcxR8ojOsrBN_eEl1V5m1EUYUNuimscundQvTOr2g==',
    "Origin": "http://event.soe.xmu.edu.cn",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "http://event.soe.xmu.edu.cn/authenticate.aspx?currentCulture=zh-CN",
    "Host": "event.soe.xmu.edu.cn",
    "X-Requested-With": "XMLHttpRequest"
}


def encrypt(pwd, key):
    with open('./EncryptJS.js', 'r') as f:
        js_str = f.read()
    js = execjs.compile(js_str)
    return js.call('encrypt_pass', pwd, key)


def login_xmuxg(username: str, password: str):
    s = requests.Session()
    resp = s.get('https://ids.xmu.edu.cn/authserver/login?service=https://account.soe.xmu.edu.cn/Account/XMULogin',
                 headers=Headers)
    content = resp.content.decode('utf-8')
    soup = bs(content, 'lxml')
    form = {'dllt': 'userNamePasswordLogin', 'execution': 'e1s1', '_eventId': 'submit', 'rmShown': '1',
            'lt': soup.find('input', attrs={'name': 'lt'})['value'], 'username': username,
            'password': encrypt(password, soup.find('input', attrs={'id': 'pwdDefaultEncryptSalt'})['value'])}
    resp = s.post('https://ids.xmu.edu.cn/authserver/login?service=https://account.soe.xmu.edu.cn/Account/XMULogin', data=form,
           headers=Headers, allow_redirects=True)
    r1 = s.get('https://account.soe.xmu.edu.cn/Home', headers=Headers)
    print(r1.content.decode('utf-8'))
    token_resp = s.get("http://account.soe.xmu.edu.cn/WcfServices/SSOService.svc/Account/RequestToken?callback=").content.decode("utf-8")[1:-2]
    token = json.loads(token_resp)["Token"]
    token_resp2 = s.post("http://event.soe.xmu.edu.cn/Authenticate.aspx", data={"token": token}, headers=Headers2)
    print(token_resp2.content.decode('utf-8'))
    final = s.get("http://event.soe.xmu.edu.cn/LectureOrder2.aspx?stuno=15320211152700")


if __name__ == '__main__':
    login_xmuxg('', '')  # test method. input your name&pass here to run the test
