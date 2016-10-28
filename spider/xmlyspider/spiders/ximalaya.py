#-*-coding:utf-8-*-

import json
import requests
import scrapy
from datetime import datetime
from ximalayaspier.items import XmlyspiderItem

class XimalayaSpider(scrapy.Spider):
    name = 'xmly'
    allowed_domains = ['http://mobile.ximalaya.com/']
    start_urls = [
        'http://mobile.ximalaya.com/mobile/discovery/v2/category/metadata/albums?calcDimension=hot&categoryId=33&device=android&pageId=1&pageSize=620&version=5.4.39'
    ]

    def parse(self, response):
        pagecode = json.loads(response.body)['list']
        item = XmlyspiderItem()
        for info in pagecode:
            item['Albumtitle'] = info['title']
#            item['AlbumId'] = info['albumId']
            item['Albumscore'] = info['score']
            item['TotalPlayCounts'] = info['playsCounts']
            item['displayDiscountedPrice'] = info['displayDiscountedPrice']
            AlbumId = info['albumid']
            albumurl = ('http://mobile.ximalaya.com/mobile/v1/album/track?albumId='
                        '%s&device=android&pageId=1&pageSize=200') % AlbumId
            yield scrapy.Request(albumurl, callback=self.parse_album)


    def parse_album(self, response):
        pagecode = json.loads(response.body)['data']['list']
        item = XmlyspiderItem()
        for info in pagecode:
            item['Title'] = info['title']
            item['Nickname'] = info['nickname']
            item['SinglePlayCount'] = info['playtimes']
            CreatedTime = int(info['createdAt']) / 1000
            item['CreatedTime'] = datetime.fromtimestamp(CreatedTime).strftime('%Y-%m-%d')
            item['Duration'] = info['duration']
            item['LikeCount'] = info['likes']
            item['CommentsCount'] = info['comments']
            trackId = info['trackId']
            singleurl = 'http://www.ximalaya.com/tracks/%s.json' % trackId
            item['category_title'] = json.loads(requests.get(singleurl).content)['category_title']
            yield item




