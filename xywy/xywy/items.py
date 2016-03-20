# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

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
    hospital_intro = scrapy.Field()
    hospital_address = scrapy.Field()
    hospital_phone = scrapy.Field()
    hospital_image_online_number = scrapy.Field()
    hospital_register_number = scrapy.Field()
    hospital_appointment = scrapy.Field()
    hospital_department_number = scrapy.Field()
    hospital_expert_number = scrapy.Field()
    hospital_score = scrapy.Field()
    hospital_number_experience = scrapy.Field()


