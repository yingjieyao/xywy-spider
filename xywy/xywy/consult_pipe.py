# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from twisted.enterprise import adbapi

import MySQLdb.cursors

class ConsultPipeline(object):
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
        conn.execute("select e_consult_id from e_consult where e_consult_id = '%s'" % item['consult_id'])
        ret = conn.fetchone()
        if ret:
            return item
        conn.execute("select e_expert_id from e_expert where e_expert_url = '%s'" % (item['expert_url']))
        ret = conn.fetchone()
        ret['e_expert_id']
        conn.execute("""
                insert into e_consult(e_consult_id, e_expert_id, e_consult_owner_id, e_consult_illness, e_consult_illness_detail,
                e_consult_previous, e_consult_want_help, e_consult_date, e_consult_analysis, e_consult_suggest, e_consult_reply_date,
                e_consult_like_number, e_consult_dislike_number) values(%s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
                """ % (item['consult_id'], ret['e_expert_id'], item['patient_id'], item['illness'], item['illness_detail'], item['previous'],
                    item['want_help'], item['date'], item['analysis'], item['suggest'], item['reply_date'], item['like_number'],
                    item['dislike_number']))
        # ans = conn.fetchone()
        # if ans:
        #     return item
        # conn.execute("""
        #         insert into e_order(e_order_id, e_order_location, e_expert_id, e_order_illness,
        #         e_order_time, e_order_type) values(%s, '%s', %s, '%s', '%s', '%s') """ %
        #         (item['order_id'], item['location'], ret['e_expert_id'], item['illness'], item['time'], item['order_type']))
        # print ret['e_expert_id']

        return item


