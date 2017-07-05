#-*- coding:utf-8 -*-

import logging
from market.items import MarketItem
from scrapy_redis.spiders import RedisSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
#from scrapy.spiders import CrawlSpider, Rule


class MarketSpider(RedisSpider):
    """Follow categories and extract links."""
    name = 'market'
    redis_key = 'market:start_urls'

    def parse(self, response):
        item = MarketItem()
        url = response.url
        logging.info(response.url)
        title = response.xpath('//*[@id="jGoodsH1"]/text()')[0]
        pic_url = 'http:' + response.xpath('//*[@id="gd-details"]/div[2]/div/div/p[2]/img[1]/@src')[0]
        nid = response.xpath('//*[@id="jColGoods"]/@data-product-id')[0]

        item = {}
        item['title'] = title
        item['nid'] = nid
        item['pic_url'] = pic_url
        item['url'] = url

        yield item

