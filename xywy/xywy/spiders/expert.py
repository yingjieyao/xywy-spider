import re
from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from xywy.items import *

class ExpertSpider(Spider):
    name = 'Expert'
    allowed_domains = ["z.xywy.com"]

    custom_settings = {
        'ITEM_PIPELINES' : {
            # 'xywy.pipelines.ExpertPipeline': 300
            'xywy.pipelines.ExpertPipeline2': 400
        }
    }

    start_urls = ["http://z.xywy.com/b.htm"]

    def parse(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="w780 fl bdr1-top"]//a[@class="c2c"]/@href').extract()

        for url in urls:
            yield Request(url, callback=self.deep2)

    def deep2(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="fr more mt20"]//@href').extract()
        for url in urls:
            yield Request(url, callback=self.deep3)

    def deep3(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="bdr-top pb20"]//li/a/@href').extract()
        for url in urls:
            yield Request(url, callback=self.deep4)

    def deep4(self, response):
        sel = Selector(response)
        urls = sel.xpath('//div[@class="z-hospital-functional fl"]/ul/li[2]/a/@href').extract()
        for url in urls:
            yield Request(url, meta={'home': url}, callback=self.deep5)

    def deep5(self, response):
        sel = Selector(response)
        url = response.url
        home_url = response.meta['home']
        mode = re.compile(r'\d+')
        digits = mode.findall(url)
        next_digit = 2

        for digit in digits:
            if url.endswith(digit):
                next_digit = int(digit) + 1
                # print next_digit
                break

        urls = sel.xpath('//a[@class="f14 fb"]/@href').extract()
        if len(urls) == 20:
            for url in urls:
                yield Request(url, callback=self.deep6)
            yield Request(home_url + '?&page=' + str(next_digit), meta={'home': home_url}, callback=self.deep5)


    def deep6(self, response):
        sel = Selector(response)
        item = ExpertItem()
        info = sel.xpath('//div[@class="clearfix"]')

        item['e_expert_thank'] = []
        item['e_expert_phone_orders'] = []
        item['e_expert_consult_scope'] = ''
        item['e_expert_appointment'] = 0
        item['e_expert_visits'] = 0
        item['e_expert_article_number'] = 0
        item['e_expert_consult_number'] = 0
        item['e_expert_praise'] = 0
        item['e_expert_exp'] = ''
        item['e_expert_reply_number'] = 0
        item['e_expert_phone_consult_details'] = ''
        item['e_expert_phone_consult_help'] = 0
        item['e_expert_phone_consult_price'] = ''
        item['e_expert_image_consult'] = ''
        item['e_expert_image_consult_help'] = 0
        item['e_expert_add_appointment'] = ''
        item['e_expert_add_appointment_number'] = 0
        item['e_expert_name'] = sel.xpath('//div[@class="z-head-name"]/strong//text()').extract()[0]

        titles = sel.xpath('//div[@class="z-head-name"]/span/text()').extract()
        title = ''
        for t in titles:
            title = title + t + ' '
        item['e_expert_title'] = title

        hospital = info.xpath('//span[@class="fl"]/a/text()').extract()
        item['e_expert_hospital'] = item['e_expert_department'] = ""
        if hospital:
            item['e_expert_hospital'] = hospital[0]
        depart = info.xpath('//span[@class="fl ml15"]/a/text()').extract()
        if depart:
            item['e_expert_department'] = depart[0]

        test = sel.xpath('//div[@class="pt20 clearfix"]')
        excel = test.xpath('//div[@class="clearfix"][3]/div/p/text()').extract()
        item['e_expert_excel'] = ''
        if len(excel) == 1:
            item['e_expert_excel'] = excel[0]
        elif len(excel) == 2:
            item['e_expert_excel'] = excel[1]

        excel = test.xpath('//div[@class="clearfix"][4]/div/p/text()').extract()
        item['e_expert_experience'] = ''
        if len(excel) == 1:
            item['e_expert_experience'] = excel[0]
        elif len(excel) == 2:
            item['e_expert_experience'] = excel[1]

        test = sel.xpath('//div[@class="clearfix ml15 pt10"]/span[2]/text()').extract()
        item['e_expert_curative_level'] = test[0][0:-3]
        item['e_expert_attitude_level'] = test[1][0:-3]

        # next url
        next_url = sel.xpath('//div[@class="mt20 cca clearfix"]/span/a/@href').extract()
        item['e_expert_home_url'] = response.url
        item['e_expert_url'] = ''
        if next_url:
            item['e_expert_url'] = next_url[0]

        phone = sel.xpath('//div[@class="doctor-contact-phone clearfix"]/div/p//text()').extract()
        t_phone = ''
        for it in phone:
            t_phone = t_phone + it
        item['e_expert_phone_consult_details'] = t_phone
        phone_number = sel.xpath('//div[@class="doctor-contact-phone clearfix"]/div/p//span[@class="f16"]/text()').extract()
        if phone_number:
            item['e_expert_phone_consult_help'] = phone_number[0]
        else:
            item['e_expert_phone_consult_help'] = 0

        appoint = sel.xpath('//div[@class="doctor-contact-appointment clearfix"]/div//p/text()').extract()
        app = ''
        for it in appoint:
            app = app + it
        item['e_expert_add_appointment'] = app
        app_number = sel.xpath('//div[@class="doctor-contact-appointment clearfix"]/div//span[@class="f16"]/text()').extract()
        if app_number:
            item['e_expert_add_appointment_number'] = app_number[0]
        else:
            item['e_expert_add_appointment_number'] = 0

        image = sel.xpath('//div[@class="doctor-contact-tuw clearfix"]/div/p//text()').extract()
        im = ''
        for it in image:
            im = im + it
        item['e_expert_image_consult'] = im
        image_number = sel.xpath('//div[@class="doctor-contact-tuw clearfix"]/div//span[@class="f16"]/text()').extract()
        if image_number:
            item['e_expert_image_consult_help'] = image_number[0]
        else:
            item['e_expert_image_consult_help'] = 0

        if item['e_expert_url']:
            yield Request(url=item['e_expert_url'], meta={'item': item}, callback=self.deep7)

        phone_consult = sel.xpath('//ul[@class="z-functional-items z-doctor-items clearfix f14"]/li[3]//@href').extract()
        if phone_consult:
            yield Request(url=phone_consult[0], meta={'item': item}, callback=self.phone_consult)

        experience = sel.xpath('//ul[@class="z-functional-items z-doctor-items clearfix f14"]//@href').extract()
        url = experience[-1]
        yield Request(url=url, meta={'item': item}, callback=self.get_experience)

    def get_experience(self, response):
        item = response.meta['item']
        sel = Selector(response)
        all_thank = sel.xpath('//div[@class="brdc8"]')
        thanks = []
        for thank in all_thank:
            experience = ExperienceItem()
            title = thank.xpath('//div/span[1]/text()').extract()[0]
            title = title.split(' ')
            experience['e_experience_patient_id'] = title[0][3:]
            experience['e_experience_region'] = title[1][2:-3]
            ill = thank.xpath('//div/span[2]/text()').extract()[0]
            experience['e_experience_illness'] = ill[3:]
            experience['e_experience_effect'] = '5'
            experience['e_experience_attitude'] = '5'
            experience['e_experience_date'] = thank.xpath('//div/span[3]/text()').extract()[0]
            content = thank.xpath('//div[@class="thank_info pt10 pb10 f12 deepgray-a clearfix pl15 pr15"]//text()').extract()
            cont = ''
            for co in content:
                cont = cont + co
            experience['e_experience_content'] = cont
            experience['e_experience_like_number'] = thank.xpath('//div[@class="brdc8"]//em/text()').extract()[0]
            thanks.append(experience)

        item['e_expert_thank'] = thanks
        return item

    def phone_consult(self, response):
        item = response.meta['item']
        sel = Selector(response)
        price = sel.xpath('//span[@class="db z-serv-select tc z-serv-selected"]//text()').extract()
        alls = ''
        for p in price:
            alls = alls + p
        item['e_expert_phone_consult_price'] = alls
        all_con = sel.xpath('//ul[@class="tab z-slide-tab fYaHei fb"]/li[2]//@href').extract()
        if all_con:
            yield Request(url=all_con[0], meta={'item': item}, callback=self.get_all_phone_consult)
        else:
            yield item

    def get_all_phone_consult(self, response):
        item = response.meta['item']
        sel = Selector(response)
        orders = []
        all_order = sel.xpath('//div[@class="z-tab-items panel"]')
        # print response.url
        for order in all_order:
            the = PhoneConsultItem()
            patient_id = order.xpath('/div/span[1]/text()').extract()
            if patient_id:
                the['e_phone_consult_order_patient_id'] = patient[0]
            else:
                break

            the['e_phone_consult_order_ill'] = order.xpath('/div/span[2]/text()').extract()[0]
            detail = order.xpath('//p[@class="mt5 none z-detail-long"]/text()').extract()
            if detail:
                the['e_phone_consult_order_details'] = detail[0]
            else:
                break
            orders.append(the)
            # print response.url + the['e_phone_consult_order_details']

        item['e_expert_phone_orders'] = orders
        return item

    def deep7(self, response):
        sel = Selector(response)
        consult = sel.xpath('//div[@class="pl15 consult_info"]/p/text()').extract()
        item = response.meta['item']
        if consult:
            item['e_expert_consult_scope'] = consult[0]
        else:
            item['e_expert_consult_scope'] = ''
        appointment = sel.xpath('//div[@class="person_book  f12 pl10 pr10"]/span[@class="orange"]//text()').extract()
        if appointment:
            item['e_expert_appointment'] = appointment[0][0:-3]
        else:
            item['e_expert_appointment'] = 0

        visits = sel.xpath('//div[@class="greenbod"]/div[@class=" f12 padd10 lh30"]/span[1]//text()').extract()
        if visits:
            item['e_expert_visits'] = visits[0]
        else:
            item['e_expert_visits'] = 0

        article = sel.xpath('//div[@class="greenbod"]/div[@class=" f12 padd10 lh30"]/span[3]//text()').extract()
        if article:
            item['e_expert_article_number'] = article[0]
        else:
            item['e_expert_article_number'] = 0

        consult = sel.xpath('//div[@class="greenbod"]/div[@class=" f12 padd10 lh30"]/span[4]//text()').extract()
        if consult:
            item['e_expert_consult_number'] = consult[0]
        else:
            item['e_expert_consult_number'] = 0

        praise = sel.xpath('//div[@class="greenbod"]/div[@class=" f12 padd10 lh30"]/span[5]//text()').extract()
        if praise:
            item['e_expert_praise'] = praise[0]
        else:
            item['e_expert_praise'] = 0

        exp = sel.xpath('//div[@class="greenbod"]/div[@class=" f12 padd10 lh30"]/span[6]//text()').extract()
        if exp:
            item['e_expert_exp'] = exp[0]
        else:
            item['e_expert_exp'] = 0

        yield Request(url=response.url + '/zixun.php', meta={'item': item}, callback=self.deep9)

    def deep9(self, response):
        item = response.meta['item']
        sel = Selector(response)
        reply_number = sel.xpath('//span[@class="f12"]/em/text()').extract()
        if reply_number:
            item['e_expert_reply_number'] = reply_number[0]
        else:
            item['e_expert_reply_number'] = 0

        consult = sel.xpath('//span[@class="title_view lightblue-a"]/a/@href').extract()
        return item
       #  for url in consult:
       #      yield Request(url, meta={'item': item}, callback=self.deep_consult)

    def deep_consult(self, response):
        sel = Selector(response)
        item = reponse.meta['item']
        return item

