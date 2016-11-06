#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
import random
import urllib, urllib2
from bs4 import BeautifulSoup

url = 'http://jandan.net/ooxx'
header = {
            'Referer':'http://jandan.net/',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'
            }
request = urllib2.Request(url, headers=header)
repsonse = urllib2.urlopen(request)
pagecode = repsonse.read()

soup = BeautifulSoup(pagecode, 'lxml')

imgs = soup.findAll(name='a', attrs={'href':re.compile("^http.*?large.*?")})

for img in imgs:
    print img['href']
    urllib.urlretrieve(url=img['href'],filename=str(random.randint(1,100))+'.jpg')
print 'Success...'
