# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
from twisted.enterprise import adbapi

import MySQLdb.cursors

class SharePipeline2(object):
    def __init__(self):
        self.file = codecs.open('topic_id.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if item['topic_id']:
            self.file.write(item['topic_id'] + '\n')

        return item

    def spider_closed(self, spider):
        self.file.close()

class SharePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWD'],
                charset = 'utf8',
                cursorclass= MySQLdb.cursors.DictCursor,
                use_unicode = True,
                )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d =self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return d

    def _do_upinsert(self, conn, item, spider):
        conn.execute("SET NAMES utf8")
        conn.execute("select y_topic_id from y_topic where y_topic_id = %s" % item['topic_id'])
        ret = conn.fetchone()
        if ret:
            return item
        conn.execute("""
                insert into y_topic(y_topic_id, y_topic_title, y_topic_reply_number, y_topic_like_number,
                y_topic_owner_url, y_topic_view_number, y_topic_follow_number, y_topic_type, y_topic_owner_type, y_topic_content)
                values(%s, '%s', %s, %s, '%s', %s, %s, '%s', '%s', '%s') """ %
                (item['topic_id'], item['title'], item['reply_number'], item['like_number'], item['owner_url'],
                    item['view_number'], item['follow_number'], item['topic_type'], item['owner_type'], item['content']))

        return item

class ReplyPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWD'],
                charset = 'utf8',
                cursorclass= MySQLdb.cursors.DictCursor,
                use_unicode = True,
                )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        d =self.dbpool.runInteraction(self._do_upinsert, item, spider)
        return d

    def _do_upinsert(self, conn, item, spider):
        # print item['doctor']['name']
#         conn.execute("SET NAMES utf8")
#         conn.execute("select y_reply_id from y_reply where y_reply_id = %s" % item['reply_id'])
#         ret = conn.fetchone()
#         if ret:
#             return item
#
#         conn.execute("""
#                 insert into y_reply(y_reply_id, y_topic_id, y_doctor_id, y_reply_content, y_reply_like_number, y_reply_date,
#                 y_reply_follow_content, y_reply_follow_doctor_id, y_reply_follow_date) values(%s, %s, %s, '%s', '%s', '%s',
#                 '%s', '%s', '%s') """ % (item['reply_id'], item['topic_id'], item['doctor_id'], item['reply_content'],
#                     item['reply_like_number'], item['reply_date'], item['reply_follow_content'], item['follow_doctor_id'],
#                     item['follow_date']))
#
#         return item
#
#
#
