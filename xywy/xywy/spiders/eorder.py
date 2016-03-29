import re
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from xywy.items import *

class EorderSpider(Spider):
    name = 'Eorder'
    allowed_domains = ["z.xywy.com"]

    custom_settings = {
        'ITEM_PIPELINES' : {
            'xywy.pipelines.EorderPipeline': 300
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


    def __check(self, lists):
        if len(lists):
            return lists[0]
        return ''

    def parse(self, response):
        sel = Selector(response)
        lists = sel.xpath('//ul[@class="clearfix yvyuelist-item f12 tc"]/li/span')
        home_url = response.url.split("?")[0][:-10]
        # print 'response: ', response.url
        # print home_url
        if len(lists) != 0:
            cnt = len(lists)
            items = []
            for i in range(0, cnt, 5):
                item = EorderItem()
                item['order_id'] = self.__check(lists[i].xpath('text()').extract())
                item['location'] = self.__check(lists[i + 1].xpath('text()').extract())
                item['illness'] = self.__check(lists[i + 2].xpath('text()').extract())
                item['time'] = self.__check(lists[i + 3].xpath('text()').extract())
                item['order_type'] = self.__check(lists[i + 4].xpath('text()').extract())
                item['expert_url'] = home_url
                # print item['location']
                items.append(item)
                yield item

            if cnt == 50:
                next_digit = 2
                mode = re.compile(r'\d+$')
                digits = mode.findall(response.url)
                for d in digits:
                    if response.url.endswith(d):
                        next_digit = int(d) + 1
                        break
                username = home_url[22:]
                # print 'next :', home_url+ '/yuyue.php?doctoruser=' + username + '&type=list&page=' + str(next_digit)
                yield Request(url=home_url + '/yuyue.php?doctoruser=' +  username + '&type=list&page=' + str(next_digit), callback=self.parse)

