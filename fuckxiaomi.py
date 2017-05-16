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
account.send_keys('username') #input your mi login username
password.send_keys('password') #input your mi login password
submit.click()
time.sleep(0.5)
cookies = driver.get_cookies()

# swich page of buy mi6

print('start Snapped up m6, fuck xiaomi')

p = 0
while 1:
    try:
        driver.find_element_by_xpath('//*[@id="J_buyBtnBox"]/li/a').click()
        p += 1
        print('click %s times' % p)
    except:
        pass

time.sleep(120)
driver.close()

