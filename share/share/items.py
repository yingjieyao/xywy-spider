# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


# class ShareItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
#

class Topic(Item):
    topic_id = Field()
    title = Field()
    content = Field()
    reply_number = Field()
    like_number = Field()
    owner_url = Field()
    view_number = Field()
    follow_number = Field()
    topic_type = Field()
    owner_type= Field()
    topic_date = Field()

class Reply(Item):
    reply_id = Field()
    topic_id = Field()
    doctor_id = Field()
    doctor_url = Field()
    reply_content = Field()
    reply_like_number = Field()
    reply_date = Field()
    reply_follow_content = Field()
    follow_doctor_id = Field()
    follow_date = Field()
    doctor = Field()

class DoctorItem(Item):
    doctor_id = Field()
    url = Field()
    name = Field()
    title = Field()
    department = Field()
    experience_level = Field()
    best_reply = Field()
    help_patients = Field()
    reputation = Field()
    thanks = Field()
    fan_number = Field()
    excel = Field()
    hospital = Field()
    intro = Field()


