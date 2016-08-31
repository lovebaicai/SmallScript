#!/usr/bin/env python
#-*- coding:utf-8-*-
import urllib2
from bs4 import BeautifulSoup
import xlwt
from lxml import etree
import sys
from gzip import GzipFile
from StringIO import StringIO
reload(sys)
sys.setdefaultencoding("utf-8")


def Soup(url):
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
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

url = 'http://www.ximalaya.com/dq/all/'
request = urllib2.Request(url)
response = urllib2.urlopen(request)
pagecode = response.read()
soup = BeautifulSoup(pagecode, 'lxml')
sound_tag = soup.findAll('a' ,attrs={'class': 'tagBtn'})

for tag in sound_tag:
    x = 0
    k = 0
    urltab = 'http://www.ximalaya.com%s' % tag['href']
    print '%s tab start save' % tag.string
    for i in range(1, 85):
        urltab2 = (urltab + '%s') % i
        print 'start write %s%d' % (tag.string, i)
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
        # playcount = tree.xpath("//div[@class='soundContent_playcount']")[0].text
        playcount = tree.xpath("//div[@class='detailContent_playcountDetail']/span")[0].text
        intro = tree.xpath("//div[@class='detailContent_intro']/div[@class='mid_intro']/article")[0].text
        username = tree.xpath("//div[@class='username']")[0].text
        username = username.split()[0]
        try:
            writer.writerow((title.encode('utf-8', 'ignore'), username.encode('utf-8', 'ignore'),surl.encode('utf-8', 'ignore'),music_type.encode('utf-8', 'ignore'), tagString.encode('utf-8', 'ignore'),mp3duration.encode('utf-8', 'ignore'), playcount.encode('utf-8', 'ignore'),likecount.encode('utf-8', 'ignore'), commentcount.encode('utf-8', 'ignore')))
        except Exception as e:
            logging.exception(e)
        print 'write %s%d ok' % (tag.string, i)
    xmlybook.save('uptabxmly.xls')
    print '%s tab save ok' % tag.string

print 'All ok!'
