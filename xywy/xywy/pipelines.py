# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors

class CirclePipeline(object):
    def __init__(self):
        self.file = codecs.open('circle.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

# class CirclePipeline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbargs = dict(
#                 host = settings['MYSQL_HOST'],
#                 db = settings['MYSQL_DBNAME'],
#                 user = settings['MYSQL_USER'],
#                 passwd = settings['MYSQL_PASSWD'],
#                 charset = 'utf8',
#                 cursorclass= MySQLdb.cursors.DictCursor,
#                 use_unicode = True,
#                 )
#         dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         d =self.dbpool.runInteraction(self._do_upinsert, item, spider)
#         return d
#
#     def _do_upinsert(self, conn, item, spider):
#         conn.execute("SET NAMES utf8")
#         print item["circle_owner_id"]
#         conn.execute("select * from circle where circle_name = '%s' " % item['circle_name'])
#         ret = conn.fetchone()
#         if ret:
#             pass
#         else :
#             conn.execute("""
#                     insert into circle(circle_name, circle_circle_intro, circle_suffer_number, circle_expert_number,
#                     circle_topic_number, circle_owner_id) values(%s, %s, %s, %s, %s, %s)""",
#                     (item["circle_name"], item["circle_circle_intro"], item["circle_suffer_number"], item["circle_expert_number"],
#                     item["circle_topic_number"], item["circle_owner_id"]))
