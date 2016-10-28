# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
#from scrapy import log
import pymongo

class XmlyspiderPipeline(object):
    def process_item(self, item, spider):
        def __init__(self):
            self.server = settings['MONGODB_SERVER']
            self.port = settings['MONGODB_PORT']
            self.db = settings['MONGODB_DB']
            self.tab = settings['MONGODB_COLLECTION']
            connection = pymongo.MongoClient(self.server, self.port)
            db = connection[self.db]
            self.collection = db[self.tab]

        def process_item(self, item, spider):
            self.collection.insert(dict(item))
            return item
