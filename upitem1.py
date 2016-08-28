#!/usr/bin/env python
#-*- coding:utf-8-*-
import xlwt
import urllib2
from bs4 import BeautifulSoup
from lxml import etree
import logging
import sys
from datetime import datetime
from gzip import GzipFile
from StringIO import StringIO
reload(sys)
sys.setdefaultencoding("utf-8")

debug_log = logging.FileHandler(filename='debug.log')
debug_log.setLevel(logging.WARNING)
logging.getLogger('').addHandler(debug_log)

def Soup(url):
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request, timeout=10)
        pagecode = response.read()
        soup = BeautifulSoup(pagecode, 'lxml')
        return soup
    except urllib2.URLError, e:
        pass

class ContentEncodingProcessor(urllib2.BaseHandler):
# add headers to requests
    def http_request(self, req):
        req.add_header("Accept-Encoding", "gzip, deflate")
        return req

    def http_response(self, req, resp):
        old_resp = resp
# gzip
        if resp.headers.get("content-encoding") == "gzip":
            gz = GzipFile(
            fileobj=StringIO(resp.read()),
            mode="r"
            )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
            resp.msg = old_resp.msg
# deflate
        if resp.headers.get("content-encoding") == "deflate":
            gz = StringIO( deflate(resp.read()) )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
            resp.msg = old_resp.msg
        return resp

# deflate support
import zlib
def deflate(data):   # zlib only provides the zlib compress format, not the deflate format;
    try:               # so on top of all there's this workaround:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)


def Link_exists(url):
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request,timeout=10)
        return True
    except:
        return False

url = 'http://www.ximalaya.com/dq/all/'
request = urllib2.Request(url)
response = urllib2.urlopen(request)
pagecode = response.read()
soup = BeautifulSoup(pagecode, 'lxml')
sound_tag = soup.findAll('a' ,attrs={'class': 'tagBtn'})
xmlybook = xlwt.Workbook()
tablist = []
'''
def hotbook():
    for tag in sound_tag:
        urltab = 'http://www.ximalaya.com%s' % tag['href']
        tablist.append(urltab)
    #    sheet = xmlybook.add_sheet(tag.string, cell_overwrite_ok=True)
        #print tag.string
    tabname = ['悬疑','言情','幻想','历史','都市','文学','武侠','官场商战','经管','社科','QQ阅读',
               '读客图书','果麦文化','中信出版','博集天卷','磨铁阅读','蓝狮子','速播专区','推理世界','正能量有声书']
    x = 0
    for tablink in tablist[:20]:
        tablink = tablink
    #    print tablink
        k = 0
        sheet = xmlybook.add_sheet(tabname[x].decode('utf-8'), cell_overwrite_ok=True)
        numbercode = Soup(tablink)
        pagenumber = numbercode.findAll(name='a', attrs={'class': 'pagingBar_page'})
        numberlist = []
        for numbers in pagenumber:
            numberlist.append(numbers.string)
        try:
            maxpagenumber = int(numberlist[-2]) + 1
        except Exception as a:
            maxpagenumber = 1
        for i in range(1, maxpagenumber):
            print 'start write %s%d' % (tablink[32:], i)
            urltab1 = (tablink + '%s') % i
    #        print urltab1
            try:
                if Link_exists(urltab1) == True:
                    code = Soup(urltab1)
                    links_title = code.findAll(name='a', attrs={'class': 'discoverAlbum_title'})
                    for link in links_title:
                        urltab2 =  link['href']
                        encoding_support = ContentEncodingProcessor
                        opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                        # 直接用opener打开网页，如果服务器支持gzip/defalte则自动解压缩
                        html = opener.open(urltab2).read()
                        tree = etree.HTML(html)
                        title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
                        music_type = tree.xpath("//div[@class='detailContent_category']/a")[0].text
                        tags = tree.xpath("//div[@class='tagBtnList']/a[@class='tagBtn2']/span")
                        tagString = ','.join(i.text for i in tags)
                        updatetime = tree.xpath("//div[@class='detailContent_category']/span")[0].text
                        username = tree.xpath("//div[@class='username']")[0].text
                        username = username.split()[0]
                        try:
                            playcount = tree.xpath("//div[@class='detailContent_playcountDetail']/span")[0].text
                        except Exception as b:
                            logging.exception(b)
                            playcount = 0
                        try:
                            intro = tree.xpath("//div[@class='detailContent_intro']/div[@class='mid_intro']/article")[0].text
                        except Exception as f:
                            logging.exception(f)
                            intro = None
                        sheet.write(k, 0, title)
                        sheet.write(k, 1, music_type)
                        sheet.write(k, 2, tagString)
                        sheet.write(k, 3, updatetime)
                        sheet.write(k, 4, playcount)
                        sheet.write(k, 6, username)
                        sheet.write(k, 5, intro)
                        k += 1
                    print 'write %s%d ok' % (tablink[32:], i)
                xmlybook.save('hotbook.xls')
            except Exception as e:
                logging.exception(e)
        x += 1
        print '%s tab save ok' % tablink[32:]


def newbook():
    for tag in sound_tag:
        urltab = 'http://www.ximalaya.com%s' % tag['href']
        tablist.append(urltab)
    #    sheet = xmlybook.add_sheet(tag.string, cell_overwrite_ok=True)
        #print tag.string
    tabname = ['悬疑','言情','幻想','历史','都市','文学','武侠','官场商战','经管','社科','QQ阅读',
               '读客图书','果麦文化','中信出版','博集天卷','磨铁阅读','蓝狮子','速播专区','推理世界','正能量有声书']
    x = 0
    for tablink in tablist[:20]:
        tablink = tablink + 'recent'
    #    print tablink
        k = 0
        sheet = xmlybook.add_sheet(tabname[x].decode('utf-8'), cell_overwrite_ok=True)
        numbercode = Soup(tablink)
        pagenumber = numbercode.findAll(name='a', attrs={'class': 'pagingBar_page'})
        numberlist = []
        for numbers in pagenumber:
            numberlist.append(numbers.string)
        try:
            maxpagenumber = int(numberlist[-2]) + 1
        except Exception as a:
            maxpagenumber = 1
        for i in range(1, maxpagenumber):
            print 'start write %s%d' % (tablink[32:], i)
            urltab1 = (tablink + '%s') % i
    #        print urltab1
            try:
                if Link_exists(urltab1) == True:
                    code = Soup(urltab1)
                    links_title = code.findAll(name='a', attrs={'class': 'discoverAlbum_title'})
                    for link in links_title:
                        urltab2 =  link['href']
                        encoding_support = ContentEncodingProcessor
                        opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                        # 直接用opener打开网页，如果服务器支持gzip/defalte则自动解压缩
                        html = opener.open(urltab2).read()
                        tree = etree.HTML(html)
                        title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
                        music_type = tree.xpath("//div[@class='detailContent_category']/a")[0].text
                        tags = tree.xpath("//div[@class='tagBtnList']/a[@class='tagBtn2']/span")
                        tagString = ','.join(i.text for i in tags)
                        updatetime = tree.xpath("//div[@class='detailContent_category']/span")[0].text
                        username = tree.xpath("//div[@class='username']")[0].text
                        username = username.split()[0]
                        try:
                            playcount = tree.xpath("//div[@class='detailContent_playcountDetail']/span")[0].text
                        except Exception as b:
                            logging.exception(b)
                            playcount = 0
                        try:
                            intro = tree.xpath("//div[@class='detailContent_intro']/div[@class='mid_intro']/article")[0].text
                        except Exception as f:
                            logging.exception(f)
                            intro = None
                        sheet.write(k, 0, title)
                        sheet.write(k, 1, music_type)
                        sheet.write(k, 2, tagString)
                        sheet.write(k, 3, updatetime)
                        sheet.write(k, 4, playcount)
                        sheet.write(k, 6, username)
                        sheet.write(k, 5, intro)
                        k += 1
                    print 'write %s%d ok' % (tablink[32:], i)
                xmlybook.save('newbook.xls')
            except Exception as e:
                logging.exception(e)
        x += 1
        print '%s tab save ok' % tablink[32:]

'''
def classic():
    for tag in sound_tag:
        urltab = 'http://www.ximalaya.com%s' % tag['href']
        tablist.append(urltab)
    #    sheet = xmlybook.add_sheet(tag.string, cell_overwrite_ok=True)
        #print tag.string
    tabname = ['悬疑','言情','幻想','历史','都市','文学','武侠','官场商战','经管','社科','QQ阅读',
               '读客图书','果麦文化','中信出版','博集天卷','磨铁阅读','蓝狮子','速播专区','推理世界','正能量有声书']
    x = 0
    for tablink in tablist[:20]:
        tablink = tablink + 'classic'
    #    print tablink
        k = 0
        sheet = xmlybook.add_sheet(tabname[x].decode('utf-8'), cell_overwrite_ok=True)
        numbercode = Soup(tablink)
        pagenumber = numbercode.findAll(name='a', attrs={'class': 'pagingBar_page'})
        numberlist = []
        for numbers in pagenumber:
            numberlist.append(numbers.string)
        try:
            maxpagenumber = int(numberlist[-2]) + 1
        except Exception as a:
            maxpagenumber = 1
        for i in range(1, maxpagenumber):
            print 'start write %s%d' % (tablink[32:], i)
            urltab1 = (tablink + '%s') % i
    #        print urltab1
            try:
                if Link_exists(urltab1) == True:
                    code = Soup(urltab1)
                    links_title = code.findAll(name='a', attrs={'class': 'discoverAlbum_title'})
                    for link in links_title:
                        urltab2 =  link['href']
                        encoding_support = ContentEncodingProcessor
                        opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                        # 直接用opener打开网页，如果服务器支持gzip/defalte则自动解压缩
                        html = opener.open(urltab2).read()
                        tree = etree.HTML(html)
                        title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
                        music_type = tree.xpath("//div[@class='detailContent_category']/a")[0].text
                        tags = tree.xpath("//div[@class='tagBtnList']/a[@class='tagBtn2']/span")
                        tagString = ','.join(i.text for i in tags)
                        updatetime = tree.xpath("//div[@class='detailContent_category']/span")[0].text
                        username = tree.xpath("//div[@class='username']")[0].text
                        username = username.split()[0]
                        try:
                            playcount = tree.xpath("//div[@class='detailContent_playcountDetail']/span")[0].text
                        except Exception as b:
                            logging.exception(b)
                            playcount = 0
                        try:
                            intro = tree.xpath("//div[@class='detailContent_intro']/div[@class='mid_intro']/article")[0].text
                        except Exception as f:
                            logging.exception(f)
                            intro = None
                        sheet.write(k, 0, title)
                        sheet.write(k, 1, music_type)
                        sheet.write(k, 2, tagString)
                        sheet.write(k, 3, updatetime)
                        sheet.write(k, 4, playcount)
                        sheet.write(k, 6, username)
                        sheet.write(k, 5, intro)
                        k += 1
                    print 'write %s%d ok' % (tablink[32:], i)
                xmlybook.save('classicbook.xls')
            except Exception as e:
                logging.exception(e)
        x += 1
        print '%s tab save ok' % tablink[32:]

#hotbook()
#newbook()
classic()
print 'All ok!'
