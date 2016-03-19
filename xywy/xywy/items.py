# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XywyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CircleItem(scrapy.Item):
    url = scrapy.Field()
    circle_name = scrapy.Field()
    circle_circle_intro = scrapy.Field()
    circle_suffer_number = scrapy.Field()
    circle_expert_number = scrapy.Field()
    circle_topic_number = scrapy.Field()
    circle_owner_id = scrapy.Field()

class HospitalItem(scrapy.Item):
    hospital_name = scrapy.Field()

