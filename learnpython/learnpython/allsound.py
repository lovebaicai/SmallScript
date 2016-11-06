#!/usr/bin/env python
#-*- coding:utf-8-*-
import urllib
from lxml import etree
import xlwt
import urllib2
from bs4 import BeautifulSoup
#import xlwt
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def Soup(url):
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request, timeout=20)
        pagecode = response.read()
        soup = BeautifulSoup(pagecode, 'lxml')
        return soup
    except urllib2.URLError, e:
        pass

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
#xmlybook = xlwt.Workbook()
host = 'http://www.ximalaya.com'
csvFile = open('sound.csv','w+')
writer = csv.writer(csvFile)
writer.writerow(('title','username','url','type','time','playcount','likecount','commentcount'))

for tag in sound_tag:
    urltab = 'http://www.ximalaya.com%s' % tag['href']
    #if tag.string != '英语脱口秀' and tag.string != '日语' and tag.string != '消费' and tag.string != '经管' and tag.string != '古风' and tag.string != '首席诵读':
        #sheet = xmlybook.add_sheet(tag.string, cell_overwrite_ok=True)
    for i in range(1, 85):
        urltab2 = (urltab + '%s') % i
        if Link_exists(urltab2) == True:
            code  = Soup(urltab2)
            links_title = code.findAll(name='a', attrs={'class': 'discoverAlbum_title'})
            for link in links_title:
                for p in range(1, 10):
                    aurl = link['href'] + '?page=' + str(p)
                    html = urllib.urlopen(aurl).read()
                    ttree = etree.HTML(html)
                    sound_urls = ttree.xpath("//div[@class='miniPlayer3']/a/@href")
                    album_title = ttree.xpath("//div[@class='detailContent_title']/h1")[0].text
                    for surl in sound_urls:
                        surl =  host + surl
                        #print surl
                        html = urllib.urlopen(surl).read()
                        tree = etree.HTML(html)
                        title = tree.xpath("//div[@class='detailContent_title']/h1")[0].text
                        music_type = tree.xpath("//div[@class='detailContent_category']/a")[0].text
                        tags = tree.xpath("//div[@class='tagBtnList']/a[@class='tagBtn2']/span")
                        tagString = ','.join(i.text for i in tags)
                        playcount = tree.xpath("//div[@class='soundContent_playcount']")[0].text
                        likecount = tree.xpath("//a[@class='likeBtn link1 ']/span[@class='count']")[0].text
                        commentcount = tree.xpath("//a[@class='commentBtn link1']/span[@class='count']")[0].text
                        forwardcount = tree.xpath("//a[@class='forwardBtn link1']/span[@class='count']")[0].text
                        mp3duration = tree.xpath("//div[@class='sound_titlebar']/div[@class='fr']/span[@class='sound_duration']")[
                        0].text
                        username = tree.xpath("//div[@class='username']")[0].text
                        username = username.split()[0]
                        #print title, username, surl, music_type, mp3duration, playcount, likecount, commentcount
                        print '%s write start' % title
                        writer.writerow((title.encode('utf-8', 'ignore'), username.encode('utf-8', 'ignore'),
                                         surl.encode('utf-8', 'ignore'),
                                         music_type.encode('utf-8', 'ignore'), mp3duration.encode('utf-8', 'ignore'),
                                         playcount.encode('utf-8', 'ignore'),
                                         likecount.encode('utf-8', 'ignore'), commentcount.encode('utf-8', 'ignore')))
                        print '%s write ok!!!!' % title

print 'All save ok. Fuck xmly!!!!!'
