# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VapeFlavorItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    link = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    manufacturer = scrapy.Field()
    isNewFlavor = scrapy.Field()
