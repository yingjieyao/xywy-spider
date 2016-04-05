# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item

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

class DepartmentItem(Item):
    hospital_name = Field()
    url = Field()
    e_department_name = Field()
    e_department_key = Field()
    e_department_doc_number = Field()
    e_department_image = Field()
    e_department_register_number = Field()
    e_department_appointment_number = Field()
    e_department_phone_consult_number = Field()
    e_department_phone_consult_success_number = Field()
    illness = Field() ##list
    illness_number = Field()

class ExpertItem(Item):
    e_expert_name = Field()
    e_expert_title = Field()
    e_expert_hospital = Field()
    e_expert_department = Field()
    e_expert_excel = Field()
    e_expert_experience = Field()
    e_expert_curative_level = Field()
    e_expert_attitude_level = Field()
    e_expert_home_url = Field()
    e_expert_url = Field()
    e_expert_consult_scope = Field()
    e_expert_appointment = Field()
    e_expert_visits = Field()
    e_expert_article_number= Field()
    e_expert_consult_number = Field()
    e_expert_praise = Field()
    e_expert_exp = Field()
    e_expert_last_online_time = Field() ##
    e_expert_join_time = Field() ##
    e_expert_reply_number = Field()
    e_expert_appointment_success_number = Field()
    e_expert_vote_number = Field()
    e_expert_phone_consult_details = Field()
    e_expert_phone_consult_help = Field()
    e_expert_image_consult = Field()
    e_expert_image_consult_help = Field()
    e_expert_add_appointment = Field()
    e_expert_add_appointment_number = Field()
    e_expert_time = Field()
    e_expert_phone_orders = Field() # list
    e_expert_phone_consult_price = Field()
    e_expert_thank = Field() # list

class PhoneConsultItem(Item):
    e_phone_consult_order_patient_id = Field()
    e_phone_consult_order_details = Field()
    e_phone_consult_order_ill = Field()

class ExperienceItem(Item):
    e_experience_patient_id = Field()
    e_experience_region = Field()
    e_experience_illness = Field()
    e_experience_attitude = Field()
    e_experience_date = Field()
    e_experience_content = Field()
    e_experience_effect = Field()
    e_experience_like_number = Field()

class ArticleItem(Item):
    home_url = Field()
    article_url = Field()
    e_expert_id = Field()
    author = Field()
    title = Field()
    date = Field()
    content = Field()
    read = Field()
    like = Field()
    dislike = Field()
    tag = Field() # list

class VoteItem(Item):
    e_expert_url = Field()
    e_vote_illness_name = Field()
    e_vote_number = Field()

class EorderItem(Item):
    order_id = Field()
    expert_url = Field()
    location = Field()
    illness = Field()
    time = Field()
    order_type = Field()

class EappointItem(Item):
    expert_url = Field()
    e_range = Field()
    region = Field()
    require = Field()

class EconsultItem(Item):
    consult_id = Field()
    expert_url = Field()
    patient_id = Field()
    illness = Field()
    illness_detail = Field()
    previous = Field()
    want_help = Field()
    date = Field()
    analysis = Field()
    suggest = Field()
    reply_date = Field()
    like_number = Field()
    dislike_number = Field()
    replys = Field() # list

class EreplyItem(Item):
    reply_id = Field()
    consult_id = Field()
    reply_content = Field()
    reply_date = Field()
    owner_id = Field()


