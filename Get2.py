# 导入Json模块
import json
import time
import urllib.parse

import requests
import winsound
from bs4 import BeautifulSoup

# 忽略警告
requests.packages.urllib3.disable_warnings()


def addCrouse(jx0404id, kcid, session):
    url = 'https://jwxt.sztu.edu.cn/jsxsd/xsxkkc/ggxxkxkOper?kcid='
    url += str(kcid) + '&cfbs=null' + '&cfbs=null' + '&jx0404id=' + \
           str(jx0404id) + '&xkzy=' + '&trjf='
    # response = requests.get(url, headers=headers, verify=False)
    response = session.get(url, verify=False)
    res = BeautifulSoup(response.text, 'html.parser')
    print(res)
    # exit()


def Music():
    # 播放提示音
    winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS)


def getCrouse(session, CourseName, TeacherName, Day, Time):
    # 编造cookies 伪装成浏览器
    # headers = {
    #     # 定期更换Cookie
    #     'Cookie': "JSESSIONID=F7F851EE3C65E1A1750F8768E4C03E63; SELF_SERVICE_SID=96294F382E2A4D1EBC260D5042CF4EB5; SERVERID=125; JSESSIONID=B3A128BA5D1FDA6594F79683F48A35E5"
    # }

    # 课程名称 kcxx=操作系统，将中文转换为url编码
    kcxx = urllib.parse.quote(CourseName)
    # 授课老师 skls=王鑫
    skls = urllib.parse.quote(TeacherName)
    # 课程星期
    skxq = urllib.parse.quote(Day)
    # 课程节次
    skjc = urllib.parse.quote(Time)
    # sfym=false
    sfym = False
    # sfct=false
    sfct = False
    # sfxx=false
    sfxx = False
    # skfs=
    skfs = urllib.parse.quote('')

    # 拼接url
    urls = 'https://jwxt.sztu.edu.cn/jsxsd/xsxkkc/xsxkGgxxkxk?kcxx=' + kcxx + '&skls=' + skls + '&skxq=' + skxq + '&skjc=' + skjc + '&sfym=' + str(
        sfym) + '&sfct=' + str(sfct) + '&sfxx=' + str(sfxx) + '&skfs=' + skfs

    # print(urls)

    data = {
        'sEcho': 1,
        'iColumns': 14,
        'sColumns': '',
        'iDisplayStart': 0,
        'iDisplayLength': 15,
        'mDataProp_0': 'kch',
        'mDataProp_1': 'kczh',
        'mDataProp_2': 'kcmc',
        'mDataProp_3': 'xf',
        'mDataProp_4': 'skls',
        'mDataProp_5': 'sksj',
        'mDataProp_6': 'skdd',
        'mDataProp_7': 'xqmc',
        'mDataProp_8': 'syzxwrs',
        'mDataProp_9': 'syfzxwrs',
        'mDataProp_10': 'ctsm',
        'mDataProp_11': 'szkcflmc',
        'mDataProp_12': 'czOper'

    }

    # 发送请求，.text返回的是字符串
    # response = requests.get(urls, headers=headers, stream=True, verify=False).text
    # 使用post请求
    # response = requests.post(urls, headers=headers,
    #                          data=data, stream=True, verify=False).text

    response = session.post(urls, data=data, stream=True, verify=False).text
    res = BeautifulSoup(response, 'html.parser')
    # 将res转化为json格式
    res = json.loads(res.text)
    # print(res['aaData'])

    for crouse in res['aaData']:
        print("课程名称：", crouse['kcmc'] + " " + str(crouse['fzmc']), "剩余主选人数", crouse['syzxwrs'],
              "剩余非主选人数",
              crouse['syfzxwrs'], "授课老师:", crouse['skls'])
        print('----------------------------------')

        jx0404id = crouse['jx0404id']
        kcid = crouse['jx02id']
        # 主选人数不为0
        # if int(crouse['syzxwrs']) != 0:
        #     print('有课了')
        #     addCrouse(jx0404id, kcid,session)
        #     Music()
        # 非主选人数不为0
        if int(crouse['syfzxwrs']) != 0:
            print('有课了')
            addCrouse(jx0404id, kcid, session)
            Music()


if __name__ == '__main__':
    # 每10秒执行一次
    while True:
        getCrouse()
        time.sleep(10)
