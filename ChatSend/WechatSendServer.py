# 启动异步定时任务
import time
import itchat
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.triggers.date import DateTrigger


def wechat_sendfile_server():
    data = {}
    itchat.auto_login()
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # trigger = DateTrigger(run_date='2019-05-13 15:25:30')
    job = scheduler.add_job(send_file_by_time, trigger='date', next_run_time='2019-05-13 14:06:30')
    # job = scheduler.add_job(send_file_by_time, trigger)
    scheduler.start()
    job.remove()

    # try:
    #     # 实例化调度器
    #     scheduler = BackgroundScheduler()
    #     # 调度器使用DjangoJobStore()
    #     scheduler.add_jobstore(DjangoJobStore(), "default")
    #     # itchat.auto_login()
    #     # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
    #     # ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次
    #     @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='13', minute='30', second='10', id='task_time')
    #     def test_job():
    #         itchat.auto_login()
    #         print("开始发送文件-----------------------》start")
    #         group = itchat.get_chatrooms(update=True)
    #         to_group = ' '
    #         to_flag = ' '
    #         for g in group:
    #             # print(g['NickName'])
    #             if g['NickName'] == u'地下党·~~':  # 从群中找到指定的群聊
    #                 # if g['NickName'] == u'福州院数据共享事业部':  # 从群中找到指定的群聊
    #                 to_group = g['UserName']
    #                 to_flag = g['NickName']
    #                 break
    #         print("群名称是===============》", to_group)
    #         if to_flag == u'地下党·~~':
    #             itchat.send_msg('这是定时发送的测试消息，不用理睬！', toUserName='filehelper')
    #         res = itchat.send_file(r'E:\pythonPrograms\DjangoWechatTest\工作日报-数据共享-张卫东-2019.05.09.docx',
    #                                toUserName='filehelper')
    #         itchat.send_msg('这是定时发送的测试消息，不用理睬！', toUserName='filehelper')
    #         print(res)
    #         print("完成发送文件《-----------------------end")
    #         data = res
    #
    #     # 监控任务
    #     register_events(scheduler)
    #     # 调度器开始
    #     scheduler.start()
    # except Exception as e:
    #     print(e)
    #     # 报错则调度器停止执行
    #     scheduler.remove_job('task_time')
    #     scheduler.shutdown()
    # finally:
    #     return data


def send_file_by_time():

    print("开始发送文件-----------------------》start")
    group = itchat.get_chatrooms(update=True)
    to_group = ' '
    to_flag = ' '
    for g in group:
        if g['NickName'] == u'地下党·~~':  # 从群中找到指定的群聊
        # if g['NickName'] == u'福州院数据共享事业部':  # 从群中找到指定的群聊
            to_group = g['UserName']
            to_flag = g['NickName']
            break
    print("群名称是===============》", to_group)
    if to_flag == u'地下党·~~':
        itchat.send_msg('这是定时发送的测试消息，不用理睬！', toUserName='filehelper')

    res = itchat.send_file(r'E:\pythonPrograms\DjangoWechatTest\工作日报-数据共享-张卫东-2019.05.09.docx',
                           toUserName='filehelper')

    print(res)
    print("完成发送文件《-----------------------end")
