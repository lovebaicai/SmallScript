#-*-coding:utf-8-*-

import json
import requests
import scrapy
from datetime import datetime
from ..items import XmlyspiderItem


class XimalayaSpider(scrapy.Spider):
    name = 'xmly'
    allowed_domains = ['http://ximalaya.com/']
    start_urls = (
        'http://mobile.ximalaya.com/mobile/discovery/v2/category/metadata/albums?'
        'calcDimension=hot&categoryId=33&device=android&pageId=1&pageSize=620&version=5.4.39',
    )

    def parse(self, response):
        pagecode = json.loads(response.body)['list']
        #print pagecode
        item = XmlyspiderItem()
        for info in pagecode:
            item['Albumtitle'] = info['title']
            item['Albumscore'] = info['score']
            item['TotalPlayCounts'] = info['playsCounts']
            item['displayDiscountedPrice'] = info['displayDiscountedPrice']
            AlbumId = info['albumId']
            albumurl = (
               'http://mobile.ximalaya.com/mobile/v1/album/track?albumId=%s&device=android&pageId=1&pageSize=200'
               ) % AlbumId
            yield scrapy.Request(albumurl, callback=self.parse_album, meta={'item': item})
        #yield scrapy.http.Request(albumurl, callback=self.parse_album)
        #     #yield item
        #     #print 'code'
        #     #print item['Title']

    def parse_album(self, response):
        code = json.loads(response.body)['data']['list'][0]
        #print 'code'
        item = response.meta['item']
        for info1 in code:
            item['Title'] = info1['title']
            item['Nickname'] = info1['nickname']
            item['SinglePlayCount'] = info1['playtimes']
            CreatedTime = int(info1['createdAt']) / 1000
            item['CreatedTime'] = datetime.fromtimestamp(CreatedTime).strftime('%Y-%m-%d')
            item['Duration'] = info1['duration']
            item['LikeCount'] = info1['likes']
            item['CommentsCount'] = info1['comments']
            trackId = info1['trackId']
            singleurl = 'http://www.ximalaya.com/tracks/%s.json' % trackId
            item['category_title'] = json.loads(requests.get(singleurl).content)['category_title']
            yield item
