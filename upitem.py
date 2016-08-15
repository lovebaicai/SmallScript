#!/usr/bin/env python
#-*- coding:utf-8-*-
import xlwt
import urllib2
from bs4 import BeautifulSoup
import csv
from lxml import etree
import logging
import sys
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
        response = urllib2.urlopen(request)
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

for tag in sound_tag:
    k = 0
    urltab = 'http://www.ximalaya.com%s' % tag['href']
    sheet = xmlybook.add_sheet(tag.string, cell_overwrite_ok=True)
    for i in range(1, 85):
        print 'start write %s%d' % (tag.string, i)
        urltab1 = (urltab + '%s') % i
        try:
            if Link_exists(urltab1) == True:
                code = Soup(urltab1)
                links_title = code.findAll(name='a', attrs={'class': 'discoverAlbum_title'})
                for link in links_title:
                    urltab2 =  link['href']
                    introcode = Soup(urltab2)
                    intros = introcode.findAll('div', attrs={'class': 'mid_intro'})
                    for intro in intros:
                        intro = intro.article.string
                    playcounts = introcode.findAll('div', attrs={'class': 'detailContent_playcountDetail'})
                    for count in playcounts:
                        playcount  = count.span.string
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
                    sheet.write(k, 0, title)
                    sheet.write(k, 1, music_type)
                    sheet.write(k, 2, tagString)
                    sheet.write(k, 3, updatetime)
                    sheet.write(k, 4, playcount)
                    sheet.write(k, 5, intro)
                    sheet.write(k, 6, username)
                    k += 1
                print 'write %s%d ok' % (tag.string, i)
            xmlybook.save('uptabxmly.xls')
        except Exception as e:
            logging.exception(e)
    print '%s tab save ok' % tag.string

print 'All ok!'
