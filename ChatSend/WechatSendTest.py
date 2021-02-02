#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
import itchat
import time
from apscheduler.schedulers.background import BlockingScheduler
# from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger


def send_file_by_time():

    print("开始发送文件-----------------------》start")
    group = itchat.get_chatrooms(update=True)
    to_group = ' '
    to_flag = ' '
    for g in group:
        # print(g['NickName'])
        if g['NickName'] == u'地下党·~~':  # 从群中找到指定的群聊
        # if g['NickName'] == u'福州院数据共享事业部':  # 从群中找到指定的群聊
            to_group = g['UserName']
            to_flag = g['NickName']
            break
    print("群名称是===============》", to_group)
    if to_flag == u'地下党·~~':
        itchat.send_msg('这是定时发送的测试消息，不用理睬！', toUserName=to_group)
    # res = itchat.send_file(r'E:\pythonPrograms\WechatTest\工作日报-数据共享-张卫东-2019.05.06.docx', toUserName=to_group)
    res = itchat.send_file(r'E:\pythonPrograms\WechatTest\工作日报-数据共享-张卫东-2019.05.09.docx', toUserName=to_group)
    # res = itchat.send_file(r'E:\pythonPrograms\WechatTest\工作日报-数据共享-张卫东-2019.05.06.docx', toUserName='filehelper')
    print(res)
    print("完成发送文件《-----------------------end")

def main():
    itchat.auto_login()
    # itchat.auto_login(hotReload=True)
    scheduler = BlockingScheduler()
    # job = scheduler.add_job(send_file_by_time, 'date', next_run_time='2019-05-06 16:46:30')
    trigger = DateTrigger(run_date='2019-05-10 15:25:30')
    # job = scheduler.add_job(send_file_by_time, trigger='date', next_run_time='2019-05-10 14:30:30')
    job = scheduler.add_job(send_file_by_time, trigger)
    scheduler.start()
    job.remove()

if __name__ =="__main__":
    main()
