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
    user = 'test@test.com'
    pwd = 'test'
    #to = ['test@test.fm']
    msg = MIMEMultipart()
    msg['Subject'] = (str(datetime.date.today()) + 'test')
    msg['From'] = user
    msg['To'] = ','.join(to) #务必加上,smtplib的bug.

    part = MIMEText(str(datetime.date.today()) + 'test')
    msg.attach(part)

    part1 = MIMEApplication(open((str(tabname) + '.xls'), 'rb').read())
    part1.add_header('Content-Disposition', 'attachment', filename=(str(tabname) + '.xls'))
    msg.attach(part1)

    server = smtplib.SMTP('smtp.test.com')
    server.login(user, pwd)
    server.sendmail(user, to, msg.as_string())
    server.close()
    print 'Email send ok !!!'

Email()
