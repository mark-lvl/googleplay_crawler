# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from gplay.items import GplayItem
from scrapy.http import Request
import datetime
import socket
from urllib.parse import urljoin


class ManualSpider(scrapy.Spider):
    name = 'manual'
    allowed_domains = ['play.google.com']
    start_urls = ['https://play.google.com/store/apps/']

    def parse(self, response):
        # Get the see more URLs and yeild requests
        see_more_selector = response.xpath('//*[contains(@class,'"see-more"')]')

        for url in see_more_selector.extract():
            yield Request(urljoin(response.url, url))

        # Get item URLs and yield Requests
        app_selector = response.xpath('//*[contains(@class,'"card-click-target"')]/@href')
        for url in app_selector.extract():
            yield Request(urljoin(response.url, url),
                          callback=self.parse_item)

    def parse_item(self, response):
        """ This function parses an application page in Google Play.
        @url https://play.google.com/store/apps/details?id=com.aa.generaladaptiveapps
        @returns items 1
        @scrapes App_name Genre
        @scrapes URL Project Spider Server Date
        """
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