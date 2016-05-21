# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

from twisted.enterprise import adbapi

import MySQLdb.cursors

class ExpertPipeline2(object):
    def __init__(self):
        self.file1 = codecs.open('d_article_url.json', 'w', encoding='utf-8')
        self.file2 = codecs.open('d_vote_url.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        if item['e_expert_url'] != "":
            # line = json.dumps(item['e_expert_url']) + "\n"
            self.file1.write(item['e_expert_url'] + '\n')
            self.file2.write(item['e_expert_home_url'] + '\n')
        return item

    def spider_closed(self, spider):
        self.file.close()

class EappointmentPipeline(object):
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
        conn.execute("select e_expert_id from e_expert where e_expert_url = '%s'" % item['expert_url'])
        ret = conn.fetchone()
        if not ret:
            return item
        # print ret['e_expert_id']
        # conn.execute("select * from e_order where e_order_id = '%s'" % (item['order_id']))
        # ans = conn.fetchone()
        # if ans:
        #     return item
        conn.execute("""
                insert into e_appointment(e_expert_id, e_appointment_range, e_appointment_region, e_appointment_require
                ) values(%s, '%s', %s, '%s') """ %
                (ret['e_expert_id'], item['e_range'], item['region'], item['require']))
        # print ret['e_expert_id']

        return item



class EorderPipeline(object):
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
        conn.execute("select e_expert_id from e_expert where e_expert_url = '%s'" % item['expert_url'])
        ret = conn.fetchone()
        if not ret:
            return item
        conn.execute("select * from e_order where e_order_id = '%s'" % (item['order_id']))
        ans = conn.fetchone()
        if ans:
            return item
        conn.execute("""
                insert into e_order(e_order_id, e_order_location, e_expert_id, e_order_illness,
                e_order_time, e_order_type) values(%s, '%s', %s, '%s', '%s', '%s') """ %
                (item['order_id'], item['location'], ret['e_expert_id'], item['illness'], item['time'], item['order_type']))
        # print ret['e_expert_id']

        return item



class VotePipeline(object):
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
        conn.execute("select e_expert_id from e_expert where e_expert_home_url = '%s'" % item['e_expert_url'])
        ret = conn.fetchone()
        if not ret:
            return item

        conn.execute("""
                select * from e_vote where e_expert_id = %s and e_vote_illness_name = '%s' """ %
                (ret['e_expert_id'], item['e_vote_illness_name']))
        ans = conn.fetchone()
        if ans:
            return item
        conn.execute("""
                insert into e_vote(e_expert_id, e_vote_illness_name, e_vote_number) values(%s, '%s', '%s')""" %
                (ret['e_expert_id'], item['e_vote_illness_name'], item['e_vote_number']))
        return item


class ArticlePipeline(object):
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
        conn.execute("select e_expert_id from e_expert where e_expert_url = '%s'" % item['home_url'])
        ret = conn.fetchone()
        if not ret:
            return item
        conn.execute("""
                insert into e_article(e_expert_id, e_article_date, e_article_content, e_article_read,
                e_article_like, e_article_dislike, e_article_title) values(%s, '%s', '%s', '%s', '%s', '%s', '%s') """ %
                (ret['e_expert_id'], item['date'], item['content'], item['read'], item['like'], item['dislike'], item['title']))
        conn.execute("""
                select e_article_id from e_article where e_article_title = '%s' """ %
                (item['title']))
        ret = conn.fetchone()
        tag_list = item['tag']
        for tag in tag_list:
            self.__deal_tags(conn, tag, ret['e_article_id'])

    def __deal_tags(self, conn, tag, article_id):
        conn.execute("SET NAMES utf8")
        conn.execute("select e_tag_id from e_tag where e_tag_name = '%s'" % (tag))
        ret = conn.fetchone()
        if not ret:
            conn.execute("""
                    insert into e_tag(e_tag_name) values('%s')  """ % (tag))
            conn.execute("""
                    select e_tag_id from e_tag where e_tag_name = '%s' """ % (tag))
            ret = conn.fetchone()
        conn.execute("""
                insert into  e_article_tag(e_article_id, e_tag_id) values('%s', '%s') """ %
                (article_id, ret['e_tag_id']) )


class DepartmentPipeline(object):
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
        conn.execute("select hospital_id from hospital where hospital_name = '%s' " % item['hospital_name'])
        ret = conn.fetchone()
        if ret:
            print item['hospital_name'], item['e_department_name']
            conn.execute("select * from e_department where e_department_url = '%s' " %
                    (item['url']))
            exi = conn.fetchone()
            if exi:
                pass
            else:
                conn.execute("""
                    insert into e_department(e_department_url, hospital_id, e_department_name, e_department_key, e_department_doc_number,
                    e_department_image, e_department_register_number, e_department_appointment_number, e_department_phone_consult_number,
                    e_department_phone_consult_success_number) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                    (item['url'], ret['hospital_id'], item['e_department_name'], item['e_department_key'], item['e_department_doc_number'],
                        item['e_department_image'], item['e_department_register_number'], item['e_department_appointment_number'],
                        item['e_department_phone_consult_number'], item['e_department_phone_consult_success_number']))

            illness = item['illness']
            illness_number = item['illness_number']
            length = len(illness)
            for i in range(length):
                ill = illness[i]
                number = illness_number[i]
                conn.execute("select e_illness_id from e_illness where e_illness_name = '%s' " % ill)
                ills = conn.fetchone()
                if not ills:
                    conn.execute("insert into e_illness(e_illness_name) values('%s') " % ill)
                    conn.execute("select e_illness_id from e_illness where e_illness_name = '%s' " % ill)
                    ills = conn.fetchone()

                conn.execute("select e_department_id from e_department where e_department_url = '%s' " %(item['url']))
                rets = conn.fetchone()
                if rets:
                    department_id = rets['e_department_id']

                    conn.execute("select * from e_illness_doctor where e_illness_id = '%s' and e_department_id = '%s'" %
                            (ills['e_illness_id'], department_id))
                    if conn.fetchone():
                        pass
                    else:
                        conn.execute("""
                            insert into e_illness_doctor(e_illness_id, e_department_id, e_hospital_id,
                            e_illness_doctor_number) values (%s, %s, %s, %s)""", (ills['e_illness_id'], department_id, ret['hospital_id'],number))


# class DepartmentPipeline(object):
#     def __init__(self):
#         self.file = codecs.open('tmp.json', 'w', encoding='utf-8')
#
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + "\n"
#         self.file.write(line)
#         return item
#
#     def spider_closed(self, spider):
#         self.file.close()

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


class ExpertPipeline(object):
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
        conn.execute("select e_expert_id from e_expert where e_expert_home_url = '%s' " % item['e_expert_home_url'])
        ret = conn.fetchone()
        if ret:
            expert_id = ret['e_expert_id']
            for order in item['e_expert_phone_orders']:
                # print order
                p_id = order['e_phone_consult_order_patient_id']
                ill = order['e_phone_consult_order_ill']
                details = order['e_phone_consult_order_details']
                conn.execute("""
                        select * from e_phone_consult_order where e_expert_id = %s and e_phone_consult_order_patient_id = '%s' and
                        e_phone_consult_order_ill = '%s' and e_phone_consult_order_details = '%s' """ %
                        (expert_id, p_id, ill, details))
                if conn.fetchone():
                    continue
                else:
                    conn.execute("""
                            insert into e_phone_consult_order(e_expert_id, e_phone_consult_order_patient_id, e_phone_consult_order_ill,
                            e_phone_consult_order_details) values(%s, '%s', '%s', '%s') """ %
                            (expert_id, p_id, ill, details))
            return item

        conn.execute("""insert into e_expert(e_expert_name, e_expert_title, e_expert_hospital,
                e_expert_department, e_expert_excel, e_expert_experience, e_expert_curative_level, e_expert_attitude_level,
                e_expert_home_url, e_expert_url, e_expert_consult_scope, e_expert_appointment, e_expert_visits, e_expert_article_number,
                e_expert_consult_number, e_expert_praise, e_expert_exp, e_expert_phone_consult_details, e_expert_phone_consult_help,
                e_expert_image_consult, e_expert_image_consult_help, e_expert_add_appointment, e_expert_add_appoinment_number,
                e_expert_phone_consult_price)
                values('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, '%s', '%s', %s, '%s', %s, '%s', %s,
                '%s') """
                % (item['e_expert_name'], item['e_expert_title'], item['e_expert_hospital'], item['e_expert_department'],
                    item['e_expert_excel'], item['e_expert_experience'], item['e_expert_curative_level'], item['e_expert_attitude_level'],
                    item['e_expert_home_url'], item['e_expert_url'], item['e_expert_consult_scope'], item['e_expert_appointment'],
                    item['e_expert_visits'], item['e_expert_article_number'], item['e_expert_consult_number'], item['e_expert_praise'],
                    item['e_expert_exp'], item['e_expert_phone_consult_details'], item['e_expert_phone_consult_help'],
                    item['e_expert_image_consult'], item['e_expert_image_consult_help'], item['e_expert_add_appointment'],
                    item['e_expert_add_appointment_number'], item['e_expert_phone_consult_price']))

        # print item['e_expert_phone_orders']
        # print len(item['e_expert_phone_orders']), item['e_expert_home_url']
        for order in item['e_expert_phone_orders']:
            # print order
            p_id = order['e_phone_consult_order_patient_id']
            ill = order['e_phone_consult_order_ill']
            details = order['e_phone_consult_order_details']
            conn.execute("""
                    insert into e_phone_consult_order(e_expert_id, e_phone_consult_order_patient_id, e_phone_consult_order_ill,
                    e_phone_consult_order_details) values(%s, '%s', '%s', '%s') """ %
                    (expert_id, p_id, ill, details))

        thanks = item['e_expert_thank']
        if len(thanks) != 0:
            conn.execute("select e_expert_id from e_expert where e_expert_home_url = '%s'" % item['e_expert_home_url'])
            ret = conn.fetchone()
            expert_id = ret['e_expert_id']
            conn.execute('alter table e_experience CONVERT TO CHARACTER SET utf8;')
            for thank in thanks:
                conn.execute("""
                        insert into e_experience(e_expert_id, e_experience_patient_id, e_experience_region, e_experience_illness, e_experience_effect,
                        e_experience_attitude, e_experience_date, e_experience_content, e_experience_like_number) values(%s, '%s', '%s', '%s', '%s','%s',
                        '%s', '%s', %s)""" % (expert_id, thank['e_experience_patient_id'], thank['e_experience_region'], thank['e_experience_illness'],
                            thank['e_experience_effect'], thank['e_experience_attitude'], thank['e_experience_date'], thank['e_experience_content'],
                            thank['e_experience_like_number']))

        return item
