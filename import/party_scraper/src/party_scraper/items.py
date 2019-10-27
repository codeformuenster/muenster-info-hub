# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PartyItem(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    location_name = scrapy.Field()
    location_address = scrapy.Field()
    geo = scrapy.Field()
    images = scrapy.Field()
    source = scrapy.Field()
