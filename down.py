#!/usr/bin/env python
import urllib,urllib2
from bs4 import BeautifulSoup
import re

url = 'http://www.opclass.com/index.php/archives/1317/'
request = urllib2.Request(url)
response = urllib2.urlopen(request)
pagecode = response.read()
soup = BeautifulSoup(pagecode,'lxml')
links = soup.findAll(name='a', attrs={'href':re.compile('^http?://.*?flv')})
titles = soup.findAll(name='a',target='_blank' )
i = 1
for link in links:
    try:
        print 'Down start...'
        urllib.urlretrieve(link['href'],(str(i)+link.string+'.flv'))
        i += 1
        print ('Down %s successful...' % link.string)
    except:
        print 'error'
