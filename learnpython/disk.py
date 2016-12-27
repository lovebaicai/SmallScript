#!/usr/bin/env python
import os
from datetime import datetime


def disk_stat():
    hd = {}
    disk = os.statvfs("/var/lib/")
    disk1 = os.statvfs("/")

    disksize = disk.f_bsize * disk.f_blocks/(1024*1024*1024)
    used = disk.f_bsize * (disk.f_blocks - disk.f_bfree) / (1024 ** 3)
    hd['diskused'] = format((used / float(disksize)), '.2f')

    disksize1 = disk1.f_bsize * disk1.f_blocks/(1024*1024*1024)
    used1 = disk1.f_bsize * (disk1.f_blocks - disk1.f_bfree) / (1024 ** 3)
    hd['diskused1'] = format((used1 / float(disksize1)), '.2f')

    #return used, disksize, diskused, used1, disksize1, diskused1
    return hd

	
def Email():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    import datetime

    user = 'test@test.com'
    pwd = 'test'
    to = ['test@test.com']
    msg = MIMEMultipart()
    msg['Subject']  = 'Disk Exceed the limit, Please Process!' 
    msg['From'] = user
    msg['To'] = ','.join(to) 

    part = MIMEText('Listenexp disk Exceed the limit, Please Process!')
    msg.attach(part)

    server = smtplib.SMTP('smtp.qq.com')
    server.login(user, pwd)
    server.sendmail(user, to, msg.as_string())
    server.close()
    #print 'Email send ok !!!'

def main():
    hd = disk_stat()
    #print hd
    if float(hd['diskused']) > 0.75 or float(hd['diskused1']) > 0.75:
    	Email() 

if __name__== '__main__':
    time = datetime.now()
    main()
    with open('log.txt', 'a+') as f:
         f.write(str(time) + ' checking ok!\n') 
    f.close()
