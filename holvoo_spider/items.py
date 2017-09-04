# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    subtitles = scrapy.Field()
    body = scrapy.Field()
    comments = scrapy.Field()
