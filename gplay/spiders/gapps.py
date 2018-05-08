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
import re
from urllib.parse import urljoin


class GappsSpider(CrawlSpider):
    name = 'gapps'
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com/store/apps/"]
    rules = (
        Rule(LinkExtractor(allow=('/store/apps/details?')),follow=True,callback='parse_item'),
        Rule(LinkExtractor(allow=('/store/apps',)),follow=True))

    def parse_item(self, response):
        l = ItemLoader(item=GplayItem(), response=response)
        
        l.add_xpath('App_name',
                    '//*[@itemprop="name"]/span/text()',
                    MapCompose(str.strip, str.lower))
        
        l.add_xpath('Genre',
                    '//*[@itemprop="genre"]/text()',
                    MapCompose(str.strip, str.lower), Join("|"))
        
        l.add_xpath('Price','//*[@itemprop="price"]/@content', re="[,.0-9]+")

        #editor_choice = response.xpath('//img[@alt="Editors\' Choice"]/following-sibling::span[text()="Editors\' Choice"]')
        editor_choice = response.xpath('//*[@itemprop="editorsChoiceBadgeUrl"]')
        l.add_value('Editor_choice', int(bool(editor_choice)))
        
        l.add_xpath('Developer',
                    '//span/a[@itemprop="genre"][1]/../../span[1]/a/text()',
                    MapCompose(str.strip))
        
        l.add_xpath('Developer_URL',
                    '//span/a[@itemprop="genre"][1]/../../span[1]/a/@href',
                    MapCompose(str.strip))
        
        
        l.add_xpath('Content_rating',
                    '//div[contains(text(),"Content Rating")]/following-sibling::span/div/span/div[1]/text()',
                    MapCompose(str.strip))
        
        """ Calculating promotions in app
        0: no promotion
        1: Contains Adds
        2: Offers in-app purchases
        3: Contains Adds . Offers in-app purchases
        """
        promotion = 0
        promotion_selector = response.xpath('//div[contains(text(), "Contains Ads") or contains(text(), "Offers in-app purchases")]/text()').extract()
        if ("Contains Ads" in promotion_selector):
            promotion = promotion + 1
        if ("Offers in-app purchases" in promotion_selector):
            promotion = promotion + 2
        l.add_value('Promotion', promotion)

        l.add_xpath('Description',
                    '//content/div/text()',
                    MapCompose(str.strip, lambda i: i.replace("'", ''), str.lower), Join())

        l.add_xpath('App_rate',
                    '//div[contains(@aria-label,"stars out of five stars")]/text()',
                    MapCompose(float))
        
        l.add_xpath('Reviewers_count',
                    '(//span[contains(@aria-label,"ratings")])[1]/text()')

        # There are five grades in star for rating apps
        for i in range(5, 0,-1):
            l.add_xpath('Rate_'+str(i)+'star',
                        '//div/div/span[text()='+str(i)+']/following-sibling::span/@title')

        # Batch scraping fields at the bottom of the app page
        info_fields = {"Update_date":"Updated", "Filesize":"Size", "Install_count":"Installs", 
                       "Version":"Current Version", "Android_version":"Requires Android",
                       "Inapp_products":"In-app Products", "Offered_by":"Offered By"}
        
        for field_name, xpath_name in info_fields.items():
            l.add_xpath(field_name,
                        '//div/div/div/div[text()="'+str(xpath_name)+'"]/following-sibling::span/div/span/text()')

        l.add_xpath('Developer_location',
                    '//div/span/div/span/div/a[text()="Privacy Policy"]/../following-sibling::div/text()',
                    MapCompose(str.strip, 
                               lambda i: i.replace("'", ''), 
                               lambda i: i.replace("\n", ' '), 
                               str.lower))
        

        ## Filling housekeeping fields
        l.add_value('URL', response.url)
        l.add_value('Scraper_project', self.settings.get('BOT_NAME'))
        l.add_value('Scraper_spider', self.name)
        l.add_value('Scraper_server', socket.gethostname())
        l.add_value('Scraper_date', datetime.datetime.now())
        
        return l.load_item()