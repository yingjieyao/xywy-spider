import re
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from xywy.items import *

class AppointSpider(Spider):
    name = 'Eappointment'
    allowed_domains = ["z.xywy.com"]

    custom_settings = {
        'ITEM_PIPELINES' : {
            'xywy.pipelines.EappointmentPipeline': 300
        }
    }


    def __init__(self):
        article_url = open('d_article_url.json', 'r')
        urls = article_url.readlines()
        self.start_urls = []
        for url in urls:
            if len(url) > 15:
                self.start_urls.append(url[:-1] + '/yuyue.php?type=list')

        article_url.close()
        print len(self.start_urls)


    def __check(self, lists):
        if len(lists):
            return lists[0]
        return ''

    def parse(self, response):
        print response.url
        sel = Selector(response)
        res = sel.xpath('//span[@class="fl w560 lh180 pub_txtalign"]')
        item = EappointItem()
        item['e_range'] = ''
        item['require'] = ''
        item['region'] = ''
        item['expert_url'] = response.url[:-20]

        if not res:
            return item
        item['e_range'] = self.__check(res[0].xpath('text()').extract())
        item['region'] = self.__check(res[1].xpath('text()').extract())
        item['require'] = self.__check(res[2].xpath('text()').extract())
        # print 'response: ', response.url
        return item
        # print home_url
