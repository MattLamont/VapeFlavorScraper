import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class LiquidBarnSpider(scrapy.Spider):
    name = 'LiquidBarn'
    allowed_domains = ['liquidbarn.com']
    start_urls = [
        'https://www.liquidbarn.com/collections/beverage-flavors',
        'https://www.liquidbarn.com/collections/dessert-flavors',
        'https://www.liquidbarn.com/collections/fruity-flavors',
        'https://www.liquidbarn.com/collections/tobacco-flavors',
        'https://www.liquidbarn.com/collections/flavor-enhancers'
    ]

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('div.product-grid-item > a::attr(href)').extract()

        #If there are no flavor items on this page, then get out
        if len(item_links) is 0:
            return

        #Process each flavor item
        for a in item_links:
            yield scrapy.Request( 'https://www.liquidbarn.com' + a, callback=self.parse_detail_page)

        return

    def parse_detail_page(self, response):
        name = response.css('#productInfo-product > div > h1::text').extract()[0]
        image_url = response.css('img.ProductImg-product::attr(src)').extract()

        description = response.css('#productInfo-product > div > div > div > p:nth-child(2) > span::text').extract()

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Liquid Barn'
        item['image_url'] = image_url
        item['description'] = description

        yield item
