#!/usr/bin/env python
#-*- coding:utf-8-*-
import logging
import MySQLdb as mdb
from lxml import etree
from gzip import GzipFile
from StringIO import StringIO
import urllib2
import time
from bs4 import BeautifulSoup
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def Link_exists(url):
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except:
        return False

#服务器支持gzip/defalte则自动解压缩
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

def Soup(url):
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request, timeout=20)
        pagecode = response.read()
        soup = BeautifulSoup(pagecode, 'lxml')
        return soup
    except urllib2.URLError, e:
        pass

urlhost = []
url = 'http://www.ximalaya.com/dq/all/'
soup = Soup(url)
sound_tag = soup.findAll('a' ,attrs={'class': 'tagBtn'})
urllist = []
for tag in sound_tag:
    urltab = 'http://www.ximalaya.com%s' % tag['href']     #urltab是大分类链接
    numbercode = Soup(urltab)
    pagenumber = numbercode.findAll(name='a', attrs={'class': 'pagingBar_page'})
    numberlist = [] #获取分类下页面最大数
    for numbers in pagenumber:
        numberlist.append(numbers.string)
    try:
        maxpagenumber = int(numberlist[-2]) + 1
    except Exception as a:
        maxpagenumber = 1
    for i in range(1, maxpagenumber):
        urltab2 = (urltab + '%s') % i
#           print '开始抓取%s,第%s页数据' % (tag.string, i)
#        print urltab2
        if Link_exists(urltab2) == True:
            code  = Soup(urltab2)
            links_title = code.findAll(name='a', attrs={'class': 'discoverAlbum_title'})
        for link in links_title:
#            print link['href']
            encoding_support = ContentEncodingProcessor
            opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
            html = opener.open(link['href']).read()
            pagetree = etree.HTML(html)
            pagenu = pagetree.xpath("//@data-page")        #获取专辑下节目最大页数
            try:
                maxpage = pagenu[-2]
            except Exception as e:
                #logging.exception(e)
                maxpage = 1
                pass
#            for link in links_title:
            for p in range(1, int(maxpage)+1):
                aurl = link['href'] + '?page=' + str(p)     #aurl是album链接
#                print aurl

#                   print '开始爬取%s,第%s页数据' % (link.string, p)
                encoding_support = ContentEncodingProcessor
                opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                # 直接用opener打开网页，如果服务器支持gzip/defalte则自动解压缩
                html = opener.open(aurl).read()
                ttree = etree.HTML(html)
                sound_id = ttree.xpath("//@sound_ids")       #获取节目id
                urlid = sound_id[0].split(",")
                for id in urlid:
                    if id != '':
                        jsonurl = 'http://www.ximalaya.com/tracks/%s.json' %  id
                        #print jsonurl
                        urllist.append(jsonurl)
                        with open('url.txt', 'a+') as x:
                            x.write(jsonurl + '\n')

        print '%s%s页wirte ok' % (tag.string, i)
    print '%s write ok!!!!!!!!!!!!!!!!' % tag.string

print 'append ok'

