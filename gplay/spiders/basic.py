# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from gplay.items import GplayItem
import datetime
import socket


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['play.google.com']
    start_urls = ['https://play.google.com/store/apps/details?id=com.aa.generaladaptiveapps']

    def parse(self, response):
        l = ItemLoader(item=GplayItem(), response=response)
        l.add_xpath('App_name',
                    '//*[@itemprop="name"]/span/text()',
                    MapCompose(str.strip))
        l.add_xpath('Genre',
                    '//*[@itemprop="genre"]/text()',
                    MapCompose(str.strip))

        ## Filling housekeeping fields
        l.add_value('URL', response.url)
        l.add_value('Project', self.settings.get('BOT_NAME'))
        l.add_value('Spider', self.name)
        l.add_value('Server', socket.gethostname())
        l.add_value('Date', datetime.datetime.now())
        
        return l.load_item()