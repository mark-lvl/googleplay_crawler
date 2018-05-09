# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import logging

class GplayPipeline(object):
    def process_item(self, item, spider):
        return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.seen_packagenames = set()

    def process_item(self, item, spider):
        if str(item['Package_name']) in set(self.seen_packagenames):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.seen_packagenames.add(str(item['Package_name']))
            return item