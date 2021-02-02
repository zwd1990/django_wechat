# 启动异步定时任务
import itchat
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.triggers.date import DateTrigger


class WechatScheduler(object):
    def __init__(self, date_time, file_name, group_name, send_message):
    # def __init__(self, date_time):
        self.mychat = itchat.Core()
        self.date_time = date_time
        self.file_name = file_name
        self.group_name = group_name
        self.send_message = send_message


    def wechat_login_server(self):
        mychat = self.mychat
        print("11111111111", mychat)
        print("11111111111", type(mychat))

        uuid = mychat.get_QRuuid()
        print("uuid is ============", uuid)
        qr_io = mychat.get_QR(enableCmdQR=2)
        qr_io.seek(0)

        return qr_io

    def wechat_sendfile_server(self):
        mychat = self.mychat
        status = mychat.check_login()
        if status == '200':
            isLoggedIn = True
            print("deng==============")
        mychat.web_init()
        mychat.show_mobile_login()
        mychat.get_contact(True)
        mychat.start_receiving()

        scheduler = BackgroundScheduler()
        # 调度器使用DjangoJobStore()
        # scheduler.add_jobstore(DjangoJobStore(), "default")
        trigger = DateTrigger(run_date=self.date_time)
        # job = scheduler.add_job(send_file_by_time, trigger='date', next_run_time='2019-05-13 14:52:30')
        job = scheduler.add_job(self.send_file_by_time, trigger)
        print(job)
        scheduler.start()
        return


    def send_file_by_time(self):
        mychat = self.mychat
        print("开始发送文件-----------------------》start")
        group = mychat.get_chatrooms(update=True)
        to_group = ' '
        to_flag = ' '
        for g in group:
            if g['NickName'] == self.group_name:  # 从群中找到指定的群聊
            # if g['NickName'] == u'福州院数据共享事业部':  # 从群中找到指定的群聊
                to_group = g['UserName']
                to_flag = g['NickName']
                break
        print("群名称是===============》", to_group)

        if to_flag == self.group_name and self.send_message != '':
            mychat.send_msg(self.send_message, toUserName=to_group)
        res = mychat.send_file(self.file_name, toUserName=to_group)

        print(res)
        print("完成发送文件《-----------------------end")
