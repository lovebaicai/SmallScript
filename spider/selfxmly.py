#!/usr/bin/env python
#-*- coding:utf-8-*-
import re
import csv
import urllib, urllib2
from bs4 import BeautifulSoup
import xlwt

def Soup(url):
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
        pagecode = response.read()
        soup = BeautifulSoup(pagecode, 'lxml')
    except urllib2.URLError, e:
        pass
    return soup

url = 'http://www.ximalaya.com/dq/all/'
request = urllib2.Request(url)
response = urllib2.urlopen(request)
pagecode = response.read()
soup = BeautifulSoup(pagecode, 'lxml')
sound_tab = soup.findAll('a' ,attrs={'hashlink': '#explore_album_detail_entry'})
xmlybook = xlwt.Workbook()

for tab in sound_tab:
    x = 0
    k = 0
    urltab = 'http://www.ximalaya.com/%s' % tab['href']
    if tab['href'] == '/dq/poem/':
        break
    #print tab['href']
    print tab.string
    sheet = xmlybook.add_sheet(tab.string, cell_overwrite_ok=True)
    #sheet.write(0, 0, k)
    #k += 1
    #xmlybook.save('workxmly.xls')
    print '%s tab start save' % tab.string
    for i in range(1, 85):
        urltab2 = (urltab + '%s') % i
        print 'start write %s%d' % (tab.string, i)

        code  = Soup(urltab2)

        links_title = code.findAll(name='a', attrs={'class': 'discoverAlbum_title'})
        for link in links_title:
            sheet.write(k, 0, link.string)
            sheet.write(k, 1, link['href'])
            k += 1
            #xmlybook.save('workxmly.xls')
            #print 'save title link is ok'

        playcount = code.findAll('span', attrs={'class': 'sound_playcount'})
        for count in playcount:
            #sound_count = count.string
            sheet.write(x,2,count.string)
            x += 1
        print 'write %s%d ok' % (tab.string, i)
    xmlybook.save('workxmly.xls')        #xmlybook.save('workxmly.xls')
    print '%s tab save ok' % tab.string
        #print 'write %s%d is ok' % (tab.string, i)

print 'All ok!'
