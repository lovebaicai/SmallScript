# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy import Item, Field

class MarketItem(Item):
    url = Field()
    nid = Field()
    title = Field()
    pic_url = Field()
