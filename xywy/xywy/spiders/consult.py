import re
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from xywy.items import *

class ConsultSpider(Spider):
    name = 'Consult'
    allowed_domains = ["xywy.com"]

    custom_settings = {
        'ITEM_PIPELINES' : {
            'xywy.pipelines.ConsultPipeline': 300
        }
    }


    def __init__(self):
        article_url = open('d_article_url.json', 'r')
        urls = article_url.readlines()
        self.start_urls = []
        for url in urls:
            if len(url) > 15:
                self.start_urls.append(url[:-1] + '/zixun.php')

        article_url.close()


    def __check(self, lists):
        if len(lists):
            return lists[0]
        return ''

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//ul[@class="view_list f12 pl15 pr15 clearfix"]//a/@href').extract()
        home_url = response.url.split("?")[0][:-10]
        # print home_url
        for url in urls:
            # print 'get ',url
            yield Request(url=url, meta={'home_url': home_url}, callback=self.get_consult)

        cnt = len(urls)
        if cnt == 20:
            next_digit = 2
            mode = re.compile(r'\d+$')
            digits = mode.findall(response.url)
            for d in digits:
                if response.url.endswith(d):
                    next_digit = int(d) + 1
                    break

            yield Request(url=home_url + '/zixun.php?page=' + str(next_digit), callback=self.parse)

    def get_consult(self, response):
        mode = re.compile(r'\d+$')
        digits = mode.findall(response.url[:-4])
        item = EconsultItem()
        if not ditis:
            return
        item['consult_id'] = digits[0]
        item['expert_url'] = response.meta['home_url']

        sel = Selector(response)
        patient_id = sel.xpath('//div[@class="expert_info fl f12"]/p[1]/text()').extract()[0]
        item['patient_id'] = patient_id
        item['illness'] = self.__check(sel.xpath('//div[@class="reply_info fl f14 pl15 pr15 pt10 pb10"]/p[2]/text()').extract())
        item['illness_detail'] = self.__check(sel.xpath('//div[@class="reply_info fl f14 pl15 pr15 pt10 pb10"]/p[4]/text()').extract())
        item['previous'] = self.__check(sel.xpath('//div[@class="reply_info fl f14 pl15 pr15 pt10 pb10"]/p[6]/text()').extract())
        item['want_help'] = self.__check(sel.xpath('//div[@class="reply_info fl f14 pl15 pr15 pt10 pb10"]/p[8]/text()').extract())
        item['date'] = self.__check(sel.xpath('//div[@class="reply_info fl f14 pl15 pr15 pt10 pb10"]/p[9]/text()').extract())
        item['date'] = item['date'][4:]

        item['analysis'] = self.__check(sel.xpath('//p[@class="pt10 lightblue-a"]/text()').extract())
        item['suggest'] = ""
        # print reply
        item['reply_date'] = sel.xpath('//div[@class="f12 gray mt10 pt2"]/div[@class="clearfix pt15"]/span/text()').extract()[0][-19:]

        like_dislike = sel.xpath('//div[@class="f12 gray mt10 pt2"]/div[@class="clearfix pt15"]/div/span[@class="num db fl lightblue"]/text()').extract()
        item['like_number'] = like_dislike[0][1:-1]
        item['dislike_number'] = like_dislike[1][1:-1]

        item['replys'] = []

        t_replys = sel.xpath('//div[@class="clearfix mb10"]').extract()

        return item
        # if len(t_replys) <= 2:
        #     return item

        # for reply in t_replys[2:]:
        #     ask = reply.xpath('//div[@class="reply_info fl f14 pl15 pr15 pt10 pb10 reply-mark"]')
        #     ask_content = self.__check(ask.xpath('/p[1]/text()').extract())
        #     ask_date = self.__check(ask.xpath('/p[2]/text()').extract())
        #     print ask_date, ask_content, len(replys)
        #     answer = reply.xpath('//div[@class="reply_info fl f14 pl15 pr15 pt10 pb10"]')

