import requests


def check_session(s:requests.Session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.'
                      '36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    resp = s.get('https://xmuxg.xmu.edu.cn/login/check', headers=headers)
    try:
        name = resp.json()['data']['name']
        print(f'session verified {name}')
        return True
    except Exception as e:
        print(str(e))
        return False

