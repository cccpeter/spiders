# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    author = scrapy.Field()
    data = scrapy.Field()
    readnum = scrapy.Field()
    fans = scrapy.Field()
    likes = scrapy.Field()
    comment = scrapy.Field()
    # content = scrapy.Field()

