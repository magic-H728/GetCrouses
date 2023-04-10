import argparse
import configparser
import os
import time
import warnings

import win32api
import win32con

import Get
from auth import Auth

if __name__ == '__main__':
    # verify()
    warnings.filterwarnings('ignore')
    print("请稍作等待")
    print("正在读取config.ini文件")
    if os.path.exists('config.ini'):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding="UTF-8")
        school_id = config.get('user', 'name')
        pwd = config.get('user', 'password')
    else:
        win32api.MessageBox(0, "找不到config.ini文件", "提醒", win32con.MB_OK)
        exit()

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-c', '--course', action="store_true", help='get course ics')
    parser.add_argument('-e', '--exam', action="store_true", help='get exam ics')
    args = parser.parse_args()
    print("正在登录教务系统...")
    auth = Auth()
    ok, session = auth.login(school_id, pwd)
    if not ok:
        print('login fail')
        win32api.MessageBox(0, "学号或者密码错误", "提醒", win32con.MB_OK)
        exit()
    print("教务系统登录成功！")
    # id = 'F2E8C944459C47558D3198A50B53AC8A'

    res = session.get('https://jwxt.sztu.edu.cn/jsxsd/xsxk/xklc_list')

    id = Get.getID(res)

    session.get('https://jwxt.sztu.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=' + id)

    CrouseName = '软件工程'
    TeacherName = '靳小鹏'
    Day = '5'
    Time = '7-8-'
    cnt = 1

    SleepTime = 30

    # 十秒钟执行一次
    while True:
        print("第%d次尝试抢课" % cnt)
        cnt += 1
        try:
            # CrouseName是课程名称，TeacherName是老师名称，Day是星期几，Time是第几节课，最后一个参数是主选还是非主选
            # Day和Time可以为空,填写''
            # 体育课不填课程名称,一定要填老师名称、星期几、第几节课, 例如: Get.getCrouse(session, '', '李娟', '3', '7-8-')
            # 公选课使用Get2.getCrouse(session, CrouseName, TeacherName, Day, Time)
            Get.getCrouse(session, CrouseName, TeacherName, Day, Time, 'All')
            # Get2.getCrouse(session, CrouseName, TeacherName, Day, Time)
            # 如果要抢的课程有多个，可以在这里添加，要加入延时(一秒钟左右)，不然容易挂
            # Get.getCrouse(session, '操作系统', '王鑫', Day, Time)
            # time.sleep(1)
            # Get.getCrouse(session, '', '肖榕', Day, Time)

            # 一般来说，5-10秒钟执行一次就可以了。选课系统刚开放的时候可以设置1秒钟执行一次
            time.sleep(SleepTime)
        except:
            print("选课系统未开放")
            time.sleep(SleepTime)
