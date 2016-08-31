#!/usr/bin/env python
#-*- coding:utf-8-*-
#import MYSQLdb
from lxml import etree
from gzip import GzipFile
from StringIO import StringIO
import urllib2
from bs4 import BeautifulSoup
import json
import time
from Queue import Queue
import random
import socket
import threading
import traceback
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

socket.setdefaulttimeout(20)
PgEr = 0
queue = Queue(200)

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

class Ximalaya(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.host = 'http://www.ximalaya.com'
        self.client = MongoClient()
        self.db = self.client.sound
        self.soundInfo = self.db.sound
        self.AgsEr = 0
        self.SdEr = 0
        self.ClgEr = 0

        self.headers = {'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,zh-TW;q=0.2',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Host': 'www.ximalaya.com',
                        'Connection': 'Keep-Alive',
                        }

        def run(self):
            while not exit_flag.is_set():
                time.sleep(random.uniform(1,3))
                album_url = self.queue_in.get()
                self.albumGetSounds(album_url)
                self.queue_in.task_done()
                print '*** Album done, url: %s, Queue: %s, Queue_in: %s, Page: %s ***' % (album_url, self.queue.qsize(), self.queue_in.qsize(), page)

        def albumGenSounds(self, ab_url):
            try:
                encoding_support = ContentEncodingProcessor
                opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                # 直接用opener打开网页，如果服务器支持gzip/defalte则自动解压缩
                html = opener.open(ab_url).read()
                tree = etree.HTML(html)
                sound_urls = tree.xpath("//div[@class='miniPlayer3']/a/@href")
                if sound_urls:
                    for sound_url in sound_urls:
                        sound_url = self.host + sound_url
                        exists_flag = self.soundInfo_find(sound_url)
                        if not exists_flag:
                            print '>>> Sound put %s, Queue: %s, Queue_in: %s, Page: %s' % (sound_url, self.queue.qsize(), self.queue_in.qsize(), page)
                        else:
                            pass
            except Exception as e:
                print '***albumGetSounds error, error: %s, album url: %s' % (e, ab_url)
                print traceback.print_exc()
                self.AgsEr += 1
                if self.AgsEr < 3:
                    time.sleep(15)
                    self.albumGetSounds(ab_url)

        def soundpage(self, a_url, a_title, s_url):
            try:
                encoding_support = ContentEncodingProcessor
                opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
                # 直接用opener打开网页，如果服务器支持gzip/defalte则自动解压缩
                html = opener.open(s_url).read()
                tree = etree.HTML(html)




