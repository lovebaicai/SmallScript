# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
#from scrapy import log
import pymongo
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# #Mongo
# class XmlyspiderPipeline(object):
#     def __init__(self):
#         self.server = settings['MONGODB_SERVER']
#         self.port = settings['MONGODB_PORT']
#         self.db = settings['MONGODB_DB']
#         self.tab = settings['MONGODB_COLLECTION']
#         connection = pymongo.MongoClient(self.server, self.port)
#         db = connection[self.db]
#         self.collection = db[self.tab]
#
#     def process_item(self, item, spider):
#         self.collection.insert(dict(item))
#         return item

#Mysql
class XmlyMysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost", user="root", passwd="ubuntu", db="sound", charset="utf8")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(
                "create table paidsound(id int PRIMARY KEY AUTO_INCREMENT,Albumtitle varchar (255), Albumscore varchar(255),"
                "TotalPlayCounts VARCHAR(255), displayDiscountedPrice VARCHAR(255), Title VARCHAR (255), "
                "Nickname VARCHAR (255), SinglePlayCount VARCHAR (255), CreatedTime VARCHAR (255), Duration VARCHAR (255),"
                "LikeCount VARCHAR (255), CommentsCount VARCHAR (255), category_title VARCHAR (255))")
        except:
            pass

    def process_item(self, item, spider):
        self.cursor.execute(
            "insert into paidsound(Albumtitle, Albumscore, TotalPlayCounts, displayDiscountedPrice, Title, Nickname, " \
            "SinglePlayCount, CreatedTime, Duration, LikeCount, CommentsCount, category_title) values " \
            "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
             % (item['Albumtitle'], item['Albumscore'], item['TotalPlayCounts'], item['displayDiscountedPrice'],
                  item['Title'], item['Nickname'], item['SinglePlayCount'], item['CreatedTime'],
                  item['Duration'],item['LikeCount'], item['CommentsCount'], item['category_title']))
        self.conn.commit()


