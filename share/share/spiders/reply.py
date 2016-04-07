# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from share.items import *


class ReplySpider(scrapy.Spider):
    name = "Reply"

    custom_settings = {
        'ITEM_PIPELINES' : {
            'share.pipelines.ReplyPipeline': 300,
        }
    }

    def __init__(self):
        files = open('topic_id.json', 'r')
        lines = files.readlines()
        self.start_urls = []
        # for line in lines:
        line = 44616
        self.start_urls.append('http://club.xywy.com/doctorShare/index.php?type=share_operation&page=2&stat=15&share_id=' + str(line))

        files.close()

    def __check(self, st):
        if st:
            return st[0]
        return ''

    def get_digit(self, st):
        mode = re.compile(r'\d+$')
        digits = mode.findall(st)
        for d in digits:
            if st.endswith(d):
                return d
        return -1

    def parse(self, response):
        print response.url
        sel = Selector(response)
        reply_list = sel.xpath('//div[@class="dis_List clearfix pr"]')
        for reply in reply_list:
            item = Reply()
            # print reply.extract()
            item['topic_id'] = self.get_digit(response.url)
            item['reply_id'] = reply.xpath('.//input[@id="review_id"]/@value').extract()[0]
            item['doctor_id'] = json.loads(reply.xpath('./div[@class="dis_ListLe dis_ListLe_first fl mt20"]/@data-list').extract()[0])['userId']
            item['reply_content'] = reply.xpath('.//p[@class="mt10"]//text()').extract()[0]
            item['reply_like_number'] = reply.xpath('.//b[@class="fn f12"]/text()').extract()[0]
            item['doctor_url'] = 'http://club.xywy.com/doc_card/' + item['doctor_id'] + '/blog'
            item['reply_date'] = reply.xpath('.//span[@class="pl5 f12"]/text()').extract()[0]
            item['reply_follow_content'] = ''
            item['follow_doctor_id'] = ''
            item['follow_date'] = ''
            yield Request(url=item['doctor_url'], meta={'item': item}, callback=self.get_doctor)

    def join_list(self, lists):
        ret = ''
        for lis in lists:
            ret = ret + lis
        return ret

    def get_doctor(self, response):
        item = response.meta['item']
        doctor = DoctorItem()
        sel = Selector(response)
        if not response.url.endswith(item['doctor_id']):
            doctor['name'] = sel.xpath('//ul[@class="fl bdul f14"]/li[1]/span[2]/text()').extract()[0]
            doctor['title'] = sel.xpath('//ul[@class="fl bdul f14"]/li[2]/span[2]/text()').extract()[0]
            doctor['department'] = sel.xpath('//ul[@class="fl bdul f14"]/li[3]/span[2]/text()').extract()[0]
            doctor['experience_level'] = sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[1]/span/text()').extract()[0][:-1]
            doctor['best_reply'] = sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[2]/span/text()').extract()[0][:-1]
            doctor['help_patients'] = sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[3]/span/text()').extract()[0][:-1]
            doctor['reputation'] = len(sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[4]/cite').extract())
            doctor['thanks'] = sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[5]/span/text()').extract()[0][:-1]
            doctor['fan_number'] = sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[6]/span/text()').extract()[0][:-1]
            doctor['excel'] = self.join_list(sel.xpath('//div[@class="dbjb f12 mt10"]/a/text()').extract())
            doctor['hospital'] = sel.xpath('//div[@class="dbjb f12 mt10"]/text()').extract()[-1]
            doctor['intro'] = sel.xpath('//div[@class="f12 dbjj mt10 mr20 pr"]/p/text()').extract()[0]
            tmp = sel.xpath('//div[@id="jeje"]')
            if tmp:
                doctor['excel'] = tmp.xpath('./p[1]/text()').extract()[0][6:]
                doctor['hospital'] = tmp.xpath('./p[2]/text()').extract()[0][5:]
                doctor['intro'] = tmp.xpath('./div/text()').extract()[0][5:]
            # print doctor['intro']
            item['doctor'] = doctor
            return item
        # family doctor
        else:
            print response.url
            pass

