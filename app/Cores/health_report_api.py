import json

import requests


def health_report(s: requests.Session) -> str:
    Headers = {'content-type': 'application/json'}
    try:
        resp = s.get('https://xmuxg.xmu.edu.cn/api/app/214/business/now')
        form_dict = resp.json()
        # change deate in below line ()
        for i in range(0, 1): # only support 1 day since the website forbidden modify of result of former days. 
            businessId = form_dict['data'][i]['business']['id']
            resp = s.get(f'https://xmuxg.xmu.edu.cn/api/formEngine/business/{businessId}/myFormInstance')
            myFormJson = resp.json()
            formid = myFormJson['data']['id']
            form_url = f'https://xmuxg.xmu.edu.cn/api/formEngine/formInstance/{formid}'
            false = 'false'
            true = 'true'
            form_data = {"formData": [
                {"name": "select_1582538796361", "title": "今日体温 Body temperature today （℃）",
                 "value": {"stringValue": "37.3以下 Below 37.3 degree celsius"}, "hide": false},
                {"name": "select_1582538846920",
                 "title": "是否出现发热或咳嗽或胸闷或呼吸困难等症状？Do you have sypmtoms such as fever, coughing, chest tightness or breath difficulties?",
                 "value": {"stringValue": "否 No"}, "hide": false},
                {"name": "select_1584240106785", "title": "学生本人是否填写", "value": {"stringValue": "是"},
                 "hide": false}, {"name": "select_1582538939790",
                                  "title": "Can you hereby declare that all the information provided is all true and accurate and there is no concealment, false information or omission. 本人是否承诺所填报的全部内容均属实、准确，不存在任何隐瞒和不实的情况，更无遗漏之处。",
                                  "value": {"stringValue": "是 Yes"}, "hide": false},
                {"name": "input_1582538924486", "title": "备注 Notes", "value": {"stringValue": ""},
                 "hide": false}], "playerId": "owner"}
            resp = s.post(form_url, data=json.dumps(form_data), headers=Headers)
        # print(resp.content.decode('utf-8'))
        print('打卡完毕!')
        return 'Succeeded'
    except Exception as e:
        print(e)
        return 'Exception!'
