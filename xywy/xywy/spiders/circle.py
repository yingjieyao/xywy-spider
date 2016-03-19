import re
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from xywy.items import CircleItem

class CircleSpider(Spider):
    name = 'Circle'
    allowed_domains = ["home.xywy.com"]
    # rules = [Rule(LinkExtractor(allow=['/([a-z]+)/$']), callback='parse_item', follow=False)]

    custom_settings = {
        'ITEM_PIPELINES' : {
            'xywy.pipelines.CirclePipeline': 300
        }
    }

    start_urls = ["http://home.xywy.com/"]

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//a[@class="mr5"]')

        for url in urls:
            circle = CircleItem()
            circle['url'] = url.xpath('@href').extract()
            yield Request(circle['url'][0], callback=self.parse_item)

    def parse_item(self, response):
        sel = Selector(response)
        item = CircleItem()

        item['circle_name'] = sel.xpath('//div[@class="clearfix"]/div[@class="f16 fl fYaHei fb gray-a normal-a"]/a/@title').extract()[0]

        item['circle_circle_intro'] = sel.xpath('//dd[@class="pt10 lh180 gray group-info oh"]/text()').extract()[0]

        content = sel.xpath('//dd[@class="pt5 f14 graydeep"]')
        item['circle_suffer_number'] = content.xpath('//b[@class="fn green"]/text()').extract()[0]
        item['circle_expert_number'] = content.xpath('//b[@class="fn green"]/text()').extract()[1]
        item['circle_topic_number'] = content.xpath('//b[@class="fn green"]/text()').extract()[2]

        user_url = content.xpath('span[4]/a/@href').extract()
        if len(user_url) > 0:
            user_id = re.findall(r'(\w*\d+)\w*', user_url[0])
            item['circle_owner_id'] = user_id[0]
        else:
            item['circle_owner_id'] = 0

        return item
