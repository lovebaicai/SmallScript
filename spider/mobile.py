#!/usr/bin/env python
#-*- coding:utf-8-*-
import time
import datetime
import logging
import MySQLdb as mdb
from lxml import etree
from gzip import GzipFile
from StringIO import StringIO
import urllib2
from bs4 import BeautifulSoup
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#定义soup解析网页
def Soup(url):
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request, timeout=20)
        pagecode = response.read()
        soup = BeautifulSoup(pagecode, 'lxml')
        return soup
    except urllib2.URLError, e:
        pass
#判断link是否存在
def Link_exists(url):
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    try:
        response = urllib2.urlopen(request)
        return True
    except:
        return False

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
'''
con = mdb.connect('localhost', 'root', 'ubuntu', 'sound', charset='utf8')
cur = con.cursor()
try:
    cur.execute("create table testsound(title varchar(255), nickname VARCHAR(255), play_count VARCHAR(255), sound_time VARCHAR (255), album_title VARCHAR (255), category_title VARCHAR (255), coumments_count varchar(255), favorites_count varchar(255), soundurl varchar(255), albumurl varchar(255))")
except Exception as e:
    pass
'''


con = mdb.connect('localhost', 'root', 'ubuntu', 'sound', charset='utf8')
cur = con.cursor()
cur.execute("SET NAMES utf8")

try:
    cur.execute("create table albumsound(id int PRIMARY KEY AUTO_INCREMENT, albumtitle varchar(255), "
                "music_type VARCHAR (255),author VARCHAR(255),playcount VARCHAR (255), tag VARCHAR(255), "
                "starttime varchar (255), endtime varchar(255), albumurl varchar(255))")
except Exception as e:
    pass

maxpage = 3
url = 'http://www.ximalaya.com/5359104/album/3422231'

aurl = url    #aurl是album链接

encoding_support = ContentEncodingProcessor
opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
html = opener.open(aurl).read()
tree = etree.HTML(html)
albumtitle = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
music_type = tree.xpath("//div[@class='detailContent_category']/a")[0].text
tags = tree.xpath("//div[@class='tagBtnList']/a[@class='tagBtn2']/span")
tagString = ','.join(i.text for i in tags)
updatetime = tree.xpath("//div[@class='detailContent_category']/span")[0].text
username = tree.xpath("//div[@class='username']")[0].text
username = username.split()[0]
try:
    playcount = tree.xpath("//div[@class='detailContent_playcountDetail']/span")[0].text
except Exception as b:
    playcount = 0
try:
    intro = tree.xpath("//div[@class='detailContent_intro']/div[@class='mid_intro']/article")[0].text
except Exception as f:
    intro = None
uploadtimes = tree.xpath("//div[@class='miniPlayer3']/div[@class='operate']/span")
timelist = [times.text.replace('-', '', 2) for times in uploadtimes]
starttime = min(timelist)
if maxpage == 1:
    starttime = starttime
else:
    url2 = aurl + '?page=' + str(maxpage)     #aurl是album链接
    encoding_support = ContentEncodingProcessor
    opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
    html = opener.open(url2).read()
    pagetree1 = etree.HTML(html)
    uploadtimes1 = tree.xpath("//div[@class='miniPlayer3']/div[@class='operate']/span")
    timelist1 = [times.text.replace('-', '', 2) for times in uploadtimes]
    starttime1 = min(timelist1)
    if starttime1 < starttime:
        starttime = starttime1
print albumtitle, music_type, username, playcount, tagString, starttime, updatetime, aurl

try:
   cur.execute(
       "insert into albumsound(albumtitle, music_type, author, playcount, tag, starttime, endtime, albumurl)"
       "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        % (albumtitle, music_type, username, playcount, tagString, starttime, updatetime, aurl))
#               con.commit()
except Exception as f:
    logging.exception(f)
cur.close()
con.commit()
con.close()
