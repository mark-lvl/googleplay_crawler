# -*- coding: utf-8 -*-
import scrapy
from gplay.items import GplayItem


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['play.google.com']
    start_urls = ['https://play.google.com/store/apps/details?id=com.aa.generaladaptiveapps']

    def parse(self, response):
        item = GplayItem()
        item['App_name'] = response.xpath('//*[@itemprop="name"]/span/text()').extract()
        item['Genre'] = response.xpath('//*[@itemprop="genre"]/text()').extract()
        
        return item