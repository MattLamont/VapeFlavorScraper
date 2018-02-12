import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class AzureVapingSpider(scrapy.Spider):
    name = 'AzureVaping'
    allowed_domains = ['azurevaping.com']
    start_urls = [
        'https://www.azurevaping.com/gourmet-flavors-for-diy.html?limit=all',
    ]

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('h2.product-name > a::attr(href)').extract()

        #If there are no flavor items on this page, then get out
        if len(item_links) is 0:
            return

        #Process each flavor item
        for a in item_links:
            yield scrapy.Request( a, callback=self.parse_detail_page)

        next_page = response.css('a.next::attr(href)').extract_first()

        if next_page is not None:
            yield scrapy.Request( next_page, callback=self.parse)

    def parse_detail_page(self, response):
        name = response.css('div.product-name > h1::text').extract_first()
        image_url = response.css('p.product-image > img::attr(src)').extract()

        description = response.css('div.std::text').extract()

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Azure Vaping'
        item['image_url'] = image_url
        item['description'] = description

        yield item
