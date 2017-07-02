# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
class ImbdcrawlerItem(scrapy.Item):
    # Movie details
    Title = scrapy.Field()
    Page = scrapy.Field()
    Description = scrapy.Field()
    Rating = scrapy.Field()
    Directors = scrapy.Field()
    Actors = scrapy.Field()
    Genres = scrapy.Field()
    Length = scrapy.Field()
    Year = scrapy.Field()
    Votes = scrapy.Field()
    Income = scrapy.Field()


    # Housekeeping fields
    Url = scrapy.Field()
    Project = scrapy.Field()
    Spider = scrapy.Field()
    Server = scrapy.Field()
    Date = scrapy.Field()

