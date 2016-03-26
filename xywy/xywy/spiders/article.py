import re
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from xywy.items import *

class ArticleSpider(Spider):
    name = 'Article'
    allowed_domains = ["z.xywy.com"]

    # custom_settings = {
    #     'ITEM_PIPELINES' : {
    #         'xywy.pipelines.CirclePipeline': 300
    #     }
    # }


    def __init__(self):
        article_url = open('d_article_url.json', 'r')
        urls = article_url.readlines()
        self.start_urls = []
        for url in urls:
            if len(url) > 15:
                self.start_urls.append(url[:-2] + '/wenzhang.htm')

        article_url.close()


    def parse(self, response):
        item = ArticleItem()
        item['home_url'] = response.url
        sel = Selector(response)
        num_article = sel.xpath('//span[@class="yisheng6"]/text()').extract()
        # print num_article, len(num_article)
        if len(num_article) != 0:
            numbers = num_article[0]
            urls = sel.xpath('//span[@class="artit_view lightblue-a"]/a[1]/@href').extract()
            for url in urls:
                yield Request(url=url, meta={'item': item}, callback=self.get_article)

    def get_article(self, response):
        print response.url
        item = response.meta['item']
        sel = Selector(response)

        tags = sel.xpath('//p[@style="float:left;padding-right:15px;"]/span/a/text()').extract()
        f_tag = []
        for tag in tags:
            f_tag.append(tag)
        item['tag'] = f_tag

        item['article_url'] = response.url
        item['title'] = sel.xpath('//h3[@class="f20 fYaHei pt10 pb10"]/text()').extract()[0]

        author_time = sel.xpath('//div[@class="pr clearfix tl pb5 pt5"]/p/text()').extract()[1].split("|")
        author =  author_time[1][4:-1]
        time = author_time[2][6:-7]
        item['date'] = time
        item['author'] = author

        content = sel.xpath('//div[@class="new_artcont pt10 f14 lh180 clearfix"]//p/text()').extract()
        con = ''
        for cont in content:
            con = con + cont
        item['content'] = con
        read = sel.xpath('//span[@class="db fl"]/text()').extract()[0]
        item['read'] = read

        like = sel.xpath('//span[@class="num db fl"]').extract()[0]
        dislike = sel.xpath('//span[@class="num db fl mr10"]').extract()[0]
        item['like'] = like
        item['dislike'] = dislike
        return item

