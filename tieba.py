#!/usr/bin/env python
#coding=utf-8
import urllib, urllib2
import re

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

class BDTB:
    def __init__(self, baseUrl, seeLZ, floorTage):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u'百度贴吧'
        self.floorTag = floorTag

    
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #return response.read().decode('utf-8')
            return response.read()
        except urllib2.URLError ,e:
            if hasattr(e,'reason'):
                print e.reason
                return None

    def getTitle(self, page):
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        self.floor = 1
        for item in items:
            content = "\n" + self.tool.replace(item) + "\n"
            #contents.append(content.encode('utf-8')
            contents.append(content)
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open(self.defaultTitle + '.txt', 'w+')
    
    def writeData(self, contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = '\n' + str(self.floor) + u"-----------------"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)
        if pageNum == None:
            print 'URL is disable'
            return
        try:
            print '帖子共有' + str(pageNum) + '页'
            for i in range(1, int(pageNum)+1):
                print '正在写入' + str(i) + '页数据'
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print 'faild' + e.massage
        finally:
            print 'wirte succellful'

print u'Please input 帖子代号'
baseUrl = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
#baseUrl = 'http://tieba.baidu.com/p/3138733512?see_lz=1&pn=1'
seeLZ = raw_input('是否只获取楼主，是输入1，否输入0\n')
floorTag = raw_input('是否写入楼层信息,1,0\n')
bdtb = BDTB(baseUrl, seeLZ, floorTag)
bdtb.start()
