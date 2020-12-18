#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    HappyFriday--v1.0.3
    作者：手慢无玩家
    此脚本仅TRL内部玩家使用，严禁外传
    1.使用前请安装python3.x
    2.使用前需要安装对应版本的chromedriver(与本机的chrome 版本号一致)
        http://chromedriver.storage.googleapis.com/index.html
        将chromedriver 放置python3x 文件目录内
    3.安装selenium: pip install selenium
    4.cmd 中运行 & D:/Python/Python39/python.exe  .\HappyFriday.py
      D:/Python/Python39/python.exe  请替换成本机python安装目录
      或者直接双击.\HappyFriday.py (前提请关联打开方式为python)
'''

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time, datetime
from sendemail import sendemail
import smtplib
from email.mime.text import MIMEText
def isElementnoPresent(dr,by,value):
    try:
        
        element = dr.find_element(by=by, value=value)
        return False
    except:
        return True
def isElementPresent(dr,by,value):
    try:
        element = dr.find_element(by=by, value=value)
        return True
    except:
        return False
#基本信息设置
#登录信息
username="200000000000"
password="*000000!"
#选择信息： 场馆gym; 项目：item; 日期：date; 预定场地：row(行：不包括标题行)，col(列：不包括标题列)
select={'gym':  'qimo',\
        'item': 'badminton',\
        'date': '2020-12-19',\
        'row':  -1,\
        'col':  4}
#是否预定
ibook=False #True 直接预定，网上支付； False 到预定界面，不确认，仅用于测试

#设置邮件通知
Email=sendemail(['test@126.com'],isend=0)

startTime=datetime.datetime(2020,12,16,7,45,0) #设置启动时间
print('Program will start at', startTime)

while datetime.datetime.now() < startTime:
	time.sleep(1)
print('Program now starts at ',datetime.datetime.now())
print('Executing...')
#程序开始部分
message = MIMEText('程序已启动 '+str(startTime), 'plain', 'utf-8')
message['From'] = Email.getsender()   # 发送者
message['To'] =  Email.getreceivers()     # 接收者 
message['Subject'] = 'booking info'
Email.sendemail(message)
#
gymlist={'qimo': '3998000','xiti':'4836273'}
if (select['gym'] == 'qimo'):
    gymitem={'badminton':'4045681','ping-pong':'4037036'}
elif (select['gym'] == 'xiti'):
    gymitem={'badminton':'4836196'}
else:
    print("请检查gym输入是否正确")
    
book_url="http://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id="+gymlist[select['gym']]+"&item_id="+gymitem[select['item']]+"&time_date="+select['date']+"&userType"
if (select['row'] >0):
    url="/html/body/table/tbody/tr["+str(select['row']+1)+"]/td["+str(select['col'])+"]"


chromeoptions=Options()
chromeoptions.add_argument('--headless')
#启动浏览器            
driver= webdriver.Chrome(options=chromeoptions)
# driver.maximize_window()
 
driver.implicitly_wait(3)#等待3秒
#登录界面
driver.get("http://50.tsinghua.edu.cn/dl.jsp")
driver.find_element_by_id("login_username").send_keys(username)
driver.find_element_by_id("login_password").send_keys(password)
# driver.find_element_by_xpath("//div[@class='submit clearfix']/input[@alt=\"Login\"]").click()
time.sleep(0.5) #停顿片刻，给网站反应时间
try:
    driver.find_element_by_xpath("/html/body/form/div/div/div[1]/div[2]/div[2]/div[3]/input").click()
except:
    driver.find_element_by_xpath("/html/body/form/div/div/div[1]/div[2]/div[2]/div[3]/input").click()
#场地预约界面
# print(book_url)
driver.get(book_url)
# driver.get("http://50.tsinghua.edu.cn/gymbook/gymBookAction.do?ms=viewGymBook&gymnasium_id=3998000&item_id=4037036&time_date=2020-11-27&userType")

#首次进入需要确定《预定须知》
time.sleep(0.5) #停顿片刻，给网站反应时间
try:
    driver.find_element_by_xpath("/html/body/div[3]/div[3]/button").click()
except:
    driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[2]/div[3]/button").click()
#如果没有开放，刷新页面，直到场地开放
driver.implicitly_wait(0.1)#等待0.1秒
while isElementnoPresent(driver,"id","bookTableDiv") :
    driver.refresh() # 刷新方法 refresh
    print("预约未开放，刷新ing")
driver.implicitly_wait(3)#等待1秒
#开始进行场地预约
driver.switch_to.frame("overlayView")
#场地位置选择，tr 行； td 列
if (select['row'] <0):
    table1=driver.find_element_by_xpath("/html/body/table")
    table_rows = len(table1.find_elements_by_tag_name('tr'))
    url="/html/body/table/tbody/tr["+str(table_rows+select['row']+1)+"]/td["+str(select['col'])+"]"

# print(url)
driver.find_element_by_xpath(url).click()

#点击预约按钮
driver.switch_to.default_content()
try:
    driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div[1]/div/div/div[4]/span/a/span/span/i").click()
    print("点击预定")
except:
    print("场地已被预定,或不存在")
#点击确认预约按钮
if ibook:
    try:
        driver.find_element_by_xpath("/html/body/div[5]/div[3]/a[1]").click()
        print("点击支付")
    except:
        print("场地已被预定,或不存在")
    time.sleep(0.5) #停顿片刻，给网站反应时间    
    if isElementPresent(driver,"id","payFrm"): 
        print("成功预定,请在15分钟内支付订单")
        print("Enjoy Friday!")
        message = MIMEText('预定成功，请在15分钟内在清华大学体育管理与网上预约系统上完成支付', 'plain', 'utf-8')
        message['From'] = Email.getsender()   # 发送者
        message['To'] =  Email.getreceivers()     # 接收者 
        message['Subject'] ='booking info'
        Email.sendemail(message)
    else:
        print("预定失败")
        print("Try again!")
        message = MIMEText('预定失败', 'plain', 'utf-8')
        message['From'] = Email.getsender()   # 发送者
        message['To'] =  Email.getreceivers()     # 接收者 
        message['Subject'] = 'booking info'
        Email.sendemail(message)

print("HappyFriday  done!")

message = MIMEText('Program has done', 'plain', 'utf-8')
message['From'] = Email.getsender()       # 发送者
message['To'] =  Email.getreceivers()     # 接收者 
message['Subject'] = 'booking info'
Email.sendemail(message)
time.sleep(3) #停顿片刻，给网站反应时间
driver.quit()
# print("Hello world")
