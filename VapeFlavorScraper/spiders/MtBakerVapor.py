import scrapy
import logging
from VapeFlavorScraper.items import VapeFlavorItem


class MtBakerVaporSpider(scrapy.Spider):
    name = 'MtBakerVapor'
    allowed_domains = ['mtbakervapor.com']
    start_urls = ['https://www.mtbakervapor.com/flavor-shots/']
    page_number = 2

    def parse(self, response):

        #Get all the flavor items on this page
        item_links = response.css('li.product > article.card > div > h4 > a::attr(href)').extract()

        #Process each flavor item
        for a in item_links:
            yield scrapy.Request( a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        name = response.css('section.productView-header > div > h1::text').extract()[0]
        image_url = response.css('img.productView-image--default::attr(src)').extract()[0]

        description = ''

        item = VapeFlavorItem()
        item['name'] = name
        item['link'] = response.url
        item['manufacturer'] = 'Mt Baker Vapor'
        item['image_url'] = image_url
        item['description'] = description

        yield item
