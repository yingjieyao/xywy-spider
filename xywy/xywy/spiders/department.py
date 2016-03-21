# -*- coding: utf-8 -*-

import re
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from xywy.items import *

class DepartmentSpider(Spider):
    name = 'Department'
    allowed_domains = ["z.xywy.com"]
    # rules = [Rule(LinkExtractor(allow=['/([a-z]+)/$']), callback='parse_item', follow=False)]

    custom_settings = {
        'ITEM_PIPELINES' : {
            'xywy.pipelines.DepartmentPipeline': 300
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
        item = DepartmentItem()
        sel = Selector(response)
        item['hospital_name'] = sel.xpath('//div[@class="z-head-name"]/strong/text()').extract()[0]
        all_url = sel.xpath('//div[@class="z-h-ks-list bdr-top mt10"]/div[2]')

        items = []
        bool_v = []
        next_urls = []
        ## zhongdiankeshi
        urls = all_url.xpath('//div[@class="z-h-k-name-import pb10 pt10 clearfix pr minus1"]//li')
        for url1 in urls:
            item['e_department_key'] = 1
            doc_number = url1.xpath('span/a/text()').extract()
            if doc_number:
                item['e_department_doc_number'] = doc_number[0][0:-1]
            else:
                item['e_department_doc_number'] = 0
            items.append(item)
            next_urls.append(url1.xpath('a/@href').extract()[0])
            # yield Request(url=url1.xpath('a/@href').extract()[0], callback=self.get_department, meta={'item': item})


        urls = all_url.xpath('//div[@class="z-h-k-name pb10 pt10 bdr-dashed clearfix"]//li')
        for url1 in urls:
            item['e_department_key'] = 0
            doc_number = url1.xpath('span/a/text()').extract()
            if doc_number:
                item['e_department_doc_number'] = doc_number[0][0:-1]
            else:
                item['e_department_doc_number'] = 0
            items.append(item)
            next_urls.append(url1.xpath('a/@href').extract()[0])

        index = len(items)
        for it in range(index):
            yield Request(url=next_urls[it], callback=self.get_department, meta={'item': items[it]})

    def get_department(self, response):
        item = response.meta['item']
        item['url'] = response.url
        sel = Selector(response)
        item['e_department_image'] = 0
        item['e_department_register_number'] = 0
        item['e_department_appointment_number'] = 0
        item['e_department_phone_consult_number'] = 0
        item['e_department_phone_consult_success_number'] = 0
        alls = sel.xpath('//div[@class="w400 fl"]')
        for it in alls:
            test = it.xpath('span/text()').extract()[0]
            if len(test) == 5:
                item['e_department_image'] = it.xpath('span/strong/text()').extract()[0]
            elif len(test) == 12:
                item['e_department_register_number'] = it.xpath('span/strong/text()').extract()[0]
                item['e_department_appointment_number'] = it.xpath('span/span/text()').extract()[0]
            elif len(test) == 14:
                item['e_department_phone_consult_number'] = it.xpath('span/strong/text()').extract()[0]
                cnt = it.xpath('span/span/text()').extract()
                if cnt:
                    item['e_department_phone_consult_success_number'] = cnt[0]
        expert_url = sel.xpath('//ul[@class="z-functional-items z-hospital-items clearfix f14"]/li[3]/a/@href').extract()[0]
        yield Request(url=expert_url, callback=self.get_illness_number, meta={'item': item})
        print expert_url


    def get_illness_number(self, response):
        sel = Selector(response)
        item = response.meta['item']
        ills = sel.xpath('//div[@class="t-experts-ks fl"]')
        illnesses = []
        illnesses_number = []
        for ill in ills:
            illness = ill.xpath('a/span[1]/text()').extract()[0]
            illness_number = ill.xpath('a/span[2]/text()').extract()[0]
            illnesses.append(illness)
            illnesses_number.append(illness_number)
        item['illness'] = illnesses
        item['illness_number'] = illnesses_number
        return item

