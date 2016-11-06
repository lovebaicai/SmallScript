# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XmlyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Albumtitle = scrapy.Field()
#    AlbumId = scrapy.Field()
    Albumscore = scrapy.Field()
    TotalPlayCounts = scrapy.Field()
    displayDiscountedPrice = scrapy.Field()
    Title = scrapy.Field()
    Nickname = scrapy.Field()
    SinglePlayCount = scrapy.Field()
    CreateTime = scrapy.Field()
    Duration = scrapy.Field()
    LikeCounts = scrapy.Field()
    CommentsCount = scrapy.Field()
    category = scrapy.Field()
