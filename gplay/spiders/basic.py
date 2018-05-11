# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from gplay.items import GplayItem
import datetime
import socket
import re


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['play.google.com']
    #start_urls = ['https://play.google.com/store/apps/details?id=com.solverlimited.woc2']
    start_urls = ['https://play.google.com/store/apps/details?id=com.mojang.minecraftpe']

    #def parse(self, response):
        # DEBUGGING SCRAPY: We want to inspect one specific response.
        #if ".org" in response.url:
        #    from scrapy.shell import inspect_response
        #    inspect_response(response, self)

    # RUN in TERMINAL by
    # scrapy crawl basic -o spider.jl -s CLOSESPIDER_PAGECOUNT=100 --logfile log.log

    # Debugging the spider in terminal
    # scrapy parse --spider=gapps -c parse_item -d 2 -v https://play.google.com/store/apps/details?id=com.mojang.minecraftp

    def parse(self, response):
        """ This function parses an application page in Google Play.
        @url https://play.google.com/store/apps/details?id=com.mojang.minecraftpe
        @returns items 1
        @scrapes App_name Genre
        @scrapes URL Project Spider Server Date
        """
        # DEBUGGING SCRAPY: Logging in Scrapy
        # logger = logging.getLogger()
        # logger.warning("Your Message here")
        # logger.debug("Your Message here")
        # Inside the spider we can eaily use:
        # self.logger.info('Your Message here')

        l = ItemLoader(item=GplayItem(), response=response)
        
        l.add_xpath('App_name', '//*[@itemprop="name"]/span/text()')
        
        l.add_xpath('Package_name', '//meta[@property="og:url"]/@content')
        
        l.add_xpath('Genre', '//*[@itemprop="genre"]/text()')
        
        l.add_xpath('Price', '//*[@itemprop="price"]/@content')

        l.add_xpath('Editor_choice', '//*[@itemprop="editorsChoiceBadgeUrl"]')
        
        l.add_xpath('Developer', '//span/a[@itemprop="genre"][1]/../../span[1]/a/text()')
        
        l.add_xpath('Developer_URL', '//span/a[@itemprop="genre"][1]/../../span[1]/a/@href')
             
        l.add_xpath('Content_rating', '//div[contains(text(),"Content Rating")]/following-sibling::span/div/span/div[1]/text()')
        
        l.add_xpath('Promotion', '//div[contains(text(), "Contains Ads") or contains(text(), "Offers in-app purchases")]/text()')

        l.add_xpath('Description','//content/div/text()')

        l.add_xpath('App_rate', '//div[contains(@aria-label,"stars out of five stars")]/text()')
        
        l.add_xpath('Reviewers_count', '(//span[contains(@aria-label,"ratings")])[1]/text()')

        l.add_xpath('Developer_location', '//div/span/div/span/div/a[text()="Privacy Policy"]/../following-sibling::div/text()')
        
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
        
        ## Filling housekeeping fields
        l.add_value('URL', response.url)
        l.add_value('Scraper_project', self.settings.get('BOT_NAME'))
        l.add_value('Scraper_spider', self.name)
        l.add_value('Scraper_server', socket.gethostname())
        l.add_value('Scraper_date', str(datetime.datetime.now()))
        
        return l.load_item()