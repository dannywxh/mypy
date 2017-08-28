# -*- coding: utf-8 -*-
import scrapy
from myspider.items import JavspiderItem


class JavSpider(scrapy.Spider):
    name = 'jav'
    allowed_domains = ['www.ja14b.com']

    offset = 1
    url='http://www.ja14b.com/cn/vl_update.php?&mode=&page='
    start_urls = [url+str(offset)]


    def parse(self, response):
        vnames=response.xpath('//div[@class="video"]/a/@title').extract()
        vurls=response.xpath('//div[@class="video"]/a/@href').extract()
        vids=response.xpath('//div[@class="video"]/a/div[@class="id"]/text()').extract()

        vlinks = ['http://www.ja14b.com/cn' + x[1:] for x in vurls]

        for vid, vname, link in zip(vids,vnames,vlinks):
            item = JavspiderItem()

            item['vid']=vid
            item['name']=vname
            item['url']=link

            yield item

        if self.offset < 10:
            self.offset += 1

        yield scrapy.Request(self.url+str(self.offset),callback=self.parse)

