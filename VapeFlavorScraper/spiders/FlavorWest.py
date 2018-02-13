import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class FlavorWestSpider(scrapy.Spider):
    name = 'FlavorWest'
    allowed_domains = ['flavorwest.com']
    start_urls = [
        'http://flavorwest.com/index.php/water-soluble-flavoring.html?limit=all',
        'http://flavorwest.com/index.php/natural-flavoring.html?limit=all',
        'http://flavorwest.com/index.php/caffeine.html?limit=all'
    ]

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('div.item-title > a::attr(href)').extract()

        for link in item_links:
            yield scrapy.Request( link , callback=self.parse_detail_page )


    def parse_detail_page(self, response):

        name = response.css('div.product-shop > div.product-name > h1::text').extract_first()
        image_url = response.css('#zoom1::attr(href)').extract_first()

        description = ''

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Flavor West'
        item['image_url'] = image_url
        item['description'] = description

        yield item
