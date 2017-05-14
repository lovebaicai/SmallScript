#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: nemo_chen 

import time
import datetime
from selenium import webdriver

url = 'http://item.mi.com/product/10000041.html'

print('open mi6 buy page')
# brower info
driver = webdriver.Chrome()
driver.get(url)
driver.set_window_size(1855, 962)
time.sleep(2)

print('submit account & password')

# login process
driver.find_element_by_link_text(u'登录').click()
account = driver.find_element_by_id('username')
password = driver.find_element_by_id('pwd')
submit = driver.find_element_by_id('login-button')
account.clear()
password.clear()
account.send_keys('username')
password.send_keys('password')
submit.click()
time.sleep(0.5)
cookies = driver.get_cookies()

# swich page of buy mi6
a = int(datetime.datetime.now().strftime('%H%M%S'))
b = int('100000')
c = b - a
while c >0:
    c -= 1
    print(('Remaining time: {}s').format(c))
    time.sleep(1)

print('start rush to buym6, fuck xiaomi')

while 1:
    try:
        driver.find_element_by_xpath('//*[@id="J_buyBtnBox"]/li/a').click()
    except:
        pass
    if (driver.find_element_by_xpath('//*[@id="J_buyBtnBox"]/li/a').click()) == True:
        break

time.sleep(5)
driver.close()

