import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class CountryKitchenSpider(scrapy.Spider):
    name = 'CountryKitchen'
    allowed_domains = ['countrykitchensa.com']
    start_urls = [
        'https://www.countrykitchensa.com/shop/food-items/flavoring-and-extracts/46/589/1056/?sort=0&y=Brand&x0=379',
    ]

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('div.productInMinisText > div.mainText > a::attr(href)').extract()

        for link in item_links:
            yield scrapy.Request( 'https://www.countrykitchensa.com' + link , callback=self.parse_detail_page )


    def parse_detail_page(self, response):

        name = response.css('#pDescription > h1::text').extract_first()
        image_url = response.css('#pImage::attr(src)').extract_first()

        description = response.css('#tabs-1 > p::text').extract_first()

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Country Kitchen'
        item['image_url'] = image_url
        item['description'] = description

        yield item
