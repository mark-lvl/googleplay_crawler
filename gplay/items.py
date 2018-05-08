# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class GplayItem(Item):
    # Primary fields
    App_name        = Field()
    Price           = Field()
    Editor_choice   = Field()
    Developer       = Field()
    Developer_loc   = Field()
    Developer_URL   = Field()
    Genre           = Field()
    Content_rating  = Field()
    Promotion       = Field()
    Description     = Field()
    App_rate        = Field()
    Reviewers_count = Field()
    Rate_5star      = Field()
    Rate_4star      = Field()
    Rate_3star      = Field()
    Rate_2star      = Field()
    Rate_1star      = Field()
    Update_date     = Field()
    Version         = Field()
    Filesize        = Field()
    Install_count   = Field()
    Android_version = Field()
    Inapp_products  = Field()
    Offered_by      = Field()

    # Housekeeping fields
    URL             = Field()
    Scraper_project = Field()
    Scraper_spider  = Field()
    Scraper_server  = Field()
    Scraper_date    = Field()
