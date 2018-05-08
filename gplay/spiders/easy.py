# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from gplay.items import GplayItem
from scrapy.http import Request
import datetime
import socket
from urllib.parse import urljoin


class EasySpider(CrawlSpider):
    name = 'easy'
    allowed_domains = ['play.google.com']
    start_urls = ['https://play.google.com/store/apps/details?id=homeworkout.homeworkouts.noequipment']

    rules = (
        # First rule: only scan target pages - without scraping
        Rule(LinkExtractor(restrict_xpaths='//div[contains(@class,'"cluster-heading"')]/h2/span/a')),
        # Second rule: scraping the apps pages without scaning for further pages.
        Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,'"card-click-target"')]'), callback='parse_item')
    )

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
        editor_choice = response.xpath('//img[@alt="Editors\' Choice"]/following-sibling::span[text()="Editors\' Choice"]')
        editor_choice = 1 if editor_choice else 0
        l.add_value('Editor_choice', editor_choice)

        ## Filling housekeeping fields
        l.add_value('URL', response.url)
        l.add_value('Project', self.settings.get('BOT_NAME'))
        l.add_value('Spider', self.name)
        l.add_value('Server', socket.gethostname())
        l.add_value('Date', datetime.datetime.now())
        
        return l.load_item()
