# -*- coding: utf-8 -*-

import re
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from xywy.items import *

class HospitalSpider(Spider):
    name = 'Hospital'
    allowed_domains = ["z.xywy.com"]
    # rules = [Rule(LinkExtractor(allow=['/([a-z]+)/$']), callback='parse_item', follow=False)]

    custom_settings = {
        'ITEM_PIPELINES' : {
            'xywy.pipelines.HospitalPipeline': 300
        }
    }

    start_urls = ["http://z.xywy.com/yiyuan.htm"]

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//ul[@class="jib-classification clearfix"]/li/a/@href').extract()

        for url in urls:
            yield Request(url, callback=self.get_hos_pages)

    def get_hos_pages(self, response):
        sel = Selector(response)
        urls = sel.xpath('//ul[@class="clearfix"]/li')
        for url in urls:
            yield Request(url.xpath('a/@href').extract()[0], callback=self.get_info)

    def get_info(self, response):
        item = HospitalItem()
        sel = Selector(response)
        item['hospital_name'] = sel.xpath('//div[@class="z-head-name"]/strong/text()').extract()[0]

        t_add = sel.xpath('//div[@class="z-hospital-address fr"]/div/div[@class="clearfix lh30"][1]//p/text()').extract()
        if len(t_add) == 2:
            item['hospital_address'] = t_add[1].encode('utf-8')
        elif len(t_add) == 1:
            item['hospital_address'] = t_add[0].encode('utf-8')
        else:
            item['hospital_address'] = "NULL"

        t_phone = sel.xpath('//div[@class="z-hospital-address fr"]/div/div[@class="clearfix lh30"][3]//p/text()').extract()
        if len(t_phone) == 2:
            item['hospital_phone'] = t_phone[1].encode('utf-8')
        elif len(t_phone) == 1:
            item['hospital_phone'] = t_phone[0].encode('utf-8')
        else:
            item['hospital_phone'] = "NULL"

        t_image_online_number = sel.xpath('//div[@class="clearfix"]/div[1]/div[1]/span/a/text()').extract()
        if t_image_online_number:
            item['hospital_image_online_number'] = t_image_online_number[0]
        else:
            item['hospital_image_online_number'] = 0

        t_register_number = sel.xpath('//div[@class="clearfix"]/div[1]/div[2]/span/a/text()').extract()
        if t_register_number:
            item['hospital_register_number'] = t_register_number[0]
        else:
            item['hospital_register_number'] = 0

        t_appointment = sel.xpath('//div[@class="clearfix"]/div[1]/div[2]/span/em/text()').extract()
        if t_appointment:
            item['hospital_appointment'] = t_appointment[0]
        else:
            item['hospital_appointment'] = 0

        t_department_number = sel.xpath('//div[@class="clearfix"]/div[@class="gray fr mt20"]/a[1]/text()').extract()
        item['hospital_department_number'] = t_department_number[0]

        t_expert_number = sel.xpath('//div[@class="clearfix"]/div[@class="gray fr mt20"]/a[2]/text()').extract()
        if t_expert_number:
            item['hospital_expert_number'] = t_expert_number[0]
        else:
            item['hospital_expert_number'] = 0

        t_to = sel.xpath('//div[@class="help pa graydeep tc"]')
        t_score = t_to.xpath('//span[1]/text()').extract()
        if t_score:
            item['hospital_score'] = t_score[0][0:-1]
        else:
            item['hospital_score'] = -1

        t_experience = t_to.xpath('//span[2]/text()').extract()
        if t_experience:
            item['hospital_number_experience'] = t_experience[0]
        else:
            item['hospital_number_experience'] = 0

        t_intro = sel.xpath('//div[@class="z-hospital-infor bdr-top graydeep"]/p/a/@href').extract()
        if len(t_intro) == 0:
            item['hospital_intro'] = sel.xpath('//div[@class="z-hospital-infor bdr-top graydeep"]/p/text()').extract()[0].encode('utf-8')
            yield item
        else:
            yield Request(url=t_intro[0], meta={'item': item}, callback=self.get_intro)

    def get_intro(self, response):
        item = response.meta['item']
        sel = Selector(response)
        item['hospital_intro'] = sel.xpath('//div[@class="bdr-all mt20 clearfix"]/div').extract()[0]
        return item
