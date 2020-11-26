#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
class sendemail:
    def __init__(self,receivers=['booking_service@yeah.net'],isend=0):
        #邮箱服务器地址, 本初始化内容可以根据自己的情况进行设置
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


 
