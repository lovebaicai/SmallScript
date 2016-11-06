#!/usr/bin/env python
#coding=utf-8
#filename:zhihu.py

import urllib, urllib2
import time
import re
'''
class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    def replace(self, x): 
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()
'''
class Zhihu:
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent' : self.user_agent }
        self.enable = False
        #self.tool = Tool()

    def getPage(self):
        try:
            url = 'https://www.zhihu.com/topic/19552444/top-answers'
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print 'error: ', e.reason
                return None

    def getItem(self):
        pageCode = self.getPage()
        if not pageCode:
            print 'error pageCode'
        pattern = re.compile('<a class="question_link.*?>(.*?)</a>.*?<a class="author-link.*?>(.*?)</a>.*?<textarea hidden class=".*?">(.*?)</textarea>', re.S)
        result = re.findall(pattern, pageCode)
        pageStores = []
        for item in result:
            pageStores.append([item[0].strip(), item[1].strip(), item[2].strip()])
        return pageStores 

    def start(self):
        self.enable = True
        self.getItem()

spider = Zhihu()
print spider.start()
