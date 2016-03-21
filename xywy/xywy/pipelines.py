# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from twisted.enterprise import adbapi

import MySQLdb.cursors

class ExpertPipeline(object):
    def __init__(self):
        self.file = codecs.open('tmp.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class DepartmentPipeline(object):
    def __init__(self):
        self.file = codecs.open('tmp.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class CirclePipeline(object):
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
        print item["circle_owner_id"]
        conn.execute("select * from circle where circle_name = '%s' " % item['circle_name'])
        ret = conn.fetchone()
        if ret:
            pass
        else :
            conn.execute("""
                    insert into circle(circle_name, circle_circle_intro, circle_suffer_number, circle_expert_number,
                    circle_topic_number, circle_owner_id) values(%s, %s, %s, %s, %s, %s)""",
                    (item["circle_name"], item["circle_circle_intro"], item["circle_suffer_number"], item["circle_expert_number"],
                    item["circle_topic_number"], item["circle_owner_id"]))

# class HospitalPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('tmp.json', 'w', 'utf-8')
#
#     def process_item(self, item, spider):
#         # print item['hospital_intro']
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item
#
#     def spider_closed(self, spider):
#         self.file.close()

class HospitalPipeline(object):
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
        conn.execute("select * from hospital where hospital_name = '%s' " % item['hospital_name'])
        ret = conn.fetchone()
        if ret:
            pass
        else :
            conn.execute("""
                    insert into hospital(hospital_name, hospital_intro, hospital_address,
                       hospital_phone, hospital_image_online_number, hospital_register_number,
                       hospital_appointment, hospital_department_number, hospital_expert_number,
                       hospital_score, hospital_number_experience) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (item["hospital_name"], item["hospital_intro"], item["hospital_address"], item["hospital_phone"],
                    item["hospital_image_online_number"], item["hospital_register_number"], item["hospital_appointment"],
                      item["hospital_department_number"], item["hospital_expert_number"], item["hospital_score"],
                      item["hospital_number_experience"]))


