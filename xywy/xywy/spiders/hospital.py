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

    # custom_settings = {
    #     'ITEM_PIPELINES' : {
    #         'xywy.pipelines.CirclePipeline': 300
    #     }
    # }

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
        print response.url

