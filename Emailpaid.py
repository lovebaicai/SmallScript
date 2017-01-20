#!/usr/bin/env python
#-*- coding:utf-8-*-

import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def Email():
    time1 = datetime.datetime.now().strftime('%Y%m%d')
    tabname = 'sound_' + time1
    user = 'foruser'
    pwd = 'pwd'
    to = ['touser']
    msg = MIMEMultipart()
    msg['Subject'] = '付费节目每日数据统计'
    msg['From'] = user
    msg['To'] = ','.join(to) #务必加上,smtplib的bug.

    part = MIMEText(str(datetime.date.today()) + '付费节目数据统计')
    msg.attach(part)

    part1 = MIMEApplication(open((str(tabname) + '.xls'), 'rb').read())
    part1.add_header('Content-Disposition', 'attachment', filename="paid.xls")
    msg.attach(part1)

    server = smtplib.SMTP('smtp.exmail.qq.com')
    server.login(user, pwd)
    server.sendmail(user, to, msg.as_string())
    server.close()
    print 'Email send ok !!!'

if __name__ == '__main__':
    Email()
