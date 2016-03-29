import re
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from xywy.items import *

class VoteSpider(Spider):
    name = 'Vote'
    allowed_domains = ["z.xywy.com"]

    custom_settings = {
        'ITEM_PIPELINES' : {
            'xywy.pipelines.VotePipeline': 300
        }
    }


    def __init__(self):
        vote_url = open('d_vote_url.json', 'r')
        urls = vote_url.readlines()
        self.start_urls = []
        for url in urls:
            if len(url) > 15:
                print url[:-1]
                self.start_urls.append(url[:-1])

        vote_url.close()


    def parse(self, response):
        # item['home_url'] = response.url[:-13]
        sel = Selector(response)
        items = []
        votes = sel.xpath('//ul[@class="doc-attending-list mt10 clarfix public-list"]/li')
        for vote in votes:
            item = VoteItem()
            item['e_vote_illness_name'] = vote.xpath('a/@title').extract()[0]
            item['e_vote_number'] = vote.xpath('span/text()').extract()[0][1:-1]
            item['e_expert_url'] = response.url
            items.append(item)

        return items
