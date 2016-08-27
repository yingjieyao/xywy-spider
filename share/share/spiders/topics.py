# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from share.items import *


class TopicsSpider(scrapy.Spider):
    name = "Topic"
    allowed_domains = ["club.xywy.com"]
    start_urls = (
        'http://club.xywy.com/doctorShare/',
    )

    custom_settings = {
        'ITEM_PIPELINES' : {
            'share.pipelines.SharePipeline': 300,
            'share.pipelines.SharePipeline2': 400
        }
    }

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

    headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
            "Connection": "keep-alive",
            "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
            }

    def make_requests_from_url(self, url):
        return Request(url = url, headers= self.headers)

    def parse(self, response):
        sel = Selector(response)
        lists = sel.xpath('//div[@class="tab_ConR fl"]/div/a/@href').extract()
        for li in lists:
            page_id = self.get_digit(li)
            yield Request(url = li, callback = self.get_pages, headers = self.headers)

        # print response.body
        home_url = response.url.split("?")[0]
        # print home_url
        # print response.url
        current = len(lists)
        if response.url.endswith('doctorShare/'):
            total = sel.xpath('//div[@class="DocFen mt30 f14 cb"]/a[4]/text()').extract()[0]
            total = int(total)
            for i in range(2, total):
                yield Request(url = home_url + '?page=' + str(i), callback = self.parse, headers = self.headers)

        # if current >= 10:
        #     next_digit = 2
        #     mode = re.compile(r'\d+$')
        #     digits = mode.findall(response.url)
        #     for d in digits:
        #         if response.url.endswith(d):
        #             next_digit = int(d) + 1
        #             break
        #     yield Request(url = home_url + '?page=' + str(next_digit), callback = self.parse)

    def get_pages(self, response):
        sel = Selector(response)

        item = Topic()
        item['topic_id'] = self.get_digit(response.url)
        # print item['topic_id']
        item['title'] = self.__check(sel.xpath('//div[@class="fa_Biao2"]/div/em/text()').extract())
        item['reply_number'] = self.__check(sel.xpath('//div[@class="fr share_btns"]/a[1]/span/text()').extract())
        item['like_number'] = sel.xpath('//div[@class="fr share_btns"]/a[2]/span/text()').extract()[0]
        if not item['reply_number'].isdigit():
            item['reply_number'] = 0
        item['owner_url'] = self.__check(sel.xpath('//div[@class="tab_Ralax clearfix"]/span/a/@href').extract())
        view = sel.xpath('//div[@class="tab_Ralax clearfix"]/span[3]/text()').extract()
        if view:
            item['view_number'] = view[0][3:]
        else:
            item['view_number'] = 0

        item['content'] = self.__check(sel.xpath('//h2[@class="pr fl  "]/text()').extract())
        item['follow_number'] = 0
        item['topic_type'] = ''
        if item['owner_url']:
            item['follow_number'] = sel.xpath('//h2[@class="fwei fn"]/span/text()').extract()[0]
            item['topic_type'] = sel.xpath('//div[@class="fa_Biao2"]/div/a[2]/text()').extract()[0]
            # print item['topic_type']
        item['owner_type'] = 'doctor'
        return item
        # item['topic_date'] = ## hard to get
