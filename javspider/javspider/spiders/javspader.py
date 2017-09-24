# -*- coding: utf-8 -*-
import scrapy
from javspider.items import JavspiderItem
import sys
from javspider.common import format_rule2

reload(sys)
sys.setdefaultencoding('utf-8')


class JavspaderSpider(scrapy.Spider):
    name = 'jav'
    allowed_domains = ['www.ja14b.com']

    offset = 1
    url='http://www.ja14b.com/cn/vl_update.php?&mode=&page='

    start_urls=[url+str(offset)]

    has_done=['JUC-540','JUC-542','JUC-552']

    def parse(self, response):

        #vurls = response.xpath('//div[@class="video"]/a/@href').extract()

        vurls = response.css("div.video > a::attr(href)").extract()

        print vurls

        vids = response.css("div.video > a > div.id::text").extract()

        print vids

        links = ['http://www.ja14b.com/cn' + x[1:] for x in vurls]
        for vid, link in zip(vids, links):
            if vid in self.has_done:
                print "----------Has Exist!-------------"
            else:
                yield scrapy.Request(link, callback=self.parse_detail)

        if self.offset < 2:
            self.offset += 1

        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    def parse_detail(self, response):

        img = response.xpath('//*[@id="video_jacket"]/img[@id="video_jacket_img"]/@src').extract()[0]

        id = response.xpath('//div[@id="video_id"]//td[@class="text"]/text()').extract()[0]
        date = response.xpath('//div[@id="video_date"]//td[@class="text"]/text()').extract()[0]

        try:
            score = response.xpath('//div[@id="video_review"]//td[@class="text"]/span[@class="score"]/text()').extract()[0]
        except Exception as e:
            score =""

        genres_list = response.xpath('//div[@id="video_genres"]//span[@class="genre"]/a/text()').extract()[0]
        genres = " ".join(genres_list)
        cast_list = response.xpath('//div[@id="video_cast"]//span[@class="star"]/a/text()').extract()
        cast=" ".join(cast_list)
        wanted = response.xpath('//span[@id="subscribed"]/a/text()').extract()[0]
        owned = response.xpath('//span[@id="owned"]/a/text()').extract()[0]

        item=JavspiderItem()

        item['id']=format_rule2(id)
        item['img']="http:"+img
        item['date']=date
        item['score']=score
        item['wanted']=wanted
        item['owned']=owned
        item['genres']=genres
        item['cast']=cast

        yield item

