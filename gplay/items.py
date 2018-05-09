# -*- coding: utf-8 -*-

from scrapy.item import Item, Field
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose
from w3lib.html import remove_tags
import re

""" Calculating promotions in app
    0: no promotion
    1: Contains Adds
    2: Offers in-app purchases
    3: Contains Adds . Offers in-app purchases
"""
def promotion_status(value):
    promotion = 0
    if ("Contains Ads" in value):
            promotion = promotion + 1
    if ("Offers in-app purchases" in value):
        promotion = promotion + 2
    return promotion

class GplayItem(Item):
    
    # Primary fields
    App_name          = Field(input_processor=MapCompose(str.strip, str.lower))
    Package_name      = Field(input_processor=MapCompose(lambda x: re.search(r'details\?id=(.*)\&',x).group(1)))
    Genre             = Field(input_processor=MapCompose(str.strip, str.lower),
                              output_processor=Join("|"))
    Price             = Field(input_processor=MapCompose(lambda x: re.search(r"[,.0-9]+",x).group()))
    Editor_choice     = Field(input_processor=Compose(lambda x: "0" if len(x) == 0 else "1"))
    Developer         = Field(input_processor=MapCompose(str.strip))
    Developer_URL     = Field(input_processor=MapCompose(str.strip))
    Content_rating    = Field(input_processor=MapCompose(str.strip))
    Promotion         = Field(input_processor=Compose(promotion_status))
    Description       = Field(input_processor=MapCompose(str.strip, 
                                                         lambda i: i.replace("'", ''), 
                                                         str.lower,
                                                         remove_tags),
                              output_processor=Join())
    App_rate          = Field(input_processor=MapCompose(float))
    Reviewers_count   = Field()
    Rate_5star        = Field()
    Rate_4star        = Field()
    Rate_3star        = Field()
    Rate_2star        = Field()
    Rate_1star        = Field()
    Developer_location= Field(input_processor=MapCompose(str.strip, 
                                                         lambda i: i.replace("'", ''), 
                                                         lambda i: i.replace("\n", ' '), 
                                                         str.lower,
                                                         remove_tags))
    Update_date       = Field()
    Version           = Field()
    Filesize          = Field()
    Install_count     = Field()
    Android_version   = Field()
    Inapp_products    = Field()
    Offered_by        = Field()

    # Housekeeping fields
    URL               = Field()
    Scraper_project   = Field()
    Scraper_spider    = Field()
    Scraper_server    = Field()
    Scraper_date      = Field()
