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

    custom_settings = {
        'ITEM_PIPELINES' : {
            'xywy.pipelines.ArticlePipeline': 300
        }
    }


    def __init__(self):
        article_url = open('d_article_url.json', 'r')
        urls = article_url.readlines()
        self.start_urls = []
        for url in urls:
            if len(url) > 15:
                print url[:-1]
                self.start_urls.append(url[:-1] + '/wenzhang.htm')

        article_url.close()


    def parse(self, response):
        # item['home_url'] = response.url[:-13]
        sel = Selector(response)
        num_article = sel.xpath('//span[@class="yisheng6"]/text()').extract()
        home_url = response.url.split("?")[0]
        if len(num_article) != 0:
            urls = sel.xpath('//span[@class="artit_view lightblue-a"]/a[1]/@href').extract()
            numbers = len(urls)
            for url in urls:
                yield Request(url=url, meta={'from_url': home_url[:-13]}, callback=self.get_article)

            if numbers == 20:
                next_digit = 2
                mode = re.compile(r'\d+$')
                digits = mode.findall(response.url)
                for d in digits:
                    if response.url.endswith(d):
                        next_digit = int(d) + 1
                        break
                username = home_url[22:-13]
                yield Request(url=home_url + '?doctoruser=' +  username + '&page=' + str(next_digit), callback=self.parse)

        # print response.url[22:-13]

    def get_article(self, response):
        # print response.url
        item = ArticleItem()
        item['home_url'] = response.meta['from_url']
        # item = response.meta['item']
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
        item['read'] = read[3:-3]

        like = sel.xpath('//span[@class="num db fl"]/text()').extract()[0]
        dislike = sel.xpath('//span[@class="num db fl mr10"]/text()').extract()[0]
        item['like'] = like[1:-1]
        item['dislike'] = dislike[1:-1]
        return item

