#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
class sendemail:
    def __init__(self,receivers=['booking_service@yeah.net'],isend=0):
        #邮箱服务器地址
        self.mail_host = 'smtp.yeah.net'  
        #用户名
        self.mail_user = 'booking_service'  
        #密码(部分邮箱为授权码) 
        self.mail_pass = 'RQWTEFQKJYJNPZAS'   
        self.sender = 'booking_service@yeah.net'
        self.receivers = receivers  # 
        self.isend=isend
    
    def sendemail(self, message): 
        #登录并发送邮件
        if self.isend:
            try:
                smtpObj = smtplib.SMTP() 
                #连接到服务器
                smtpObj.connect(self.mail_host,25)
                #登录到服务器
                smtpObj.login(self.mail_user,self.mail_pass) 
                #发送
                smtpObj.sendmail(
                    self.sender,self.receivers,message.as_string()) 
                #退出
                smtpObj.quit() 
                print("发送邮件")
            except smtplib.SMTPException as e:
                print('error',e) #打印错误
        else:
            print("测试阶段，不发送邮件")
    def getsender(self):
        return self.sender
    def getreceivers(self, id=0):
        return self.receivers[id]

# Email=sendemail()
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
# message = MIMEText('预定成功，请在15分钟内在清华大学体育管理与网上预约系统上完成支付', 'plain', 'utf-8')
# message['From'] = Email.getsender()   # 发送者
# message['To'] =  Email.getreceivers()     # 接收者 
# message['Subject'] = '场地预定成功信息'

# Email.sendemail(message0)
 
