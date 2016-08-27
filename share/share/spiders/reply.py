# -*- coding: utf-8 -*-
import re
import sys
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

    headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
            }
    def __init__(self):
        files = open('topic_id.json', 'r')
        lines = files.readlines()
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.start_urls = []
        for line in lines:
            # line = '45183%0A'
            self.start_urls.append('http://club.xywy.com/doctorShare/index.php?type=share_operation&page=2&stat=15&share_id=' + str(line))

        files.close()

    def make_requests_from_url(self, url):
        return Request(url = url, headers = self.headers)

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
        sel = Selector(response)
        reply_list = sel.xpath('//div[@class="dis_List clearfix pr"]')
        for reply in reply_list:
            item = Reply()
            # print reply.extract()
            item['topic_id'] = self.get_digit(response.url[:-3])
            item['reply_id'] = reply.xpath('.//input[@id="review_id"]/@value').extract()[0]
            doctor_id = reply.xpath('./div[@class="dis_ListLe dis_ListLe_first fl mt20"]/@data-list').extract()
            if doctor_id:
                item['doctor_id'] = json.loads(reply.xpath('./div[@class="dis_ListLe dis_ListLe_first fl mt20"]/@data-list').extract()[0])['userId']
            else:
                continue
            item['reply_content'] = self.__check(reply.xpath('.//p[@class="mt10"]//text()').extract())
            item['reply_like_number'] = reply.xpath('.//b[@class="fn f12"]/text()').extract()[0]
            item['doctor_url'] = 'http://club.xywy.com/doc_card/' + item['doctor_id'] + '/blog'
            item['reply_date'] = reply.xpath('.//span[@class="pl5 f12"]/text()').extract()[0]
            item['reply_follow_content'] = ''
            item['follow_doctor_id'] = ''
            item['follow_date'] = ''
            yield Request(url=item['doctor_url'], meta={'item': item}, callback=self.get_doctor, headers=self.headers)

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
            doctor['experience_level'] = self.__check(sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[1]/span/text()').extract())
            tmp = self.__check(sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[2]/span/text()').extract())
            if len(tmp):
                doctor['best_reply'] = tmp[:-1]
            else:
                doctor['best_reply'] = ''

            doctor['help_patients'] = sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[3]/span/text()').extract()[0][:-1]
            doctor['reputation'] = len(sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[4]/cite').extract())
            doctor['thanks'] = sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[5]/span/text()').extract()[0][:-1]
            doctor['fan_number'] = sel.xpath('//ul[@class="bdxli pt10 f12 clearfix black"]/li[6]/span/text()').extract()[0][:-1]
            doctor['excel'] = self.join_list(sel.xpath('//div[@class="dbjb f12 mt10"]/a/text()').extract())
            doctor['hospital'] = sel.xpath('//div[@class="dbjb f12 mt10"]/text()').extract()[-1]
            doctor['intro'] = sel.xpath('//div[@class="f12 dbjj mt10 mr20 pr"]/p/text()').extract()[0]
            doctor['url'] = response.url
            tmp = sel.xpath('//div[@id="jeje"]')
            if tmp:
                doctor['excel'] = tmp.xpath('./p[1]/text()').extract()[0][6:]
                doctor['hospital'] = tmp.xpath('./p[2]/text()').extract()[0][5:]
                doctor['intro'] = tmp.xpath('./div/text()').extract()[0][5:]

                item['doctor'] = doctor
                yield item
        # family doctor
            else:
                family_doc_url = response.url.replace("share","home")
                yield Request(url=family_doc_url, meta={'item': item}, callback=self.get_family_doctor, headers = self.headers)

    def get_family_doctor(self, response):
        sel = Selector(response)
        item = response.meta['item']
        doctor = DoctorItem()
        doctor['url'] = response.url
        doctor['experience_level'] = ''
        doctor['best_reply'] = 0
        doctor['name'] = sel.xpath('//div[@class="pa doc-attent-pop none"]/div/span[2]/em/text()').extract()[0]
        doctor['title'] = sel.xpath('//div[@class=" lh200 pt10 f14"]//text()').extract()[0]

        hospital_depart = sel.xpath('//div[@class=" lh200 pt10 f14"]//text()').extract()[1]
        hos = hospital_depart.split("-")[0]
        depart = hospital_depart.split("-")[1]
        doctor['department'] = depart
        doctor['hospital'] = hos
        doctor['excel'] = self.__check(sel.xpath('//div[@class="HomeLe fl"]/div/div[@class="HomeJie f14 fwei pt20"][1]/div/text()').extract()[0])
        doctor['intro'] = self.__check(sel.xpath('//div[@class="HomeLe fl"]/div/div[@class="HomeJie f14 fwei pt20"][2]/div/text()').extract()[0])
        doctor['help_patients'] = sel.xpath('//div[@class="f14 fwei HomeHelp tc lh200 clearfix pt10"]/span[1]/text()').extract()[0]
        doctor['fan_number'] = 0
        doctor['thanks'] = 0
        doctor['reputation'] = 0
        item['doctor'] = doctor
        return item
