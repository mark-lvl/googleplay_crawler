# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class GplayItem(Item):
    # Primary fields
    App_name        = Field()
    Link            = Field()
    Updated         = Field()
    Author          = Field()
    Filesize        = Field()
    Downloads       = Field()
    Version         = Field()
    Compatibility   = Field()
    Content_rating  = Field()
    Author_link     = Field()
    Genre           = Field()
    Price           = Field()
    Rating_value    = Field()
    Review_number   = Field()
    Description     = Field()
    IAP             = Field()
    Developer_badge = Field()
    Physical_address= Field()
    Video_URL       = Field()
    Developer_ID    = Field()

    # Housekeeping fields
    url             = Field()
    project         = Field()
    spider          = Field()
    server          = Field()
    date            = Field()
