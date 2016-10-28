#!/usr/bin/env python3
#-*-coding:utf-8-*-
#author:nemo_chen
#version:1.0

from datetime import datetime
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr ='xxxx@xxxx.com' 
password = 'xxxxx'
to_addr = 'xxxx@xxxx.com'
smtp_server = 'smtp.xx.com'
time = datetime.now()

def food():
    try:
        msg = MIMEText('mail', 'plain', 'utf-8')
        msg['From'] = _format_addr('mailname<%s>' % from_addr)
        msg['To'] = _format_addr('tomailname <%s>' % to_addr)
        msg['Subject'] = Header('title', 'utf-8').encode()
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        with open('/var/log/food.log', 'a+') as d:
            d.write(str(time) + ' ok\n')
    except Exception as f:
        return f
        with open('/var/log/food.log', 'a+') as a:
            a.write(f)
food()
